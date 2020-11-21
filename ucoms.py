#!/usr/bin/python3

import argparse
import logging
import os
import re
import sys
import yaml
from mako.template import Template

# Logger setup for logging(as executable or as import)
logging.basicConfig(format='ucoms %(asctime)s %(levelname)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)
logger = logging.Logger("ucoms")
module_logger = logging.getLogger('ucoms')

# Argparse setup for calling this as an executable.
parser = argparse.ArgumentParser(
    prog="ucoms",
    description="ucoms is a module as well as an executable, \
                 running it as an executable allows you to use the \
                 code generation functions"
)
parser.add_argument("-g",
                    "--generate",
                    help="Run code generation tools",
                    action="store_true",
                    default=False)
parser.add_argument("--force_c",
                    help="If you prefer to use pure C for your embedded code, \
                          use this option to force generation of C code",
                    default=False,
                    action="store_true")
parser.add_argument("--first_generation",
                    help="This flag generates the one-time files which will \
                          be maintained by user \
                          after first generation these files are: \
                          \'ucoms_init.h/c/cc\' and \
                          \'ucoms_actions.h/cc/c\'",
                    default=False,
                    action="store_true")
parser.add_argument("--proto_yaml",
                    help="Protocol description yaml file.",
                    default="example_protocol.yml")
ARGS = parser.parse_args()


class uComs():
    def __init__(self, protocol_yaml):
        # Setup module logger.
        self._logger = logging.getLogger("ucoms")
        self._logger.info("Starting ucoms")
        # Check if file exists, if it does, load the yaml data
        if os.path.isfile(protocol_yaml):
            with open(protocol_yaml) as file_pointer:
                self._yaml_data = yaml.full_load(file_pointer)
                self._logger.info("Loaded %s as protocol description" %
                                  (protocol_yaml))
        else:
            logger.fatal("Protocol file %s doesn't exist in the file system" %
                         (protocol_yaml))
            sys.exit(1)
        self._pattern_list = list()
        pattern = self._yaml_data['Protocol']['Pattern'].items()
        for element_key, element_value in pattern:
            self._pattern_list.insert(int(element_key), element_value)
        self._logger.info("Protocol file parsed successfully")
        if self.validateData():
            self._logger.debug("Build and validation successful")
        else:
            self._logger.fatal("Failed to validate data")

    def parse(self, input_string):
        '''
            Iterate through the pattern list, make sure that each element is
            the first in the string then pop off of string, if we are looking
            at the command in the list we expect the delimiter to immediately
            follow, then if we are looking at the value, pull the integer out
        '''
        working_string = input_string
        value = None
        key = None
        for element in self._pattern_list:
            if element == "Value":
                # TODO(Daniel): handle values other than ints
                value = int(re.search(r'[-+]?\d*\.?\d+([eE][-+]?\d+)?',
                            working_string).group())
                working_string = working_string.split(str(value))[-1]
            elif element == "Command":
                # TODO(Daniel): handle command formats
                split_string = working_string.split(
                    self._yaml_data["Protocol"]["Delimiter"])
                key = split_string[0]
                working_string = split_string[1]
            else:
                split_string = working_string.split(
                    self._yaml_data["Protocol"][element])
                if len(split_string) > 1:
                    if split_string[0] == '':
                        working_string = split_string[1]
            if key is not None and value is not None:
                commands = self._yaml_data["Protocol"]["Commands"].items()
                for command_key, command_value in commands:
                    if key == command_value:
                        self._logger.info("Parsed %s with value %d" %
                                          (command_key, value))
                        return {command_key: value}
        return None

    def generate(self, force_c, generate_actions):
        self._logger.info("Starting Generator")
        templates = [Template(
            filename="mako_files/ucoms.h.mako")]
        if not force_c:
            templates.append(Template(
                filename="mako_files/ucoms_decode.cc.mako"))
        else:
            templates.append(
                Template(filename="mako_files/ucoms_decode.c.mako"))
        if generate_actions:
            if not force_c:
                templates.append(
                    Template(filename="mako_files/ucoms_init.cc.mako"))
                templates.append(
                    Template(filename="mako_files/ucoms_actions.cc.mako"))
            else:
                templates.append(
                    Template(filename="mako_files/ucoms_init.c.mako"))
                templates.append(
                    Template(filename="mako_files/ucoms_actions.c.mako"))
        for template in templates:
            output_filename = template.filename.split('/')[-1]
            output_filename = output_filename.split(".mako")[0]
            output_filename = "generated_" + output_filename
            output_file = open(output_filename, "w+")
            output_file.write(template.render())
            self._logger.info("Genererated %s as %s" %
                              (template.filename, output_filename))
            output_file.close()

    def validateData(self):
        if self._yaml_data is not None:
            return True
        return False



def main():
    uc = uComs(ARGS.proto_yaml)
    if ARGS.generate:
        uc.generate(ARGS.force_c, ARGS.first_generation)


if __name__ == "__main__":
    main()
