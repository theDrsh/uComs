#!/usr/bin/python3

import argparse
import logging
import os
import sys
import yaml
from mako.template import Template

# TODO: Make a map between host and device keys, and give it to the decoder object, allow it to look up an input key and output key pair.

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
parser.add_argument("--first_generation",
                    help="This flag generates the one-time files which will \
                          be maintained by user \
                          after first generation these files are: \
                          \'ucoms_init.h/c/cc\' and \
                          \'ucoms_actions.h/cc/c\'",
                    default=False,
                    action="store_true")
parser.add_argument("-y",
                    "--proto_yaml",
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
        self.command_mapping = dict()
        self.compiled_host_dict = dict()
        self.compiled_device_dict = dict()
        self.value_type_map = dict()
        self.type_map = dict()
        self.compile_commands()
        self._logger.info("Building Host decoder...")
        self.host_decoder = uComsDecoder(self.compiled_host_dict, self.type_map, self.value_type_map)
        self._logger.info("Building Device decoder...")
        self.device_decoder = uComsDecoder(self.compiled_device_dict, self.type_map, self.value_type_map)
        self.pattern_types = list(self._yml_data["Protocol"]["Interactions"].keys())

    def compile_commands(self):
        # Make some short hands
        interaction_list = self._yml_data["Protocol"]["Interactions"].keys()
        protocol = self._yml_data["Protocol"]
        dict_of_commands = protocol["Commands"]
        # Go through all Interactions and compile the host and device command dicts
        for pattern in interaction_list:
            if "Command" not in protocol["Interactions"][pattern]:
                logger.fatal("Command key not found for %s" % (pattern))
                sys.exit(1)
            command_item = protocol["Interactions"][pattern]["Command"]
            if "Host" in protocol["Interactions"][pattern]:
                host_pattern = protocol["Interactions"][pattern]["Host"]
            else:
                host_pattern = None
            if "Device" in protocol["Interactions"][pattern]:
                device_pattern = protocol["Interactions"][pattern]["Device"]
            else:
                device_pattern = None
            compiled_command = ""

            # Asynchronous commands can have no host patterns
            if host_pattern is not None:
                # Compile the host commands for given pattern
                for host_item in host_pattern:
                    if host_pattern[host_item] in protocol:
                        compiled_command += protocol[host_pattern[host_item]]
                    elif host_pattern[host_item] == "Command":
                        compiled_command += command_item
                    elif host_pattern[host_item] == "Argument":
                        # use formatter to be placeholder for the argument
                        compiled_command += "{}"
                    elif host_pattern[host_item] == "Value":
                        # if the host pattern has a value in it, that means it's an argument
                        compiled_command += "{}"
                        continue
                    else:
                        logger.fatal("Protocol %s specifies key %s in Host pattern \
                                    of %s which doesn't exist in protocol" % (
                                        self.protocol_yaml,
                                        host_pattern[host_item],
                                        pattern))
                        sys.exit(1)
                # Commands with expected arguments
                if pattern in dict_of_commands:
                    for (arg_key, arg_val) in dict_of_commands[pattern].items():
                        key = pattern + arg_key + "Host"
                        value = compiled_command.format(arg_val, "{}")
                        # Host patterns with a Value, are passing an arguement down to the device
                        if "{}" in value:
                            self.value_type_map[pattern] = self._yml_data["Protocol"]["Interactions"][pattern]["ValueType"]
                            value = value.format("{%s}"%(self._yml_data["Protocol"]["Interactions"][pattern]["ValueType"]))
                        if key in dict_of_commands:
                            logger.fatal("Duplicate Key %s in compiled Host commands" %
                                        (key))
                        self.type_map.update({key : pattern})
                        self.compiled_host_dict.update({key: value})
                else:
                    # Only have to do this once
                    key = pattern + "Host"
                    value = compiled_command
                    # Host patterns with a Value, are passing an arguement down to the device
                    if "{}" in value:
                        self.value_type_map[pattern] = self._yml_data["Protocol"]["Interactions"][pattern]["ValueType"]
                        value = value.replace("{}", self._yml_data["Protocol"]["Interactions"][pattern]["ValueType"])
                    if key in dict_of_commands:
                        logger.fatal("Duplicate Key %s in compiled Host commands" %
                                    (key))
                    self.type_map.update({key : pattern})
                    self.compiled_host_dict.update({key: value})


            compiled_command = ""
            if device_pattern is not None:
                for device_item in device_pattern:
                    if device_pattern[device_item] in protocol:
                        compiled_command += protocol[device_pattern[device_item]]
                    elif device_pattern[device_item] == "Command":
                        compiled_command += command_item
                    elif device_pattern[device_item] == "Argument":
                        compiled_command += "{}"
                    elif device_pattern[device_item] == "Value":
                        compiled_command += "{}"
                    else:
                        logger.fatal("Protocol %s specifies key %s in Device \
                        pattern of %s interaction which doesn't exist in \
                        protocol" % (self.protocol_yaml,
                                    device_pattern[device_item],
                                    pattern))
                        sys.exit(1)
                if pattern in dict_of_commands:
                    for (arg_key, arg_val) in dict_of_commands[pattern].items():
                        key = pattern + arg_key + "Device"
                        value = compiled_command.format(arg_val, "{}")
                        if key in dict_of_commands:
                            logger.fatal("Duplicate Key %s in compiled Device dict" %
                                        (key))
                        self.type_map.update({key : pattern})
                        self.compiled_device_dict.update({key: value})
                else:
                    key = pattern + "Device"
                    value = compiled_command
                    if key in dict_of_commands:
                        logger.fatal("Duplicate Key %s in compiled Device dict" %
                                    (key))
                    self.type_map.update({key : pattern})
                    self.compiled_device_dict.update({key: value})
            if pattern in dict_of_commands:
                for (arg_key, arg_val) in dict_of_commands[pattern].items():
                    host_key = pattern + arg_key + "Host"
                    device_key = pattern + arg_key + "Device"
                    self.command_mapping.update({host_key : device_key})
            else:
                host_key = "None"
                device_key = "None"
                if host_pattern is not None:
                    host_key = pattern + "Host"
                if device_pattern is not None:
                    device_key = pattern + "Device"
                self.command_mapping.update({host_key : device_key})

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
        # Remove value from string
        for (device_key, device_value) in self.compiled_device_dict.items():
            if '{}' in device_value:
                preamble = device_value.split('{}')[0]
                post_value = device_value.split('{}')[-1]
                if (preamble in input_string) and (post_value in input_string):
                    working_string = input_string[len(preamble):]
                    value = float(working_string.split(post_value)[0])
                    key = device_key
            elif input_string == device_value:
                key = device_key
                value = device_value
        return {key: value}

    def generate(self, generate_actions):
        self._logger.info("Starting Generator")
        templates = [Template(
            filename="mako_files/ucoms.h.mako")]
        templates.append(Template(
            filename="mako_files/ucoms_decode.h.mako"))
        templates.append(Template(
            filename="mako_files/ucoms.cc.mako"))
        # TEST HEADERS
        templates.append(Template(
        filename="mako_files/ucoms_decode_test.h.mako"))
        templates.append(Template(
            filename="mako_files/ucoms_decode.cc.mako"))
        if generate_actions:
            templates.append(
                Template(filename="mako_files/ucoms_init.cc.mako"))
            templates.append(
                Template(filename="mako_files/ucoms_actions.cc.mako"))
        for template in templates:
            self._logger.info("Generating %s" % (template.filename))
            output_filename = template.filename.split('/')[-1]
            output_filename = output_filename.split(".mako")[0]
            output_filename = "generated_files/generated_" + output_filename
            output_file = open(output_filename, "w+")
            output_file.write(template.render(uc=self))
            self._logger.info("Generated %s as %s" %
                              (template.filename, output_filename))
            output_file.close()

    def GetHostKey(self, value):
        for host_key, host_value in self.compiled_host_dict.items():
            if value == str(host_value):
                return host_key
        return None

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
            def __init__(self, value, depth, path_value):
                self.children = None
                self.value = value
                self.depth = depth
                self.path_value = path_value

        def __init__(self):
            self.root = self.Leaf("", 0, "")
            self.max_depth = 0
            self.tree_list = []

        def build_tree(self, command_list):
            for command in command_list:
                self.insert(command, self.root, 1, command)

        def insert(self, value, leaf, depth, orig_string):
            if not leaf.children:
                leaf.children = []
                leaf.path_value = ""
                if (value[0] == '{') and ("}" in value):
                    value_type = value.split("}")[0][1:]
                    leaf.children.append(self.Leaf("uComsValue%s"%(value_type), depth, orig_string))
                    value = value.split("}")[-1]
                    value = " " + value
                else:
                    leaf.children.append(self.Leaf(value[0], depth, orig_string))
                if depth > self.max_depth:
                    self.max_depth = depth
                if len(value) > 1:
                    self.insert(value[1:], leaf.children[-1], depth + 1, orig_string)
                return
            else:
                for child in leaf.children:
                    if child.value == value[0]:
                        if len(value) > 1:
                            self.insert(value[1:], child, depth + 1, orig_string)
                        return
                if (value[0] == '{') and ("}" in value):
                    value_type = value.split("}")[0][1:]
                    leaf.children.append(self.Leaf("uComsValue%s"%(value_type), depth, orig_string))
                    value = value.split("}")[-1]
                    value = " " + value
                else:
                    leaf.children.append(self.Leaf(value[0], depth, None))
                if len(value) > 1:
                    self.insert(value[1:], leaf.children[-1], depth + 1, orig_string)
        def tree_to_list_of_lists(self):
            pass
        def recursive_dfs(self, leaf):
            if not leaf.children:
                return
            for child in leaf.children:
                self.recursive_dfs(child)



    def __init__(self, compiled_dict, type_map, value_type_map):
        self.compiled_dict = compiled_dict
        self.type_map = type_map
        self.value_type_map = value_type_map
        self.tree = self.Tree()
        self.compiled_command_list = []
        for compiled_value in self.compiled_dict.values():
            self.compiled_command_list.append(compiled_value)
        self.build_decoder()
        self.decoder_string = ""
        self.build_decoder_string()

    def build_decoder(self):
        self.tree.build_tree(self.compiled_command_list)

    def build_decoder_string(self):
        self.decoder_string = self.build_decoder_string_helper(self.tree.root, 2)

    def build_decoder_string_helper(self, leaf, spacing):
        spacing_str = "  " * spacing
        leaf_with_children_string = ""
        leaf_with_no_children_string = ""
        if not leaf.children:
            # Leaf with no children
            child_string =   "case \'" + leaf.value + "\':\n"
            child_string +=  spacing_str + "    if ((strlen(input) - 1) > index) { return INIT_DECODE_STRUCT; }\n"
            child_string +=  spacing_str + "    command.input = kCommand" + self.GetKey(leaf.path_value) + ";\n"
            child_string +=  spacing_str + "    command.output = GetDeviceKey(command.input);\n"
            child_string +=  spacing_str + "    command.command_type = kCommandType" + self.type_map[self.GetKey(leaf.path_value)] +";\n"
            leaf_with_no_children_string += spacing_str + child_string
            leaf_with_no_children_string += spacing_str + "    return command;\n"
            return leaf_with_no_children_string
        # Skip root case
        if leaf is not self.tree.root:
            if (len(leaf.children) == 1) and ("uComsValue" in leaf.children[0].value):
                leaf_with_children_string += spacing_str + "case \'" + leaf.value + "\':\n"
                spacing_str += "  "
                leaf_with_children_string += spacing_str + "index++;\n"
                leaf_with_children_string += spacing_str + "end_index = ParseSubstring(index, input, '%s');\n"%(leaf.children[0].children[0].value)
                leaf_with_children_string += spacing_str + "if (end_index < 0) { return INIT_DECODE_STRUCT; }\n"
                leaf_with_children_string += spacing_str + "command.value = ValueHandler(index, end_index, input, %s);\n"%(leaf.children[0].value)
                leaf_with_children_string += spacing_str + "if (command.value.stored_type == uComsValueError) { return INIT_DECODE_STRUCT; }\n"
                leaf_with_children_string += spacing_str + "index = end_index;\n"
                leaf_with_children_string += spacing_str + "working_char = input[index];\n"
                leaf_with_children_string += spacing_str + "switch (working_char) {\n"
                brace_spacing = len(spacing_str)
                leaf = leaf.children[0]
            else:
                leaf_with_children_string += spacing_str + "case \'" + leaf.value + "\':\n"
                spacing_str += "  "
                leaf_with_children_string += spacing_str + "working_char = Increment(&index, input);\n"
                leaf_with_children_string += spacing_str + "switch (working_char) {\n"
                brace_spacing = len(spacing_str)
        else:
            leaf_with_children_string += "switch (working_char) {\n"
            brace_spacing = 2
        # Iterate through children to create cases for switch
        for child in leaf.children:
            spacing_str += "  "
            # Skip root spacing
            if leaf is not self.tree.root:
                leaf_with_children_string += self.build_decoder_string_helper(child, spacing + 2)
            else:
                leaf_with_children_string += self.build_decoder_string_helper(child, spacing)
        # Close curly braces
        leaf_with_children_string += spacing_str + "default:\n"
        leaf_with_children_string += spacing_str + "  return INIT_DECODE_STRUCT;\n"
        leaf_with_children_string += (brace_spacing * " ") + "}\n"
        # Return string recursively
        return leaf_with_children_string

    def GetKey(self, in_value):
        for key, value in self.compiled_dict.items():
            if value == in_value:
                return key
        return None

def main():
    uc = uComs(ARGS.proto_yaml)
    if ARGS.generate:
        uc.generate(ARGS.first_generation)


if __name__ == "__main__":
    main()
