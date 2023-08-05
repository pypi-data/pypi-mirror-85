"""
Module C1 is used to validate the input data compiled in A1 or read in B0.

In A1/B0, the input parameters were parsed to str/bool/float/int. This module
tests whether the parameters are in correct value ranges:
- Display error message when wrong type
- Display error message when outside defined range
- Display error message when feed-in tariff > electricity price (would cause loop, see #119)

"""

import logging
import os

import pandas as pd

from multi_vector_simulator.utils.constants import (
    PATH_INPUT_FILE,
    PATH_INPUT_FOLDER,
    PATH_OUTPUT_FOLDER,
    DISPLAY_OUTPUT,
    OVERWRITE,
)
from multi_vector_simulator.utils.constants_json_strings import (
    PROJECT_DURATION,
    DISCOUNTFACTOR,
    TAX,
    LABEL,
    CURR,
    DISPATCH_PRICE,
    SPECIFIC_COSTS_OM,
    DEVELOPMENT_COSTS,
    SPECIFIC_COSTS,
    AGE_INSTALLED,
    LIFETIME,
    INSTALLED_CAP,
    FILENAME,
    EFFICIENCY,
    EVALUATED_PERIOD,
    START_DATE,
    SOC_INITIAL,
    SOC_MAX,
    SOC_MIN,
    FEEDIN_TARIFF,
    MAXIMUM_CAP,
    SCENARIO_NAME,
    PROJECT_NAME,
    LONGITUDE,
    LATITUDE,
    PERIODS,
    COUNTRY,
    ENERGY_PRICE,
    ENERGY_PROVIDERS,
    ENERGY_PRODUCTION,
    ENERGY_BUSSES,
    VALUE,
    ASSET_DICT,
    RENEWABLE_ASSET_BOOL,
    TIMESERIES,
)


# web-application: valid input directly connected to cell-input


def lookup_file(file_path, name):
    """
    Checks whether file specified in `file_path` exists.

    If it does not exist, a FileNotFoundError is raised.

    :param file_path: File name including path of file that is checked.
    :param name: Something referring to which component the file belongs. In\
    :func:`~.CO_data_processing.get_timeseries_multiple_flows` the label of the\
    asset is used.
    :return:
    """
    if os.path.isfile(file_path) is False:
        msg = (
            f"Missing file! The timeseries file '{file_path}' \nof asset "
            + f"{name} can not be found. Operation terminated."
        )
        raise FileNotFoundError(msg)


def check_feedin_tariff(dict_values):
    r"""
    Raises error if feed-in tariff > energy price of any asset in 'energyProvider.csv'.

    Parameters
    ----------
    dict_values : dict
        Contains all input data of the simulation.

    Returns
    -------
    Indirectly, raises error message in case of feed-in tariff > energy price of any
    asset in 'energyProvider.csv'.

    """
    for provider in dict_values[ENERGY_PROVIDERS].keys():
        feedin_tariff = dict_values[ENERGY_PROVIDERS][provider][FEEDIN_TARIFF]
        electricity_price = dict_values[ENERGY_PROVIDERS][provider][ENERGY_PRICE]
        diff = feedin_tariff[VALUE] - electricity_price[VALUE]
        if isinstance(diff, float) or isinstance(diff, int):
            if diff > 0:
                msg = f"Feed-in tariff > energy price for the energy provider asset '{dict_values[ENERGY_PROVIDERS][provider][LABEL]}' would cause an unbound solution and terminate the optimization. Please reconsider your feed-in tariff and energy price."
                raise ValueError(msg)
            else:
                logging.debug(
                    f"Feed-in tariff < energy price for energy provider asset '{dict_values[ENERGY_PROVIDERS][provider][LABEL]}'"
                )
        else:
            boolean = [
                k > 0 for k in diff.values
            ]  # True if there is an instance where feed-in tariff > electricity_price
            if any(boolean) is True:
                instances = sum(boolean)  # Count instances
                msg = f"Feed-in tariff > energy price in {instances} during the simulation time for the energy provider asset '{dict_values[ENERGY_PROVIDERS][provider][LABEL]}'. This would cause an unbound solution and terminate the optimization. Please reconsider your feed-in tariff and energy price."
                raise ValueError(msg)
            else:
                logging.debug(
                    f"Feed-in tariff < energy price for energy provider asset '{dict_values[ENERGY_PROVIDERS][provider][LABEL]}'"
                )


