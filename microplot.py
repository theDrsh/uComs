import logging
import os
import sys
import yaml

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
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

        element_list = list()
        for element in self._yaml_data['Protocol']:
            if element != "Commands":
                element_list.append(element)

        self._compiled_commands = dict()
        for command, command_values in self._yaml_data['Protocol']['Commands'].items():
            pattern = command_values['Pattern']
            command_pattern = pattern.split("%")
            # remove any empty elements
            command_pattern.remove("")
            output_string = ""
            for element in command_pattern:
                if element not in element_list:
                    output_string += element
                else:
                    output_string += self._yaml_data['Protocol'][element]
                self._compiled_commands[command] = output_string
