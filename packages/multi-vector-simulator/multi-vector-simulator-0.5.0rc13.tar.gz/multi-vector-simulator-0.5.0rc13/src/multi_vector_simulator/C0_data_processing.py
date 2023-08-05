import logging
import os
import sys

import pandas as pd
import warnings

from multi_vector_simulator.utils.constants import (
    TIME_SERIES,
    PATH_INPUT_FOLDER,
    PATH_OUTPUT_FOLDER,
    TYPE_BOOL,
    FILENAME,
    HEADER,
    DEFAULT_WEIGHTS_ENERGY_CARRIERS,
)

from multi_vector_simulator.utils.constants_json_strings import *
import multi_vector_simulator.B0_data_input_json as B0
import multi_vector_simulator.C1_verification as C1
import multi_vector_simulator.C2_economic_functions as C2
import multi_vector_simulator.F0_output as F0

"""
Module C0 prepares the data read from csv or json for simulation, ie. pre-processes it. 
- Verify input values with C1
- Identify energyVectors and write them to project_data/sectors
- Create an excess sink for each bus
- Process start_date/simulation_duration to pd.datatimeindex (future: Also consider timesteplenghts)
- Add economic parameters to json with C2
- Calculate "simulation annuity" used in oemof model
- Add demand sinks to energyVectors (this should actually be changed and demand sinks should be added to bus relative to input_direction, also see issue #179)
- Translate input_directions/output_directions to bus names
- Add missing cost data to automatically generated objects (eg. DSO transformers)
- Read timeseries of assets and store into json (differ between one-column csv, multi-column csv)
- Read timeseries for parameter of an asset, eg. efficiency
- Parse list of inputs/outputs, eg. for chp
- Define dso sinks, sources, transformer stations (this will be changed due to bug #119), also for peak demand pricing
- Add a source if a conversion object is connected to a new input_direction (bug #186)
- Define all necessary energyBusses and add all assets that are connected to them specifically with asset name and label
- Multiply `maximumCap` of non-dispatchable sources by max(timeseries(kWh/kWp)) as the `maximumCap` is limiting the flow but we want to limit the installed capacity (see issue #446)
"""


class InvalidPeakDemandPricingPeriods(ValueError):
    # Exeption if an input is not valid
    pass


class UnknownEnergyCarrier(ValueError):
    # Exception if an energy carrier is not in DEFAULT_WEIGHTS_ENERGY_CARRIERS
    pass


def all(dict_values):
    """
    Function executing all pre-processing steps necessary
    :param dict_values
    All input data in dict format

    :return Pre-processed dictionary with all input parameters

    """
    B0.retrieve_date_time_info(dict_values[SIMULATION_SETTINGS])
    add_economic_parameters(dict_values[ECONOMIC_DATA])
    identify_energy_vectors(dict_values)

    ## Verify inputs
    # todo check whether input values can be true
    # C1.check_input_values(dict_values)
    # todo Check, whether files (demand, generation) are existing

    # Adds costs to each asset and sub-asset, adds time series to assets
    process_all_assets(dict_values)

    # check electricity price >= feed-in tariff todo: can be integrated into check_input_values() later
    C1.check_feedin_tariff(dict_values=dict_values)

    # check time series of non-dispatchable sources in range [0, 1]
    C1.check_non_dispatchable_source_time_series(dict_values)

    # Perform basic (limited) check for moduel completeness
    C1.check_for_sufficient_assets_on_busses(dict_values)

    F0.store_as_json(
        dict_values,
        dict_values[SIMULATION_SETTINGS][PATH_OUTPUT_FOLDER],
        "json_input_processed",
    )


def identify_energy_vectors(dict_values):
    """
    Identifies all energyVectors used in the energy system by checking every entry 'energyVector' of all assets.
    energyVectors later will be used to distribute costs and KPI amongst the sectors (not implemented)

    Parameters
    ----------
    dict_values: dict
        All input data in dict format

    Returns
    -------
    Update dict['project_data'] by used sectors

    Notes
    -----
    Function tested with test_add_economic_parameters()
    """
    dict_of_sectors = {}
    names_of_sectors = ""
    for level1 in dict_values.keys():
        for level2 in dict_values[level1].keys():
            if (
                isinstance(dict_values[level1][level2], dict)
                and ENERGY_VECTOR in dict_values[level1][level2].keys()
            ):
                energy_vector_name = dict_values[level1][level2][ENERGY_VECTOR]
                if energy_vector_name not in dict_of_sectors.keys():
                    check_if_energy_carrier_is_defined_in_DEFAULT_WEIGHTS_ENERGY_CARRIERS(
                        energy_vector_name, level1, level2
                    )
                    dict_of_sectors.update(
                        {energy_vector_name: energy_vector_name.replace("_", " ")}
                    )
                    names_of_sectors = names_of_sectors + energy_vector_name + ", "

    dict_values[PROJECT_DATA].update({SECTORS: dict_of_sectors})
    logging.info(
        "The energy system modelled includes following energy vectors / sectors: %s",
        names_of_sectors[:-2],
    )


def check_if_energy_carrier_is_defined_in_DEFAULT_WEIGHTS_ENERGY_CARRIERS(
    energy_carrier, asset_group, asset
):
    r"""
    Raises an error message if an energy vector is unknown.

    It then needs to be added to the DEFAULT_WEIGHTS_ENERGY_CARRIERS in constants.py

    Parameters
    ----------
    energy_carrier: str
        Name of the energy carrier

    asset_group: str
        Name of the asset group

    asset: str
        Name of the asset

    Returns
    -------
    None

    Notes
    -----
    Tested with:
    - test_check_if_energy_carrier_is_defined_in_DEFAULT_WEIGHTS_ENERGY_CARRIERS_pass()
    - test_check_if_energy_carrier_is_defined_in_DEFAULT_WEIGHTS_ENERGY_CARRIERS_fails()
    """
    if energy_carrier not in DEFAULT_WEIGHTS_ENERGY_CARRIERS:
        raise UnknownEnergyCarrier(
            f"The energy carrier {energy_carrier} of asset group {asset_group}, asset {asset} is unknown, "
            f"as it is not defined within the DEFAULT_WEIGHTS_ENERGY_CARRIERS."
            f"Please check the energy carrier, or update the DEFAULT_WEIGHTS_ENERGY_CARRIERS in contants.py (dev)."
        )


def add_economic_parameters(economic_parameters):
    """
    Update economic parameters with annuity factor and CRF

    Parameters
    ----------

    economic_parameters: dict
        Economic parameters of the simulation

    Returns
    -------

    Updated economic parameters

    Notes
    -----
    Function tested with test_add_economic_parameters()
    """

    economic_parameters.update(
        {
            ANNUITY_FACTOR: {
                VALUE: C2.annuity_factor(
                    economic_parameters[PROJECT_DURATION][VALUE],
                    economic_parameters[DISCOUNTFACTOR][VALUE],
                ),
                UNIT: "?",
            }
        }
    )
    # Calculate crf
    economic_parameters.update(
        {
            CRF: {
                VALUE: C2.crf(
                    economic_parameters[PROJECT_DURATION][VALUE],
                    economic_parameters[DISCOUNTFACTOR][VALUE],
                ),
                UNIT: "?",
            }
        }
    )


