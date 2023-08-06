"""
    Geo-Instruments
    Sitecheck Scanner
    Data handler Package for Scanner

"""
import json
import logging
import os
from pathlib import Path

from . import options
from . import utlis

logger = logging.getLogger('data')


def check_mode(sensor: object) -> object:
    """
    Pauses run to give observer the chance to look at the information before proceeding.

    :return: Wait for input
    :rtype: object
    """
    return
    if os.environ['Repl']:
        logger.log(f'{sensor} is missing data')
        return input(
            "Pausing run for eval.\nPress Enter to continue...")


async def watchdog_handler(diff, project_name, sensor, last_updated):
    """
    Handles sorting sensor watchdog status.

    Timeesamps from last update are sorted into three categories:
    Up-to-date, Behind, Old

    :param diff: Time since last reading
    :type diff: int

    :param project_name: Name of Project
    :type project_name: str

    :param sensor: Sensor ID
    :type sensor: str

    :param last_updated: Formatted Date string
    :type last_updated: str
    """
    # Sensor is Up-to-date.
    if diff <= options.Watchdog:
        data_list = [
            project_name,
            sensor,
            last_updated
            ]
        if options.PrintNew:
            logger.info(data_list)
            store(project_name, data_list)
        else:
            logger.debug(data_list)

    # Sensor is Behind.
    elif options.Watchdog <= diff <= options.Oldperiod:
        data_list = [
            project_name,
            sensor,
            'Older than %s hours' % options.args.time,
            f"Time since: {convert(diff)}",
            f"Last update: {last_updated}"
            ]
        store(project_name, data_list)
        logger.info(data_list)
        check_mode(sensor)
    # Sensor is Old. Assumes after a week that this is a known issue.
    else:
        data_list = [
            project_name,
            sensor,
            'Older than a week',
            convert(diff),
            last_updated
            ]
        if options.PrintOld:
            logger.info(data_list)
            store(project_name, data_list)
            # check_mode(sensor)
        else:
            logger.debug(data_list)


def store(project, data_list):
    """
    Sensor Data storage function

    :param project:	Project name
    :type project: str

    :param data_list: Sensor data in list format
                Examples: ['IP2', 'Okay', '2020-01-16 08:00:00']
    :type data_list: list

    :rtype: None
    """
    if os.environ['SCANNER_OUTPUT_TYPE'] == 'file':
        store_path = Path(f"{os.environ['Output']}"
                          f"//data"
                          f"//{os.environ['filedate']}"
                          f"//{project}.txt")
        utlis.ensure_exists(store_path)
        with open(store_path, 'a') as file:
            if not file.tell():
                file.write('[')
            else:
                file.write(',')
            file.write(json.dumps(data_list))
    elif os.environ['SCANNER_OUTPUT_TYPE'] == 'mqtt':
        utlis.post(project, data_list)
    else:
        print(project, data_list)


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)
