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
        self.protocol_yaml = protocol_yaml
        # Setup module logger.
        self._logger = logging.getLogger("ucoms")
        self._logger.info("Starting ucoms")
        # Check if file exists, if it does, load the yaml data
        if os.path.isfile(protocol_yaml):
            with open(protocol_yaml) as file_pointer:
                self._yml_data = yaml.full_load(file_pointer)
                self._logger.info("Loaded %s as protocol description" %
                                  (protocol_yaml))
        else:
            logger.fatal("Protocol file %s doesn't exist in the file system" %
                         (protocol_yaml))
            sys.exit(1)
        self.compiled_host_dict = dict()
        self.compiled_device_dict = dict()
    
    def compile_commands(self):
        # Make some short hands
        pattern_list = self._yml_data["Protocol"]["Patterns"].keys()
        protocol = self._yml_data["Protocol"]
        dict_of_commands = protocol["Commands"]
        for pattern in pattern_list:
            if "Command" not in protocol["Patterns"][pattern]:
                logger.fatal("Command key is required but not found in pattern %s"%(pattern))
                sys.exit(1)
            command_item = protocol["Patterns"][pattern]["Command"]
            print(command_item)
            host_pattern = protocol["Patterns"][pattern]["Host"]
            device_pattern = protocol["Patterns"][pattern]["Device"]
            compiled_command = ""
            # Compile the host commands by taking a pattern, building it then creating a dict with all the keys and values of compiled commands
            for host_item in host_pattern:
                if host_pattern[host_item] in protocol:
                    compiled_command += protocol[host_pattern[host_item]]
                elif host_pattern[host_item] == "Command":
                    compiled_command += command_item
                elif host_pattern[host_item] == "Argument":
                    compiled_command += "{}"
                else:
                    logger.fatal("Protocol %s specifies key %s in Host pattern of %s interaction which doesn't exist in protocol"%(self.protocol_yaml, host_pattern[host_item], pattern))
                    sys.exit(1)
            for (argument_key, argument_value) in dict_of_commands[pattern].items():
                key = pattern + argument_key + "Host"
                value = compiled_command.format(argument_value)
                if key in dict_of_commands:
                    logger.fatal("Duplicate Key %s in compiled Host commands"%(key))
                self.compiled_host_dict.update({key : value})
                    
            for device_item in device_pattern:
                pass


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
                    self._yml_data["Protocol"]["Delimiter"])
                key = split_string[0]
                working_string = split_string[1]
            else:
                split_string = working_string.split(
                    self._yml_data["Protocol"][element])
                if len(split_string) > 1:
                    if split_string[0] == '':
                        working_string = split_string[1]
            if key is not None and value is not None:
                commands = self._yml_data["Protocol"]["Commands"].items()
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
            output_filename = "generated_files/generated_" + output_filename
            output_file = open(output_filename, "w+")
            output_file.write(template.render())
            self._logger.info("Genererated %s as %s" %
                              (template.filename, output_filename))
            output_file.close()

    def validateData(self):
        if self._yml_data is not None:
            return True
        return False


class uComsDecoder():
    '''
    The Decoder uses a tree to build a nested switch-case in C/C++
    '''
    class Tree():

        class Leaf():
            def __init__(self, value):
                self.children = None
                self.value = value

        def __init__(self):
            self.root = self.Leaf("")
            self.max_depth = 0
            self.tree_list = []

        def build_tree(self, command_list):
            for command in command_list:
                self.insert(command, self.root, 1)

        def insert(self, value, leaf, depth):
            if not leaf.children:
                leaf.children = []
                leaf.children.append(self.Leaf(value[0]))
                if depth > self.max_depth:
                    self.max_depth = depth
                if len(value) > 1:
                    self.insert(value[1:], leaf.children[-1], depth + 1)
                return
            else:
                for child in leaf.children:
                    if child.value == value[0]:
                        if len(value) > 1:
                            self.insert(value[1:], child, depth + 1)
                        return
                leaf.children.append(self.Leaf(value[0]))
                if len(value) > 1:
                    self.insert(value[1:], leaf.children[-1], depth + 1)
                
        def print_tree(self):
            if not self.root.children:
                print(None)
                return
            for i in range(self.max_depth + 1):
                self.tree_list.append("%d: "%(i))
            self.print_tree_helper(self.root, self.tree_list, 0)
            print(self.tree_list)

        def print_tree_helper(self, leaf, tree_list, index):
            if index >= len(tree_list):
                return
            tree_list[index] += " " + leaf.value
            if not leaf.children:
                return
            for child in leaf.children:
                self.print_tree_helper(child, tree_list, index + 1)

    def __init__(self, yml_data):
        self._yml_data = yml_data
        self.tree = self.Tree()
        self.compiled_command_list = []
    
    def build_decoder(self):
        pattern = self._yml_data["Protocol"]["Pattern"]
        root_pattern = self._yml_data["Protocol"][pattern[1]]
        if len(root_pattern) <= 1 and len(root_pattern) > 0:
            self.tree.root.value = root_pattern
            del pattern[1]
        for command_value in self._yml_data["Protocol"]["Commands"].values():
            temp_string = "" 
            for pattern_value in pattern.values():
                if pattern_value == "Command":
                    temp_string += command_value        
                elif pattern_value == "Value":
                    continue
                else:
                    temp_string += self._yml_data["Protocol"][pattern_value]
            self.compiled_command_list.append(temp_string)
        self.tree.build_tree(self.compiled_command_list)



def main():
    uc = uComs(ARGS.proto_yaml)
    if ARGS.generate:
        uc.generate(ARGS.force_c, ARGS.first_generation)
    uc.compile_commands()
    # decoder = uComsDecoder(uc._yml_data)
    # decoder.build_decoder()


if __name__ == "__main__":
    main()