def process_all_assets(dict_values):
    """defines dict_values['energyBusses'] for later reference

    :param dict_values:
    :return:
    """
    # Define all busses based on the in- and outflow directions of the assets in the input data
    define_busses(dict_values)
    # Define all excess sinks for each energy bus
    auto_sinks = define_excess_sinks(dict_values)

    # Needed for E3.total_demand_each_sector(), but location is not perfect as it is more about the model then the settings.
    # Decided against implementing a new major 1st level category in json to avoid an excessive datatree.
    dict_values[SIMULATION_SETTINGS].update({EXCESS + AUTO_SINK: auto_sinks})

    # process all energyAssets:
    # Attention! Order of asset_groups important. for energyProviders/energyConversion sinks and sources
    # might be defined that have to be processed in energyProduction/energyConsumption

    # The values of the keys are functions!
    asset_group_list = {
        ENERGY_PROVIDERS: energyProviders,
        ENERGY_CONVERSION: energyConversion,
        ENERGY_STORAGE: energyStorage,
        ENERGY_PRODUCTION: energyProduction,
        ENERGY_CONSUMPTION: energyConsumption,
    }

    for asset_group, asset_function in asset_group_list.items():
        logging.info("Pre-processing all assets in asset group %s.", asset_group)
        # call asset function connected to current asset group (see asset_group_list)
        asset_function(dict_values, asset_group)

        logging.debug(
            "Finished pre-processing all assets in asset group %s.", asset_group
        )

    logging.info("Processed cost data and added economic values.")


def define_excess_sinks(dict_values):
    r"""
    Define energy excess sinks for each bus

    Parameters
    ----------
    dict_values: dict
        All simulation parameters

    Returns
    -------
    Updates dict_values
    """
    auto_sinks = []
    for bus_name in dict_values[ENERGY_BUSSES]:
        excess_sink_name = bus_name + EXCESS
        energy_vector = dict_values[ENERGY_BUSSES][bus_name][ENERGY_VECTOR]
        define_sink(
            dict_values=dict_values,
            asset_name=excess_sink_name,
            price={VALUE: 0, UNIT: CURR + "/" + UNIT},
            input_bus_name=bus_name,
            energy_vector=energy_vector,
        )
        dict_values[ENERGY_BUSSES][bus_name].update({EXCESS: excess_sink_name})
        auto_sinks.append(excess_sink_name)
        logging.debug(
            f"Created excess sink for energy bus {bus_name}, connected to {ENERGY_VECTOR} {energy_vector}."
        )
    return auto_sinks


def energyConversion(dict_values, group):
    """Add lifetime capex (incl. replacement costs), calculate annuity (incl. om), and simulation annuity to each asset

    :param dict_values:
    :param group:
    :return:
    """
    #
    for asset in dict_values[group]:
        define_missing_cost_data(dict_values, dict_values[group][asset])
        evaluate_lifetime_costs(
            dict_values[SIMULATION_SETTINGS],
            dict_values[ECONOMIC_DATA],
            dict_values[group][asset],
        )
        # check if maximumCap exists and add it to dict_values
        process_maximum_cap_constraint(
            dict_values=dict_values, group=group, asset=asset
        )

        # in case there is only one parameter provided (input bus and one output bus)
        if (
            FILENAME in dict_values[group][asset][EFFICIENCY]
            and HEADER in dict_values[group][asset][EFFICIENCY]
        ):
            receive_timeseries_from_csv(
                dict_values[SIMULATION_SETTINGS], dict_values[group][asset], EFFICIENCY,
            )
        # in case there is more than one parameter provided (either (A) n input busses and 1 output bus or (B) 1 input bus and n output busses)
        # dictionaries with filenames and headers will be replaced by timeseries, scalars will be mantained
        elif isinstance(dict_values[group][asset][EFFICIENCY][VALUE], list):
            treat_multiple_flows(dict_values[group][asset], dict_values, EFFICIENCY)

            # same distinction of values provided with dictionaries (one input and one output) or list (multiple).
            # They can at turn be scalars, mantained, or timeseries
            logging.debug(
                "Asset %s has multiple input/output busses with a list of efficiencies. Reading list",
                dict_values[group][asset][LABEL],
            )
        else:
            logging.debug(f"Not loading {group} asset {asset} from file")
            compute_timeseries_properties(dict_values[group][asset])


def energyProduction(dict_values, group):
    """

    :param dict_values:
    :param group:
    :return:
    """
    for asset in dict_values[group]:
        define_missing_cost_data(dict_values, dict_values[group][asset])
        evaluate_lifetime_costs(
            dict_values[SIMULATION_SETTINGS],
            dict_values[ECONOMIC_DATA],
            dict_values[group][asset],
        )

        if FILENAME in dict_values[group][asset]:
            if dict_values[group][asset][FILENAME] in ("None", None):
                dict_values[group][asset].update({DISPATCHABILITY: True})
                check_if_energy_carrier_is_defined_in_DEFAULT_WEIGHTS_ENERGY_CARRIERS(
                    asset, group, asset
                )
            else:
                receive_timeseries_from_csv(
                    dict_values[SIMULATION_SETTINGS],
                    dict_values[group][asset],
                    "input",
                )
                # If Filename defines the generation timeseries, then we have an asset with a lack of dispatchability
                dict_values[group][asset].update({DISPATCHABILITY: False})
        else:
            logging.debug(
                f"Not loading {group} asset {asset} from a file, timeseries is provided"
            )
            compute_timeseries_properties(dict_values[group][asset])
        # check if maximumCap exists and add it to dict_values
        process_maximum_cap_constraint(dict_values, group, asset)


def energyStorage(dict_values, group):
    """

    :param dict_values:
    :param group:
    :return:
    """
    for asset in dict_values[group]:
        for subasset in [STORAGE_CAPACITY, INPUT_POWER, OUTPUT_POWER]:
            # Redefining the label of storage components, ie. so that is is clear to which storage a component (eg. input power) belongs.
            dict_values[group][asset][subasset].update(
                {
                    LABEL: dict_values[group][asset][LABEL]
                    + "_"
                    + dict_values[group][asset][subasset][LABEL]
                }
            )
            define_missing_cost_data(
                dict_values, dict_values[group][asset][subasset],
            )
            evaluate_lifetime_costs(
                dict_values[SIMULATION_SETTINGS],
                dict_values[ECONOMIC_DATA],
                dict_values[group][asset][subasset],
            )

            # check if parameters are provided as timeseries
            for parameter in [EFFICIENCY, SOC_MIN, SOC_MAX]:
                if parameter in dict_values[group][asset][subasset] and isinstance(
                    dict_values[group][asset][subasset][parameter][VALUE], dict
                ):
                    receive_timeseries_from_csv(
                        dict_values[SIMULATION_SETTINGS],
                        dict_values[group][asset][subasset],
                        parameter,
                    )
                elif parameter in dict_values[group][asset][subasset] and isinstance(
                    dict_values[group][asset][subasset][parameter][VALUE], list
                ):
                    treat_multiple_flows(
                        dict_values[group][asset][subasset], dict_values, parameter
                    )
            # check if maximumCap exists and add it to dict_values
            process_maximum_cap_constraint(dict_values, group, asset, subasset)

        # define input and output bus names
        dict_values[group][asset].update(
            {INPUT_BUS_NAME: bus_suffix(dict_values[group][asset][INFLOW_DIRECTION])}
        )
        dict_values[group][asset].update(
            {OUTPUT_BUS_NAME: bus_suffix(dict_values[group][asset][OUTFLOW_DIRECTION])}
        )