def check_time_series_values_between_0_and_1(time_series):
    r"""
    Checks whether all values of `time_series` in [0, 1].

    Parameters
    ----------
    time_series : pd.Series
        Time series to be checked.

    Returns
    -------
    bool
        True if values of `time_series` within [0, 1], else False.

    """
    boolean = time_series.between(0, 1)

    return bool(boolean.all())


def check_non_dispatchable_source_time_series(dict_values):
    r"""
    Raises error if time series of non-dispatchable sources are not between [0, 1].

    Parameters
    ----------
    dict_values : dict
        Contains all input data of the simulation.

    Returns
    -------
    Indirectly, raises error message in case of time series of non-dispatchable sources
    not between [0, 1].

    """
    # go through all non-dispatchable sources
    for key, source in dict_values[ENERGY_PRODUCTION].items():
        if TIMESERIES in source and source[RENEWABLE_ASSET_BOOL][VALUE] is True:
            # check if values between 0 and 1
            result = check_time_series_values_between_0_and_1(
                time_series=source[TIMESERIES]
            )
            if result is False:
                logging.error(
                    f"{TIMESERIES} of non-dispatchable source {source[LABEL]} contains values out of bounds [0, 1]."
                )
                return False


def check_input_values(dict_values):
    """

    :param dict_values:
    :return:
    """
    for asset_name in dict_values:
        if not (isinstance(dict_values[asset_name], dict)):
            # checking first layer of dict_values
            all_valid_intervals(asset_name, dict_values[asset_name], "")
        else:
            # logging.debug('Asset %s checked for validation.', asset_name)
            for sub_asset_name in dict_values[asset_name]:
                if not (isinstance(dict_values[asset_name][sub_asset_name], dict)):
                    # checking second layer of dict values
                    all_valid_intervals(
                        sub_asset_name,
                        dict_values[asset_name][sub_asset_name],
                        asset_name,
                    )
                else:
                    # logging.debug('\t Sub-asset %s checked for validation.', sub_asset_name)
                    for sub_sub_asset_name in dict_values[asset_name][sub_asset_name]:
                        if not (
                            isinstance(
                                dict_values[asset_name][sub_asset_name][
                                    sub_sub_asset_name
                                ],
                                dict,
                            )
                        ):
                            # checking third layer of dict values
                            all_valid_intervals(
                                sub_sub_asset_name,
                                dict_values[asset_name][sub_asset_name][
                                    sub_sub_asset_name
                                ],
                                asset_name + sub_asset_name,
                            )
                        else:
                            # logging.debug('\t\t Sub-sub-asset %s checked for validation.', sub_sub_asset_name)
                            logging.critical(
                                "Verification Error! Add another layer to evaluation."
                            )

    logging.info(
        "Input values have been verified. This verification can not replace a manual input parameter check."
    )


