import logging
import os
import re
import sys
import yaml

logging.basicConfig(format='MICROPLOT %(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logger = logging.Logger("MicroPlot")
module_logger = logging.getLogger('MicroPlot')


class MicroPlot():
    def __init__(self, protocol_yaml):
        # Setup module logger.
        self._logger = logging.getLogger("Microplot")
        self._logger.info("Starting MicroPlot")
        # Check if file exists, if it does, load the yaml data
        if os.path.isfile(protocol_yaml):
            with open(protocol_yaml) as file_pointer:
                self._yaml_data = yaml.load(file_pointer)
                self._logger.info("Loaded %s as protocol description" % (protocol_yaml))
        else:
            logger.fatal("Protocol file %s doesn't exist in the file system" % (protocol_yaml))
            sys.exit(1)
        self._pattern_list = list()
        for element_key, element_value in self._yaml_data['Protocol']['Pattern'].items():
            self._pattern_list.insert(int(elemen`t_key), element_value)

    def parse(self, input_string):
        '''
            Iterate through the pattern list, make sure that each element is the first in the
            string then pop off of string, if we are looking at the command in the list we expect
            the delimiter to immediately follow, then if we are looking at the value, pull the
            integer value out of it
        '''
        working_string = input_string
        value = None
        key = None
        for element in self._pattern_list:
            if element == "Value":
                # TODO(Daniel): handle values other than ints
                value = int(re.search(r'\d+', working_string).group())
            elif element == "Command":
                # TODO(Daniel): handle command formats other then command then delimiter
                split_string = working_string.split(self._yaml_data["Protocol"]["Delimiter"])
                key = split_string[0]
                working_string = split_string[1]
            else:
                split_string = working_string.split(self._yaml_data["Protocol"][element])
                if len(split_string) > 1:
                    if split_string[0] == '':
                        working_string = split_string[1]
            if key is not None and value is not None:
                for command_key, command_value in self._yaml_data["Protocol"]["Commands"].items():
                    if key == command_value:
                        return {command_key : value}
        return None