def energyProviders(dict_values, group):
    """

    :param dict_values:
    :param group:
    :return:
    """
    # add sources and sinks depending on items in energy providers as pre-processing
    for asset in dict_values[group]:
        define_dso_sinks_and_sources(dict_values, asset)

        # Add lifetime capex (incl. replacement costs), calculate annuity
        # (incl. om), and simulation annuity to each asset
        define_missing_cost_data(dict_values, dict_values[group][asset])
        evaluate_lifetime_costs(
            dict_values[SIMULATION_SETTINGS],
            dict_values[ECONOMIC_DATA],
            dict_values[group][asset],
        )


def energyConsumption(dict_values, group):
    """

    :param dict_values:
    :param group:
    :return:
    """
    for asset in dict_values[group]:
        define_missing_cost_data(dict_values, dict_values[group][asset])
        evaluate_lifetime_costs(
            dict_values[SIMULATION_SETTINGS],
            dict_values[ECONOMIC_DATA],
            dict_values[group][asset],
        )
        if INPUT_BUS_NAME not in dict_values[group][asset]:
            dict_values[group][asset].update(
                {INPUT_BUS_NAME: bus_suffix(dict_values[group][asset][ENERGY_VECTOR])}
            )

        if FILENAME in dict_values[group][asset]:
            receive_timeseries_from_csv(
                dict_values[SIMULATION_SETTINGS],
                dict_values[group][asset],
                "input",
                is_demand_profile=True,
            )
        else:
            logging.debug(
                f"Not loading {group} asset {asset} from a file, timeseries is provided"
            )
            compute_timeseries_properties(dict_values[group][asset])


def define_missing_cost_data(dict_values, dict_asset):
    """

    :param dict_values:
    :param dict_asset:
    :return:
    """

    # read timeseries with filename provided for variable costs.
    # if multiple dispatch_price are given for multiple busses, it checks if any v
    # alue is a timeseries
    if DISPATCH_PRICE in dict_asset:
        if isinstance(dict_asset[DISPATCH_PRICE][VALUE], dict):
            receive_timeseries_from_csv(
                dict_values[SIMULATION_SETTINGS], dict_asset, DISPATCH_PRICE,
            )
        elif isinstance(dict_asset[DISPATCH_PRICE][VALUE], list):
            treat_multiple_flows(dict_asset, dict_values, DISPATCH_PRICE)

    economic_data = dict_values[ECONOMIC_DATA]

    basic_costs = {
        OPTIMIZE_CAP: {VALUE: False, UNIT: TYPE_BOOL},
        UNIT: "?",
        INSTALLED_CAP: {VALUE: 0.0, UNIT: UNIT},
        DEVELOPMENT_COSTS: {VALUE: 0, UNIT: CURR},
        SPECIFIC_COSTS: {VALUE: 0, UNIT: CURR + "/" + UNIT},
        SPECIFIC_COSTS_OM: {VALUE: 0, UNIT: CURR + "/" + UNIT_YEAR},
        DISPATCH_PRICE: {VALUE: 0, UNIT: CURR + "/" + UNIT + "/" + UNIT_YEAR},
        LIFETIME: {VALUE: economic_data[PROJECT_DURATION][VALUE], UNIT: UNIT_YEAR,},
        AGE_INSTALLED: {VALUE: 0, UNIT: UNIT_YEAR,},
    }

    # checks that an asset has all cost parameters needed for evaluation.
    # Adds standard values.
    str = ""
    for cost in basic_costs:
        if cost not in dict_asset:
            dict_asset.update({cost: basic_costs[cost]})
            str = str + " " + cost

    if len(str) > 1:
        logging.debug("Added basic costs to asset %s: %s", dict_asset[LABEL], str)


def define_busses(dict_values):
    """
    This function defines the ENERGY_BUSSES that the energy system model is comprised of.
    For that, it adds each new bus defined as INPUT_DIRECTION or OUTPUT_DIRECTION in all assets
    of all the energyAsset types (ENERGY_CONVERSION, ENERGY_PRODUCTION, ENERGY_CONSUMPTION, ENERGY_PROVIDERS, ENERGY_STORAGE)

    Parameters
    ----------
    dict_values: dict
        Dictionary with all simulation information

    Returns
    -------
    Extends dict_values by key "ENERGY_BUSSES" and all their names.

    """
    # create new group of assets: busses
    dict_values.update({ENERGY_BUSSES: {}})

    # Interatively adds busses to ENERGY_BUSSES for each new bus in the inflow/outflow direction of subsequent assets
    for group in [
        ENERGY_CONVERSION,
        ENERGY_PRODUCTION,
        ENERGY_CONSUMPTION,
        ENERGY_PROVIDERS,
        ENERGY_STORAGE,
    ]:
        for asset in dict_values[group]:
            add_busses_of_asset_depending_on_in_out_direction(
                dict_values, dict_values[group][asset], asset
            )


def add_busses_of_asset_depending_on_in_out_direction(
    dict_values, dict_asset, asset_key
):
    """
    Check if the INPUT_DIRECTION and OUTPUT_DIRECTION, ie the bus, of an asset is already included in energyBusses.
    Otherwise, add to dict_values(ENERGY_BUSSES).

    Translates INPUT_DIRECTION and OUTPUT_DIRECTION into INPUT_BUS_NAME and OUTPUT_BUS_NAME.

    Parameters
    ----------
    dict_values: dict
        All simulation information

    dict_asset: dict
        All information of the current asset

    asset_key: str
        Key that calls the dict_asset from dict_values[asset_group][key]

    Returns
    -------
    Updated dict_values with potentially additional busses of the energy system.
    Updated dict_asset with the input_bus_name
    """
    for direction in [INFLOW_DIRECTION, OUTFLOW_DIRECTION]:
        # This is the parameter that will be added to dict_asset as the bus_name_key
        if direction == INFLOW_DIRECTION:
            bus_name_key = INPUT_BUS_NAME
        else:
            bus_name_key = OUTPUT_BUS_NAME

        energy_vector = dict_asset[ENERGY_VECTOR]
        # Check if the asset has an INFLOW_DIRECTION or OUTFLOW_DIRECTION
        if direction in dict_asset:
            bus = dict_asset[direction]
            # Check if a list ob busses is in INFLOW_DIRECTION or OUTFLOW_DIRECTION
            if isinstance(bus, list):
                # If true: All busses need to be checked
                bus_list = []
                # Checking each bus of the list
                for subbus in bus:
                    # Append bus name to bus_list
                    bus_list.append(bus_suffix(subbus))
                    # Check if bus of the direction is already contained in energyBusses
                    update_bus(
                        bus=subbus,
                        dict_values=dict_values,
                        asset_key=asset_key,
                        asset_label=dict_asset[LABEL],
                        energy_vector=energy_vector,
                    )
                # Add bus_name_key to dict_asset
                dict_asset.update({bus_name_key: bus_list})
            # If false: Only one bus
            else:
                # Check if bus of the direction is already contained in energyBusses
                update_bus(
                    bus=bus,
                    dict_values=dict_values,
                    asset_key=asset_key,
                    asset_label=dict_asset[LABEL],
                    energy_vector=energy_vector,
                )
                # Add bus_name_key to dict_asset
                dict_asset.update({bus_name_key: bus_suffix(bus)})


def bus_suffix(bus_direction):
    """
    Returns the name of a bus with the suffix defined in constants_json_strings.py (BUS_SUFFIX)

    It is possible that the suffix will be dropped later on, in case that users always enter the directions with suffix " bus" anyway.

    Parameters
    ----------
    bus_direction: str
        A string, ie. a bus name

    Returns
    -------
    Above string with BUS_SUFFIX
    """
    bus_label = bus_direction + BUS_SUFFIX
    return bus_label