def all_valid_intervals(name, value, title):
    """
    Checks whether `value` of `name` is valid.

    Checks include the expected type and the expected range a parameter is
    supposed to be inside.

    :param name:
    :param value:
    :param title:
    :return:
    """
    valid_type_string = [
        PROJECT_NAME,
        SCENARIO_NAME,
        COUNTRY,
        "parent",
        "type",
        FILENAME,
        LABEL,
        CURR,
        PATH_OUTPUT_FOLDER,
        DISPLAY_OUTPUT,
        PATH_INPUT_FILE,
        PATH_INPUT_FOLDER,
        "sector",
    ]

    valid_type_int = [EVALUATED_PERIOD, "time_step", PERIODS]

    valid_type_timestamp = [START_DATE]

    valid_type_index = ["index"]

    valid_binary = ["optimize_cap", DSM, OVERWRITE]

    valid_intervals = {
        LONGITUDE: [-180, 180],
        LATITUDE: [-90, 90],
        LIFETIME: ["largerzero", "any"],
        AGE_INSTALLED: [0, "any"],
        INSTALLED_CAP: [0, "any"],
        MAXIMUM_CAP: [0, "any", None],
        SOC_MIN: [0, 1],
        SOC_MAX: [0, 1],
        SOC_INITIAL: [0, 1],
        "crate": [0, 1],
        EFFICIENCY: [0, 1],
        "electricity_cost_fix_annual": [0, "any"],
        "electricity_price_var_kWh": [0, "any"],
        "electricity_price_var_kW_monthly": [0, "any"],
        FEEDIN_TARIFF: [0, "any"],
        DEVELOPMENT_COSTS: [0, "any"],
        SPECIFIC_COSTS: [0, "any"],
        SPECIFIC_COSTS_OM: [0, "any"],
        DISPATCH_PRICE: [0, "any"],
        DISCOUNTFACTOR: [0, 1],
        PROJECT_DURATION: ["largerzero", "any"],
        TAX: [0, 1],
    }

    if name in valid_type_int:
        if not (isinstance(value, int)):
            logging.error(
                'Input error! Value %s/%s is not in recommended format "integer".',
                name,
                title,
            )

    elif name in valid_type_string:
        if not (isinstance(value, str)):
            logging.error(
                'Input error! Value %s/%s is not in recommended format "string".',
                name,
                title,
            )

    elif name in valid_type_index:
        if not (isinstance(value, pd.DatetimeIndex)):
            logging.error(
                'Input error! Value %s/%s is not in recommended format "pd.DatetimeIndex".',
                name,
                title,
            )

    elif name in valid_type_timestamp:
        if not (isinstance(value, pd.Timestamp)):
            logging.error(
                'Input error! Value %s/%s is not in recommended format "pd.DatetimeIndex".',
                name,
                title,
            )

    elif name in valid_binary:
        if not (value is True or value is False):
            logging.error(
                "Input error! Value %s/%s is neither True nor False.", name, title
            )

    elif name in valid_intervals:
        if name == SOC_INITIAL:
            if value is not None:
                if not (0 <= value and value <= 1):
                    logging.error(
                        "Input error! Value %s/%s should be None, or between 0 and 1.",
                        name,
                        title,
                    )
        else:

            if valid_intervals[name][0] == "largerzero":
                if value <= 0:
                    logging.error(
                        "Input error! Value %s/%s can not be to be smaller or equal to 0.",
                        name,
                        title,
                    )
            elif valid_intervals[name][0] == "nonzero":
                if value == 0:
                    logging.error("Input error! Value %s/%s can not be 0.", name, title)
            elif valid_intervals[name][0] == 0:
                if value < 0:
                    logging.error(
                        "Input error! Value %s/%s has to be larger than or equal to 0.",
                        name,
                        title,
                    )

            if valid_intervals[name][1] == "any":
                pass
            elif valid_intervals[name][1] == 1:
                if 1 < value:
                    logging.error(
                        "Input error! Value %s/%s can not be larger than 1.",
                        name,
                        title,
                    )

    else:
        logging.warning(
            "VALIDATION FAILED: Code does not define a valid range for value %s/%s",
            name,
            title,
        )


def check_for_sufficient_assets_on_busses(dict_values):
    r"""
    Validating model regarding busses - each bus has to have 2+ assets connected to it, exluding energy excess sinks
    Parameters
    ----------
    dict_values: dict
        All simulation parameters

    Returns
    -------
    Logging error message if test fails
    """
    for bus in dict_values[ENERGY_BUSSES]:
        if len(dict_values[ENERGY_BUSSES][bus][ASSET_DICT]) < 3:
            asset_string = ", ".join(
                map(str, dict_values[ENERGY_BUSSES][bus][ASSET_DICT].keys())
            )
            logging.error(
                f"Energy system bus {bus} has too few assets connected to it. "
                f"The minimal number of assets that need to be connected "
                f"so that the bus is not a dead end should be two, excluding the excess sink. "
                f"These are the connected assets: {asset_string}"
            )
