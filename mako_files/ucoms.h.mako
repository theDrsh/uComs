// ucoms generates this file
// DO NOT EDIT
// This file contains definitions of:
//    actions - this is the code that is run when a command is parsed, big switch statement
//    init - this is the code that is run that connects ucoms to hardware interfaces
//    parse - tree based parser for parsing commands to an enum, and generates reply

#pragma once
#include <string>

enum uComsCommandTypes{
  kCommandTypeNone = 0,
% for command_type in range(len(uc.pattern_types)):
  ${'kCommandType' + uc.pattern_types[command_type]} = ${command_type + 1},
% endfor
  kLenCommandTypes = ${len(uc.pattern_types) + 1},
};

enum uComsCommandsHost {
  kCommandNoneHost = 0,
% for command in uc.compiled_host_dict.keys():
  ${'kCommand' + command} = ${(list(uc.compiled_host_dict.keys())).index(command) + 1},
% endfor
  kLenCommandsHost = ${len(list(uc.compiled_host_dict.keys())) + 1},
};

enum uComsCommandsDevice {
  kCommandNoneDevice = 0,
% for command in uc.compiled_device_dict.keys():
  ${'kCommand' + command} = ${(list(uc.compiled_device_dict.keys())).index(command) + 1},
% endfor
  kLenCommandsDevice = ${len(list(uc.compiled_device_dict.keys())) + 1},
};

// Prototypes
uComsCommandsDevice GetDeviceKey(uComsCommandsHost host_key);
uComsCommandsHost GetHostKey(uComsCommandsDevice device_key);
std::string GetDeviceKeyString(uComsCommandsDevice device_key);
std::string GetHostKeyString(uComsCommandsHost host_key);
uComsCommandTypes GetCommandType(uComsCommandsHost host_key);
uComsCommandTypes GetCommandType(uComsCommandsDevice device_key);

enum uComsValue_e {
  uComsValueNone  = -1,
  uComsValueInt   =  0,
  uComsValueBool  =  1,
  uComsValueFloat =  2,
  uComsValueError,
};

struct uComsValue_t {
  // handled types:
  int32_t value_int;
  int32_t    value_bool;
  float   value_float;
  // type stored:
  uComsValue_e stored_type;
};

struct uComsDecodedCommand {
  uComsCommandsHost input;
  uComsCommandsDevice output;
  uComsCommandTypes command_type;
  uComsValue_t value;
};

static const int32_t BOOL_NA = -1;
static const int32_t INT_NA = INT32_MAX;
static const float FLOAT_NA = -1;

static const uComsValue_t INIT_VALUE_STRUCT = {
  .value_int = INT_NA,
  .value_bool = BOOL_NA,
  .value_float = FLOAT_NA,
};

static const uComsDecodedCommand INIT_DECODE_STRUCT = {
  .input = (uComsCommandsHost)0,
  .output = (uComsCommandsDevice)0,
  .command_type = (uComsCommandTypes)42,
};