def remove_bus_suffix(bus_label):
    """
    Removes suffix from a INPUT / OUTPUT BUS LABEL to get the INPUT / OUTPUT DIRECTION.

    Parameters
    ----------
    bus_label: str
        Bus label with suffix

    Returns
    -------
    Bus direction (without suffix)
    """
    bus_direction = bus_label[: -len(BUS_SUFFIX)]
    return bus_direction


def update_bus(bus, dict_values, asset_key, asset_label, energy_vector):
    """
    Checks if an bus is already included in ENERGY_BUSSES and otherwise adds it.
    Adds asset key and label to list of assets attached to a bus.

    Parameters
    ----------
    dict_values: dict
        Dict of all simulation parameters

    bus: str
        A bus label

    asset_key: str
        Key with with an dict_asset would be called from dict_values[groups][key]

    asset_label: str
        Label of the asset

    energy_vector: str
        Energy vector of the asset
        - Output flow of an energy conversion asset (disregard energy vector if the assets inflow direction is connected to the bus)
        - Input flow of a sink
        - Output flow of a source
        - Energy vector of a storage

    Returns
    -------
    Updated dict_values[ENERGY_BUSSES], optionally with new busses and/or by adding an asset to a bus

    EnergyBusses now has following keys: LABEL, ENERGY_VECTOR, ASSET_DICT
    """
    bus_label = bus_suffix(bus)

    if bus_label not in dict_values[ENERGY_BUSSES]:
        # add bus to asset group energyBusses
        dict_values[ENERGY_BUSSES].update(
            {
                bus_label: {
                    LABEL: bus_label,
                    ENERGY_VECTOR: energy_vector,
                    ASSET_DICT: {},
                }
            }
        )

    else:
        if dict_values[ENERGY_BUSSES][bus_label][ENERGY_VECTOR] is None:
            dict_values[ENERGY_BUSSES][bus_label].update({ENERGY_VECTOR: energy_vector})

    # Asset should added to respective bus
    dict_values[ENERGY_BUSSES][bus_label][ASSET_DICT].update({asset_key: asset_label})
    logging.debug("Added asset %s to bus %s", asset_label, bus_label)


def define_dso_sinks_and_sources(dict_values, dso):
    r"""
    Defines all sinks and sources that need to be added to model the transformer using assets of energyConsumption, energyProduction and energyConversion.

    Parameters
    ----------
    dict_values
    dso

    Returns
    -------
    Updated dict_values
    """

    number_of_pricing_periods = dict_values[ENERGY_PROVIDERS][dso][
        PEAK_DEMAND_PRICING_PERIOD
    ][VALUE]

    months_in_a_period = determine_months_in_a_peak_demand_pricing_period(
        number_of_pricing_periods,
        dict_values[SIMULATION_SETTINGS][EVALUATED_PERIOD][VALUE],
    )

    dict_availability_timeseries = define_availability_of_peak_demand_pricing_assets(
        dict_values, number_of_pricing_periods, months_in_a_period,
    )

    list_of_dso_energyConversion_assets = add_a_transformer_for_each_peak_demand_pricing_period(
        dict_values, dict_values[ENERGY_PROVIDERS][dso], dict_availability_timeseries,
    )

    define_source(
        dict_values=dict_values,
        asset_key=dso + DSO_CONSUMPTION,
        output_bus_direction=dict_values[ENERGY_PROVIDERS][dso][OUTFLOW_DIRECTION]
        + DSO_PEAK_DEMAND_BUS_NAME,
        price=dict_values[ENERGY_PROVIDERS][dso][ENERGY_PRICE],
        energy_vector=dict_values[ENERGY_PROVIDERS][dso][ENERGY_VECTOR],
    )

    # define feed-in sink of the DSO
    define_sink(
        dict_values=dict_values,
        asset_name=dso + DSO_FEEDIN + AUTO_SINK,
        price=dict_values[ENERGY_PROVIDERS][dso][FEEDIN_TARIFF],
        input_bus_name=dict_values[ENERGY_PROVIDERS][dso][INPUT_BUS_NAME],
        specific_costs={VALUE: 0, UNIT: CURR + "/" + UNIT},
        energy_vector=dict_values[ENERGY_PROVIDERS][dso][ENERGY_VECTOR],
    )

    dict_values[ENERGY_PROVIDERS][dso].update(
        {
            CONNECTED_CONSUMPTION_SOURCE: dso + DSO_CONSUMPTION + AUTO_SOURCE,
            CONNECTED_PEAK_DEMAND_PRICING_TRANSFORMERS: list_of_dso_energyConversion_assets,
            CONNECTED_FEEDIN_SINK: dso + DSO_FEEDIN + AUTO_SINK,
        }
    )


def define_availability_of_peak_demand_pricing_assets(
    dict_values, number_of_pricing_periods, months_in_a_period
):
    r"""
    Determined the availability timeseries for the later to be defined dso assets for taking into account the peak demand pricing periods.

    Parameters
    ----------
    dict_values: dict
        All simulation inputs
    number_of_pricing_periods: int
        Number of pricing periods in a year. Valid: 1,2,3,4,6,12
    months_in_a_period: int
        Duration of a period

    Returns
    -------
    dict_availability_timeseries: dict
        Dict with all availability timeseries for each period

    """
    dict_availability_timeseries = {}
    for period in range(1, number_of_pricing_periods + 1):
        availability_in_period = pd.Series(
            0, index=dict_values[SIMULATION_SETTINGS][TIME_INDEX]
        )
        time_period = pd.date_range(
            # Period start
            start=dict_values[SIMULATION_SETTINGS][START_DATE]
            + pd.DateOffset(months=(period - 1) * months_in_a_period),
            # Period end, with months_in_a_period durartion
            end=dict_values[SIMULATION_SETTINGS][START_DATE]
            + pd.DateOffset(months=(period) * months_in_a_period, hours=-1),
            freq=str(dict_values[SIMULATION_SETTINGS][TIMESTEP][VALUE]) + UNIT_MINUTE,
        )

        availability_in_period = availability_in_period.add(
            pd.Series(1, index=time_period), fill_value=0
        )
        dict_availability_timeseries.update({period: availability_in_period})

    return dict_availability_timeseries


def add_a_transformer_for_each_peak_demand_pricing_period(
    dict_values, dict_dso, dict_availability_timeseries
):
    r"""
    Adds transformers that are supposed to model the peak_demand_pricing periods for each period.
    This is changed compared to MVS 0.3.0, as there a peak demand pricing period was added by adding a source, not a transformer.

    Parameters
    ----------
    dict_values: dict
        dict with all simulation parameters

    dict_dso: dict
        dict with all info on the specific dso at hand

    dict_availability_timeseries: dict
        dict with all availability timeseries for each period

    Returns
    -------
    list_of_dso_energyConversion_assets: list
        List of names of newly added energy conversion assets,

    Updated dict_values with a transformer for each peak demand pricing period
    """

    list_of_dso_energyConversion_assets = []
    for key in dict_availability_timeseries.keys():
        if len(dict_availability_timeseries.keys()) == 1:
            transformer_name = (
                dict_dso[LABEL] + DSO_CONSUMPTION + DSO_PEAK_DEMAND_PERIOD
            )
        else:
            transformer_name = (
                dict_dso[LABEL]
                + DSO_CONSUMPTION
                + DSO_PEAK_DEMAND_PERIOD
                + "_"
                + str(key)
            )

        define_transformer_for_peak_demand_pricing(
            dict_values=dict_values,
            dict_dso=dict_dso,
            transformer_name=transformer_name,
            timeseries_availability=dict_availability_timeseries[key],
        )

        list_of_dso_energyConversion_assets.append(transformer_name)

    logging.debug(
        f"The peak demand pricing price of {dict_dso[PEAK_DEMAND_PRICING][VALUE]} {dict_values[ECONOMIC_DATA][CURR]} "
        f"is set as specific_costs_om of the peak demand pricing transformers of the DSO."
    )
    return list_of_dso_energyConversion_assets


