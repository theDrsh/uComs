// GENERATED DO NOT EDIT
#include "generated_ucoms.h"
#include <string>

#pragma once

// These should be the DEVICE command keys
enum TestCommandKeys {
% for device_key in range(len(list(uc.compiled_device_dict.keys()))):
  ${'kTestKey' + list(uc.compiled_device_dict.keys())[device_key]} = ${device_key},
% endfor
% for host_key in range(len(list(uc.compiled_host_dict.keys()))):
  % if host_key not in uc.command_mapping:
  ${'kTestKey' + list(uc.compiled_host_dict.keys())[host_key]} = ${host_key},
  %endif
% endfor
  kLenTestKeys = ${len(list(uc.compiled_device_dict.keys()))}
};

// These should be the HOST values(input of decoder)
const std::string TestCommandInputValues[kLenTestKeys] {
% for host_key in range(len(list(uc.compiled_host_dict.keys()))):
  % if "{Int}" in uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]]:
  [${'kTestKey' + list(uc.compiled_device_dict.keys())[host_key]}] = "${"%s%s%s"%(uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]].split("{Int}")[0], "%d", uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]].split("{Int}")[-1])}",
  % elif "{float}" in uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]]:
  [${'kTestKey' + list(uc.compiled_device_dict.keys())[host_key]}] = "${uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]]}",
  % elif "{bool}" in uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]]:
  [${'kTestKey' + list(uc.compiled_device_dict.keys())[host_key]}] = "${uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]]}",
  % else:
  [${'kTestKey' + list(uc.compiled_device_dict.keys())[host_key]}] = "${uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]]}",
  % endif
% endfor
};

// These should be the DEVICE values(output of decoder)
const std::string TestCommandOutputValues[kLenTestKeys] {
% for device_key in range(len(list(uc.compiled_device_dict.keys()))):
  [${'kTestKey' + list(uc.compiled_device_dict.keys())[device_key]}] = "${(uc.compiled_device_dict[list(uc.compiled_device_dict.keys())[device_key]]).format("%d")}",
% endfor
};

uComsDecodedCommand TestStructs[kLenTestKeys] = {
% for (host, device) in uc.command_mapping.items():
  % if "GetOne" in host:
  [${'kTestKey' + device}] = {.input = ${"kCommand" + host}, .output = ${"kCommand" + device}, .command_type = ${"kCommandType" + uc.type_map[device]}, .value = INIT_VALUE_STRUCT},
  % elif "SetOne" in host:
  [${'kTestKey' + device}] = {.input = ${"kCommand" + host}, .output = ${"kCommand" + device}, .command_type = ${"kCommandType" + uc.type_map[device]}, .value = {.value_int=${"kTestKey" + device}, .value_bool=BOOL_NA, .value_float=FLOAT_NA, .stored_type=uComsValueInt}},
  % elif "StartAsync" in host:
  [${'kTestKey' + host}] = {.input = ${"kCommand" + host}, .output = ${"kCommandNoneDevice"}, .command_type = ${"kCommandTypeStartAsyncReport"}, .value = {.value_int=INT_NA, .value_bool=BOOL_NA, .value_float=FLOAT_NA, .stored_type=uComsValueError}},
  % else:

  % endif
% endfor
};
