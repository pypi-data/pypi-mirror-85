"""
    Geo-Instruments
    Sitecheck Scanner

    CLI entry point and function pool
"""
# __name__ = 'Scanner'
# __author__ = "Dan Edens"
# __url__= "https://geodev.geo-instruments.com/DanEdens/Sitecheck_Scanner"


import os
import sys

import paho.mqtt.client as mqtt
from ptpython.repl import embed

from sitecheck.Scanner.scanner import config
from sitecheck.Scanner.scanner import options
from sitecheck.Scanner.scanner import utlis
from sitecheck.Scanner.scanner import endpoints

hostname = os.environ.get('awsip')
port = int(os.environ.get('awsport', '-1'))
client = mqtt.Client("qv", clean_session=True)
client.connect(hostname, port)

# Logger streams
root_log = utlis.make_logger('root')
logger = utlis.make_logger('log')
config_log = utlis.make_logger('config')
data_log = utlis.make_logger('data')
projecthandler_log = utlis.make_logger('projecthandler')
utlis_log = utlis.make_logger('utlis')
chrome_log = utlis.make_logger('chrome')


projects = config.read_config_file()


async def Scan():
    """
    Invoke to Scan all projects marked with "skip = false" in projects.ini
    """
    from sitecheck.Scanner.scanner import projecthandler

    client.publish('Scanner/arguments', f"{sys.argv}")
    client.publish('Scanner/ProjectTable',
                   f'\n{utlis.projects_table(config.read_config_file())}')
    [await (projecthandler.run_controller(project)) for project in
     projects.sections()]
    logger.info('\nScan completed.')


async def daemon(topic='Scanner/stdin'):
    """Create an MQTT client daemon that listens for commands"""
    client.subscribe(topic)
    client.publish('Scanner/log', f"Daemon activated for topic '{topic}'")
    client.on_message = on_message
    client.loop_forever()


async def on_message(userdata, message):
    client.publish('Scanner/stdout', f"{message.topic}: Received message ""'{str(message.payload)} \n'"
                   f"With userdata: {str(userdata)}")
    endpoints.parse(message)


def repl():
    """
    Repl mode entry point. 
    Implies debug, check, and headful modes
    """
    logger.info('Scanner/log', f"Repl mode running")
    embed(globals(), locals())


def edit():
    """
    Edits project config file
    """    
    config.edit_project()


def enable_all_projects():
    """
    Quick reset of all projects to skip = false
    """
    for each in projects.sections():
        config.edit_config_option(each, 'skip', 'false')