def determine_months_in_a_peak_demand_pricing_period(
    number_of_pricing_periods, simulation_period_lenght
):
    r"""
    Check if the number of peak demand pricing periods is valid.
    Warns user that in case the number of periods exceeds 1 but the simulation time is not a year,
    there could be an unexpected number of timeseries considered.
    Raises error if number of peak demand pricing periods is not valid.

    Parameters
    ----------
    number_of_pricing_periods: int
        Defined in csv, is number of pricing periods within a year
    simulation_period_lenght: int
        Defined in csv, is number of days of the simulation

    Returns
    -------
    months_in_a_period: float
        Number of months that make a period, will be used to determine availability of dso assets
    """

    # check number of pricing periods - if >1 the simulation has to cover a whole year!
    if number_of_pricing_periods > 1:
        if simulation_period_lenght != 365:
            logging.debug(
                f"\n Message for dev: Following warning is not technically true, "
                f"as the evaluation period has to approximately be "
                f"larger than 365/peak demand pricing periods (see #331)."
            )
            logging.warning(
                f"You have chosen a number of peak demand pricing periods > 1."
                f"Please be advised that if you are not simulating for a year (365d)"
                f"an possibly unexpected number of periods will be considered."
            )
    if number_of_pricing_periods not in [1, 2, 3, 4, 6, 12]:
        raise InvalidPeakDemandPricingPeriods(
            f"You have defined a number of peak demand pricing periods of {number_of_pricing_periods}. "
            f"Acceptable values are, however: 1 (yearly), 2 (half-yearly), 3 (each trimester), 4 (quarterly), 6 (every two months) and 1 (monthly)."
        )

    # defines the number of months that one period constists of.
    months_in_a_period = 12 / number_of_pricing_periods
    logging.info(
        "Peak demand pricing is taking place %s times per year, ie. every %s "
        "months.",
        number_of_pricing_periods,
        months_in_a_period,
    )
    return months_in_a_period


def define_transformer_for_peak_demand_pricing(
    dict_values, dict_dso, transformer_name, timeseries_availability
):
    r"""
    Defines a transformer for peak demand pricing in energyConverion

    Parameters
    ----------
    dict_values: dict
        All simulation parameters

    dict_dso: dict
        All values connected to the DSO

    transformer_name: str
        label of the transformer to be added

    timeseries_availability: pd.Series
        Timeseries of transformer availability. Introduced to cover peak demand pricing.

    Returns
    -------
    Updated dict_values with newly added transformer asset in the energyConversion asset group.
    """

    default_dso_transformer = {
        LABEL: transformer_name,
        OPTIMIZE_CAP: {VALUE: True, UNIT: TYPE_BOOL},
        INSTALLED_CAP: {VALUE: 0, UNIT: dict_dso[UNIT]},
        INFLOW_DIRECTION: dict_dso[INFLOW_DIRECTION] + DSO_PEAK_DEMAND_BUS_NAME,
        INPUT_BUS_NAME: bus_suffix(
            dict_dso[INFLOW_DIRECTION] + DSO_PEAK_DEMAND_BUS_NAME
        ),
        OUTFLOW_DIRECTION: dict_dso[OUTFLOW_DIRECTION],
        OUTPUT_BUS_NAME: bus_suffix(dict_dso[OUTFLOW_DIRECTION]),
        AVAILABILITY_DISPATCH: timeseries_availability,
        EFFICIENCY: {VALUE: 1, UNIT: "factor"},
        DEVELOPMENT_COSTS: {VALUE: 0, UNIT: CURR},
        SPECIFIC_COSTS: {VALUE: 0, UNIT: CURR + "/" + dict_dso[UNIT],},
        SPECIFIC_COSTS_OM: {
            VALUE: dict_dso[PEAK_DEMAND_PRICING][VALUE],
            UNIT: CURR + "/" + dict_dso[UNIT] + "/" + UNIT_YEAR,
        },
        DISPATCH_PRICE: {VALUE: 0, UNIT: CURR + "/" + dict_dso[UNIT] + "/" + UNIT_HOUR},
        OEMOF_ASSET_TYPE: OEMOF_TRANSFORMER,
        ENERGY_VECTOR: dict_dso[ENERGY_VECTOR],
        AGE_INSTALLED: {VALUE: 0, UNIT: UNIT_YEAR},
    }

    dict_values[ENERGY_CONVERSION].update({transformer_name: default_dso_transformer})

    logging.debug(
        f"Model for peak demand pricing: Adding transfomer {transformer_name}."
    )


def define_source(
    dict_values, asset_key, output_bus_direction, energy_vector, **kwargs
):
    r"""
    Defines a source with default input values. If kwargs are given, the default values are overwritten.

    Parameters
    ----------
    dict_values: dict
        Dictionary to which source should be added, with all simulation parameters

    asset_key: str
        key under which the asset is stored in the asset group

    energy_vector: str
        Energy vector the new asset should belong to

    kwargs: Misc.
        Kwargs that can overwrite the default values.
        Typical kwargs:
            - TIMESERIES
            - SPECIFIC_COSTS_OM
            - SPECIFIC_COSTS
            - "price"

    Returns
    -------
    Standard source defined as:
    """

    output_bus_name = get_name_or_names_of_in_or_output_bus(output_bus_direction)

    default_source_dict = {
        OEMOF_ASSET_TYPE: OEMOF_SOURCE,
        LABEL: asset_key + AUTO_SOURCE,
        OUTFLOW_DIRECTION: output_bus_direction,
        OUTPUT_BUS_NAME: output_bus_name,
        DISPATCHABILITY: True,
        # OPEX_VAR: {VALUE: price, UNIT: CURR + "/" + UNIT},
        LIFETIME: {
            VALUE: dict_values[ECONOMIC_DATA][PROJECT_DURATION][VALUE],
            UNIT: UNIT_YEAR,
        },
        OPTIMIZE_CAP: {VALUE: True, UNIT: TYPE_BOOL},
        MAXIMUM_CAP: {VALUE: None, UNIT: "?"},
        AGE_INSTALLED: {VALUE: 0, UNIT: UNIT_YEAR,},
        ENERGY_VECTOR: energy_vector,
    }

    for item in kwargs:
        if item in [SPECIFIC_COSTS_OM, SPECIFIC_COSTS]:
            default_source_dict.update({item: kwargs[item]})
        if item == TIMESERIES:
            default_source_dict.update({DISPATCHABILITY: False})
            logging.debug(
                f"{default_source_dict[LABEL]} can provide a total generation of {sum(kwargs[TIMESERIES].values)}"
            )
            default_source_dict.update(
                {
                    OPTIMIZE_CAP: {VALUE: True, UNIT: TYPE_BOOL},
                    TIMESERIES_PEAK: {VALUE: max(kwargs[TIMESERIES]), UNIT: "kW"},
                    # todo if we have normalized timeseries hiere, the capex/opex (simulation) have changed, too
                    TIMESERIES_NORMALIZED: kwargs[TIMESERIES] / max(kwargs[TIMESERIES]),
                }
            )
        if item == "price":
            if FILENAME in kwargs[item] and HEADER in kwargs[item]:
                kwargs[item].update(
                    {
                        VALUE: get_timeseries_multiple_flows(
                            dict_values[SIMULATION_SETTINGS],
                            default_source_dict,
                            kwargs[item][FILENAME],
                            kwargs[item][HEADER],
                        )
                    }
                )
            determine_dispatch_price(dict_values, kwargs[item], default_source_dict)

    dict_values[ENERGY_PRODUCTION].update({asset_key: default_source_dict})

    logging.info(
        f"Asset {default_source_dict[LABEL]} was added to the energyProduction assets."
    )

    apply_function_to_single_or_list(
        function=update_bus,
        parameter=output_bus_direction,
        dict_values=dict_values,
        asset_key=asset_key,
        asset_label=default_source_dict[LABEL],
        energy_vector=energy_vector,
    )


