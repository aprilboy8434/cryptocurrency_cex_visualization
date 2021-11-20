import os
from configparser import ConfigParser

def configParserHelper(configJsonFilePath, section):

    configJsonFilePath = os.path.expanduser( configJsonFilePath )

    # create a parser
    parser = ConfigParser()

    # read config file
    parser.read(configJsonFilePath)

    # get section, default to postgresql
    configDict = dict()
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            configDict[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, configJsonFilePath))

    return configDict