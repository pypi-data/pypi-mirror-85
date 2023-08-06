# Built-in Modules
import re
import os
import logging
from datetime import timedelta, datetime

# Third Party Modules
from astral import Observer
from astral import sun
import pandas as pd
from pytz import timezone


def get_sun_elevation(ts):
    """
    :param ts:
    :return: The sun elevation for a given timestamp
    """
    # Default to the location of the St Lucia Campus
    # TODO: These coords should be pulled from the DB
    #  (integrate into dre-database-api)
    long = 153.014008
    lat = -27.497999
    observer = Observer(lat, long)
    return sun.elevation(observer, pd.to_datetime(ts))


def is_public_holiday(dt, hols):
    """
    :param dt Localized datetime numpy datetime64
    :param hols List of dates of public holidays
    :return: 1 if the date exists in the list of holidays
    """
    return 1 if dt.date() in hols else 0


def is_working_hours(dt):
    """
    :param dt Localized datetime numpy datetime64
    :return: 1 or 0 depending on working hours threshold
    """
    return 1 if 7 < dt.hour < 18 else 0


def get_dow(dt):
    """
    :param dt Localized datetime numpy datetime64
    :return: Day of the week
    """
    return dt.dayofweek()


def get_hod(dt):
    """
    :param dt Localized datetime numpy datetime64
    :return: Hour of the day (rounded to nearest 30 min)
    """
    return float(dt.hour + (30 * round(dt.minute*2.0/30)/2.0)/60)


def is_weekend(dt):
    return 1 if 5 <= dt.weekday() <= 6 else 0


def get_time_related_timeseries(config, idx, hols):
    features_df = None
    if config is None:
        return features_df
    features_df = pd.DataFrame(index = idx)
    # Initialize Supported timeseries
    features = {name: [] for name in config}
    for ts in features_df.index:
        dt = pd.to_datetime(ts, timezone('UTC'))\
            .astimezone(timezone('Australia/Brisbane'))
        if "sunElevation" in features:
            features['sunElevation'].append(get_sun_elevation(ts))
        if "daylight" in features:
            features['daylight'].append(1 if get_sun_elevation(dt) > 0 else 0)
        if "publicHoliday":
            features['publicHoliday'].append(is_public_holiday(dt, hols))
        if "weekend":
            features['weekend'].append(is_weekend(dt))
        if "workingHours":
            features['workingHours'].append(is_working_hours(dt))
        if "dow":
            features['weekend'].append(get_dow(dt))
        if "hod":
            features['weekend'].append(get_hod(dt))
    # Fill out the dataframe
    for name, values in features.items():
        features_df[name] = values
    return features_df