def get_name_or_names_of_in_or_output_bus(bus):
    """
    Returns the bus names of one or multiple in- or output busses.

    Parameters
    ----------
    bus: str
        A bus name without bus suffix

    Returns
    -------
    Bus name with suffix
    """
    if isinstance(bus, list):
        bus_name = []
        for bus_item in bus:
            bus_name.append(bus_suffix(bus_item))
    else:
        bus_name = bus_suffix(bus)
    return bus_name


def determine_dispatch_price(dict_values, price, source):
    # check if multiple busses are provided
    # for each bus, read time series for dispatch_price if a file name has been
    # provided in energy price
    if isinstance(price[VALUE], list):
        source.update({DISPATCH_PRICE: {VALUE: [], UNIT: price[UNIT]}})
        values_info = []
        for element in price[VALUE]:
            if isinstance(element, dict):
                source[DISPATCH_PRICE][VALUE].append(
                    get_timeseries_multiple_flows(
                        dict_values[SIMULATION_SETTINGS],
                        source,
                        element[FILENAME],
                        element[HEADER],
                    )
                )
                values_info.append(element)
            else:
                source[DISPATCH_PRICE][VALUE].append(element)
        if len(values_info) > 0:
            source[DISPATCH_PRICE]["values_info"] = values_info

    elif isinstance(price[VALUE], dict):
        source.update(
            {
                DISPATCH_PRICE: {
                    VALUE: {
                        FILENAME: price[VALUE][FILENAME],
                        HEADER: price[VALUE][HEADER],
                    },
                    UNIT: price[UNIT],
                }
            }
        )
        receive_timeseries_from_csv(
            dict_values[SIMULATION_SETTINGS], source, DISPATCH_PRICE
        )
    else:
        source.update({DISPATCH_PRICE: {VALUE: price[VALUE], UNIT: price[UNIT]}})

    if type(source[DISPATCH_PRICE][VALUE]) == pd.Series:
        logging.debug(
            f"{source[LABEL]} was created, with a price defined as a timeseries (average: {source[DISPATCH_PRICE][VALUE].mean()})."
        )
    else:
        logging.debug(
            f"{source[LABEL]} was created, with a price of {source[DISPATCH_PRICE][VALUE]}."
        )


def define_sink(
    dict_values, asset_name, price, input_bus_name, energy_vector, **kwargs
):
    r"""
    This automatically defines a sink for an oemof-sink object. The sinks are added to the energyConsumption assets.

    Parameters
    ----------
    dict_values: dict
        All information of the simulation

    asset_name: str
        label of the asset to be generated

    price: float
        Price of dispatch of the asset

    input_direction: str
        Direction from which energy is provided to the sink, used to create inbut bus name

    kwargs: Misc
        Common parameters:
        -

    Returns
    -------
    Updates dict_values[ENERGY_CONSUMPTION] with a new sink

    Notes
    -----
    Examples:
    - Used to define excess sinks for all energyBusses
    - Used to define feed-in sink for each DSO
    """

    # create name of bus. Check if multiple busses are given
    input_direction = remove_bus_suffix(input_bus_name)

    # create a dictionary for the sink
    sink = {
        OEMOF_ASSET_TYPE: OEMOF_SINK,
        LABEL: asset_name + AUTO_SINK,
        INFLOW_DIRECTION: input_direction,
        INPUT_BUS_NAME: input_bus_name,
        # OPEX_VAR: {VALUE: price, UNIT: CURR + "/" + UNIT},
        LIFETIME: {
            VALUE: dict_values[ECONOMIC_DATA][PROJECT_DURATION][VALUE],
            UNIT: UNIT_YEAR,
        },
        AGE_INSTALLED: {VALUE: 0, UNIT: UNIT_YEAR,},
        ENERGY_VECTOR: energy_vector,
        OPTIMIZE_CAP: {VALUE: True, UNIT: TYPE_BOOL},
    }

    if energy_vector is None:
        raise ValueError(
            f"The {ENERGY_VECTOR} of the automatically defined sink {asset_name+AUTO_SINK} is invalid: {energy_vector}."
        )

    # check if multiple busses are provided
    # for each bus, read time series for dispatch_price if a file name has been provided in feedin tariff
    if isinstance(price[VALUE], list):
        sink.update({DISPATCH_PRICE: {VALUE: [], UNIT: price[UNIT]}})
        values_info = []
        for element in price[VALUE]:
            if isinstance(element, dict):
                timeseries = get_timeseries_multiple_flows(
                    dict_values[SIMULATION_SETTINGS],
                    sink,
                    element[FILENAME],
                    element[HEADER],
                )
                if asset_name[-6:] == "feedin":
                    sink[DISPATCH_PRICE][VALUE].append([-i for i in timeseries])
                else:
                    sink[DISPATCH_PRICE][VALUE].append(timeseries)
            else:
                sink[DISPATCH_PRICE][VALUE].append(element)
        if len(values_info) > 0:
            sink[DISPATCH_PRICE]["values_info"] = values_info

    elif isinstance(price[VALUE], dict):
        sink.update(
            {
                DISPATCH_PRICE: {
                    VALUE: {
                        FILENAME: price[VALUE][FILENAME],
                        HEADER: price[VALUE][HEADER],
                    },
                    UNIT: price[UNIT],
                }
            }
        )
        receive_timeseries_from_csv(
            dict_values[SIMULATION_SETTINGS], sink, DISPATCH_PRICE
        )
        if (
            asset_name[-6:] == "feedin"
        ):  # change into negative value if this is a feedin sink
            sink[DISPATCH_PRICE].update(
                {VALUE: [-i for i in sink[DISPATCH_PRICE][VALUE]]}
            )
    else:
        if asset_name[-6:] == "feedin":
            value = -price[VALUE]
        else:
            value = price[VALUE]
        sink.update({DISPATCH_PRICE: {VALUE: value, UNIT: price[UNIT]}})

    for item in [SPECIFIC_COSTS, SPECIFIC_COSTS_OM]:
        if item in kwargs:
            sink.update(
                {item: kwargs[item],}
            )

    # update dictionary
    dict_values[ENERGY_CONSUMPTION].update({asset_name: sink})

    # If multiple input busses exist
    apply_function_to_single_or_list(
        function=update_bus,
        parameter=input_direction,
        dict_values=dict_values,
        asset_key=asset_name,
        asset_label=sink[LABEL],
        energy_vector=energy_vector,
    )


def apply_function_to_single_or_list(function, parameter, **kwargs):
    """
    Applies function to a paramter or to a list of parameters and returns resut

    Parameters
    ----------
    function: func
        Function to be applied to a parameter

    parameter: float/str/boolean or list
        Parameter, either float/str/boolean or list to be evaluated
    kwargs
        Miscellaneous arguments for function to be called

    Returns
    -------
    Processed parameter (single) or list of processed para<meters
    """
    if isinstance(parameter, list):
        parameter_processed = []
        for parameter_item in parameter:
            parameter_processed.append(function(parameter_item, **kwargs))
    else:
        parameter_processed = function(parameter, **kwargs)

    return parameter_processed


def evaluate_lifetime_costs(settings, economic_data, dict_asset):
    r"""
    Evaluates specific costs of an asset over the project lifetime. This includes:
    - LIFETIME_PRICE_DISPATCH (C2.determine_lifetime_price_dispatch)
    - LIFETIME_SPECIFIC_COST
    - LIFETIME_SPECIFIC_COST_OM
    - ANNUITY_SPECIFIC_INVESTMENT_AND_OM
    - SIMULATION_ANNUITY

    The DEVELOPMENT_COSTS are not processed here, as they are not necessary for the optimization.

    Parameters
    ----------
    settings: dict
        dict of simulation settings, including:
        - EVALUATED_PERIOD

    economic_data: dict
        dict of economic data of the simulation, including
        - project duration (PROJECT_DURATION)
        - discount factor (DISCOUNTFACTOR)
        - tax (TAX)
        - CRF
        - ANNUITY_FACTOR

    dict_asset: dict
        dict of all asset parameters, including
        - SPECIFIC_COSTS
        - SPECIFIC_COSTS_OM
        - LIFETIME

    Returns
    -------
    Updates asset dict with
    - LIFETIME_PRICE_DISPATCH (C2.determine_lifetime_price_dispatch)
    - LIFETIME_SPECIFIC_COST
    - LIFETIME_SPECIFIC_COST_OM
    - ANNUITY_SPECIFIC_INVESTMENT_AND_OM
    - SIMULATION_ANNUITY
    - SPECIFIC_REPLACEMENT_COSTS_INSTALLED
    - SPECIFIC_REPLACEMENT_COSTS_OPTIMIZED
    Notes
    -----

    Tested with:
    - test_evaluate_lifetime_costs_adds_all_parameters()
    - Test_Economic_KPI.test_benchmark_Economic_KPI_C2_E2()

    """

    C2.determine_lifetime_price_dispatch(dict_asset, economic_data)

    (
        specific_capex,
        specific_replacement_costs_optimized,
        specific_replacement_costs_already_installed,
    ) = C2.capex_from_investment(
        investment_t0=dict_asset[SPECIFIC_COSTS][VALUE],
        lifetime=dict_asset[LIFETIME][VALUE],
        project_life=economic_data[PROJECT_DURATION][VALUE],
        discount_factor=economic_data[DISCOUNTFACTOR][VALUE],
        tax=economic_data[TAX][VALUE],
        age_of_asset=dict_asset[AGE_INSTALLED][VALUE],
    )

    dict_asset.update(
        {
            LIFETIME_SPECIFIC_COST: {
                VALUE: specific_capex,
                UNIT: dict_asset[SPECIFIC_COSTS][UNIT],
            }
        }
    )

    dict_asset.update(
        {
            SPECIFIC_REPLACEMENT_COSTS_OPTIMIZED: {
                VALUE: specific_replacement_costs_optimized,
                UNIT: dict_asset[SPECIFIC_COSTS][UNIT],
            }
        }
    )

    dict_asset.update(
        {
            SPECIFIC_REPLACEMENT_COSTS_INSTALLED: {
                VALUE: specific_replacement_costs_already_installed,
                UNIT: dict_asset[SPECIFIC_COSTS][UNIT],
            }
        }
    )

    # Annuities of components including opex AND capex #
    dict_asset.update(
        {
            ANNUITY_SPECIFIC_INVESTMENT_AND_OM: {
                VALUE: C2.annuity(
                    dict_asset[LIFETIME_SPECIFIC_COST][VALUE],
                    economic_data[CRF][VALUE],
                )
                + dict_asset[SPECIFIC_COSTS_OM][VALUE],  # changes from dispatch_price
                UNIT: dict_asset[LIFETIME_SPECIFIC_COST][UNIT] + "/" + UNIT_YEAR,
            }
        }
    )

    dict_asset.update(
        {
            LIFETIME_SPECIFIC_COST_OM: {
                VALUE: dict_asset[SPECIFIC_COSTS_OM][VALUE]
                * economic_data[ANNUITY_FACTOR][VALUE],
                UNIT: dict_asset[SPECIFIC_COSTS_OM][UNIT][:-2],
            }
        }
    )

    dict_asset.update(
        {
            SIMULATION_ANNUITY: {
                VALUE: C2.simulation_annuity(
                    dict_asset[ANNUITY_SPECIFIC_INVESTMENT_AND_OM][VALUE],
                    settings[EVALUATED_PERIOD][VALUE],
                ),
                UNIT: CURR + "/" + UNIT + "/" + EVALUATED_PERIOD,
            }
        }
    )


# read timeseries. 2 cases are considered: Input type is related to demand or generation profiles,
# so additional values like peak, total or average must be calculated. Any other type does not need this additional info.
def receive_timeseries_from_csv(
    settings, dict_asset, input_type, is_demand_profile=False
):
    """

    :param settings:
    :param dict_asset:
    :param type:
    :return:
    """
    if input_type == "input" and "input" in dict_asset:
        file_name = dict_asset[input_type][FILENAME]
        header = dict_asset[input_type][HEADER]
        unit = dict_asset[input_type][UNIT]
    elif FILENAME in dict_asset:
        # todo this input/file_name thing is a workaround and has to be improved in the future
        # if only filename is given here, then only one column can be in the csv
        file_name = dict_asset[FILENAME]
        unit = dict_asset[UNIT] + "/" + UNIT_HOUR
    else:
        file_name = dict_asset[input_type][FILENAME]
        header = dict_asset[input_type][HEADER]
        unit = dict_asset[input_type][UNIT]

    file_path = os.path.join(settings[PATH_INPUT_FOLDER], TIME_SERIES, file_name)
    C1.lookup_file(file_path, dict_asset[LABEL])

    data_set = pd.read_csv(file_path, sep=",")

    if FILENAME in dict_asset:
        header = data_set.columns[0]

    if len(data_set.index) == settings[PERIODS]:
        if input_type == "input":
            dict_asset.update(
                {
                    TIMESERIES: pd.Series(
                        data_set[header].values, index=settings[TIME_INDEX]
                    )
                }
            )
        else:
            dict_asset[input_type][VALUE] = pd.Series(
                data_set[header].values, index=settings[TIME_INDEX]
            )

        logging.debug("Added timeseries of %s (%s).", dict_asset[LABEL], file_path)
    elif len(data_set.index) >= settings[PERIODS]:
        if input_type == "input":
            dict_asset.update(
                {
                    TIMESERIES: pd.Series(
                        data_set[header][0 : len(settings[TIME_INDEX])].values,
                        index=settings[TIME_INDEX],
                    )
                }
            )
        else:
            dict_asset[input_type][VALUE] = pd.Series(
                data_set[header][0 : len(settings[TIME_INDEX])].values,
                index=settings[TIME_INDEX],
            )

        logging.info(
            "Provided timeseries of %s (%s) longer than evaluated period. "
            "Excess data dropped.",
            dict_asset[LABEL],
            file_path,
        )

    elif len(data_set.index) <= settings[PERIODS]:
        logging.critical(
            "Input error! "
            "Provided timeseries of %s (%s) shorter then evaluated period. "
            "Operation terminated",
            dict_asset[LABEL],
            file_path,
        )
        sys.exit()

    if input_type == "input":
        compute_timeseries_properties(dict_asset)


def compute_timeseries_properties(dict_asset):
    """Compute peak, aggregation, average and normalize timeseries

    Parameters
    ----------
    dict_asset: dict
        dict of all asset parameters, must contain TIMESERIES key

    Returns
    -------
    None
    Add TIMESERIES_PEAK, TIMESERIES_TOTAL, TIMESERIES_AVERAGE and TIMESERIES_NORMALIZED
    to dict_asset

    """

    if TIMESERIES in dict_asset:
        timeseries = dict_asset[TIMESERIES]
        unit = dict_asset[UNIT]

        dict_asset.update(
            {
                TIMESERIES_PEAK: {VALUE: max(timeseries), UNIT: unit,},
                TIMESERIES_TOTAL: {VALUE: sum(timeseries), UNIT: unit,},
                TIMESERIES_AVERAGE: {
                    VALUE: sum(timeseries) / len(timeseries),
                    UNIT: unit,
                },
            }
        )

        logging.debug("Normalizing timeseries of %s.", dict_asset[LABEL])
        dict_asset.update(
            {TIMESERIES_NORMALIZED: timeseries / dict_asset[TIMESERIES_PEAK][VALUE]}
        )
        # just to be sure!
        if any(dict_asset[TIMESERIES_NORMALIZED].values) > 1:
            logging.error(
                f"{dict_asset[LABEL]} normalized timeseries has values greater than 1."
            )
        if any(dict_asset[TIMESERIES_NORMALIZED].values) < 0:
            logging.error(
                f"{ dict_asset[LABEL]} normalized timeseries has negative values."
            )


def treat_multiple_flows(dict_asset, dict_values, parameter):
    """
    This function consider the case a technical parameter on the json file has a list of values because multiple
    inputs or outputs busses are considered.
    Parameters
    ----------
    dict_values:
    dictionary of current values of the asset
    parameter:
    usually efficiency. Different efficiencies will be given if an asset has multiple inputs or outputs busses,
    so a list must be considered.

    Returns
    -------

    """
    updated_values = []
    values_info = (
        []
    )  # filenames and headers will be stored to allow keeping track of the timeseries generation
    for element in dict_asset[parameter][VALUE]:
        if isinstance(element, dict):
            updated_values.append(
                get_timeseries_multiple_flows(
                    dict_values[SIMULATION_SETTINGS],
                    dict_asset,
                    element[FILENAME],
                    element[HEADER],
                )
            )
            values_info.append(element)
        else:
            updated_values.append(element)
    dict_asset[parameter][VALUE] = updated_values
    if len(values_info) > 0:
        dict_asset[parameter].update({"values_info": values_info})


# reads timeseries specifically when the need comes from a multiple or output busses situation
# returns the timeseries. Does not update any dictionary
def get_timeseries_multiple_flows(settings, dict_asset, file_name, header):
    """

    Parameters
    ----------
    dict_asset:
    dictionary of the asset
    file_name:
    name of the file to read the time series
    header:
    name of the column where the timeseries is provided

    Returns
    -------

    """
    file_path = os.path.join(settings[PATH_INPUT_FOLDER], TIME_SERIES, file_name)
    C1.lookup_file(file_path, dict_asset[LABEL])

    data_set = pd.read_csv(file_path, sep=",")
    if len(data_set.index) == settings[PERIODS]:
        return pd.Series(data_set[header].values, index=settings[TIME_INDEX])
    elif len(data_set.index) >= settings[PERIODS]:
        return pd.Series(
            data_set[header][0 : len(settings[TIME_INDEX])].values,
            index=settings[TIME_INDEX],
        )
    elif len(data_set.index) <= settings[PERIODS]:
        logging.critical(
            "Input error! "
            "Provided timeseries of %s (%s) shorter then evaluated period. "
            "Operation terminated",
            dict_asset[LABEL],
            file_path,
        )
        sys.exit()


def process_maximum_cap_constraint(dict_values, group, asset, subasset=None):
    """
    Checks if maximumCap is in `dict_values` and if not, adds value None.

    Parameters
    ----------
    dict_values: dict
        dictionary of all assets

    group: str
        Group that the asset belongs to (str). Used to acces sub-asset data and for error messages.

    asset: str
        asset name

    subasset: str
        subasset name.
        Default: None.

    Returns
    -------
    Updates the asset dictionary.

    * Unit of MaximumCap is asset unit

    If MaximumCap is changed depends on its value:
    * If MaximumCap not in asset dict: MaximumCap is None
    * If MaximumCap < installed Cap: invalid, MaximumCap is None
    * If MaximumCap == 0: invalid, MaximumCap is None
    * If MaximumCap > installedCap and group != energyProviders: pass
    * If MaximumCap > installedCap and group == energyProviders and filename not in asset_dict: pass
    * If MaximumCap > installedCap and group == energyProviders and filename in asset_dict (non-dispatchable assets): MaximumCap == MaximumCap/peak(timeseries)
    """
    if subasset is None:
        asset_dict = dict_values[group][asset]
    else:
        asset_dict = dict_values[group][asset][subasset]

    # Check if a maximumCap is defined
    if MAXIMUM_CAP not in asset_dict:
        asset_dict.update({MAXIMUM_CAP: {VALUE: None}})
    else:
        if asset_dict[MAXIMUM_CAP][VALUE] is not None:
            # adapt maximumCap of non-dispatchable sources
            if group == ENERGY_PRODUCTION and asset_dict[FILENAME] is not None:
                asset_dict[MAXIMUM_CAP][VALUE] = (
                    asset_dict[MAXIMUM_CAP][VALUE] * asset_dict[TIMESERIES_PEAK][VALUE]
                )
                logging.debug(
                    f"Parameter {MAXIMUM_CAP} of asset '{asset_dict[LABEL]}' was multiplied by the peak value of {TIMESERIES}. This was done as the aimed constraint is to limit the power, not the flow."
                )
            # check if maximumCap is greater that installedCap
            if asset_dict[MAXIMUM_CAP][VALUE] < asset_dict[INSTALLED_CAP][VALUE]:
                message = (
                    f"The stated maximumCap in {group} {asset} is smaller than the "
                    "installedCap. Please enter a greater maximumCap."
                    "For this simulation, the maximumCap will be "
                    "disregarded and not be used in the simulation"
                )
                warnings.warn(UserWarning(message))
                logging.warning(message)
                asset_dict[MAXIMUM_CAP][VALUE] = None
            # check if maximumCap is 0
            elif asset_dict[MAXIMUM_CAP][VALUE] == 0:
                message = (
                    f"The stated maximumCap of zero in {group} {asset} is invalid."
                    "For this simulation, the maximumCap will be "
                    "disregarded and not be used in the simulation."
                )
                warnings.warn(UserWarning(message))
                logging.warning(message)
                asset_dict[MAXIMUM_CAP][VALUE] = None

    asset_dict[MAXIMUM_CAP].update({UNIT: asset_dict[UNIT]})
