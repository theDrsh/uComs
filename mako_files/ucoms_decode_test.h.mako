// GENERATED DO NOT EDIT
#include "generated_ucoms.h"
#include <string>

#pragma once

// These should be the DEVICE command keys
enum TestCommandKeys {
% for device_key in range(len(list(uc.compiled_device_dict.keys()))):
  ${'kTestKey' + list(uc.compiled_device_dict.keys())[device_key]} = ${device_key},
% endfor
  kLenTestKeys = ${len(list(uc.compiled_device_dict.keys()))}
};

// These should be the HOST values(input of decoder)
const std::string TestCommandInputValues[kLenTestKeys] {
% for host_key in range(len(list(uc.compiled_host_dict.keys()))):
  [${'kTestKey' + list(uc.compiled_device_dict.keys())[host_key]}] = "${uc.compiled_host_dict[list(uc.compiled_host_dict.keys())[host_key]]}",
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
  [${'kTestKey' + device}] = {.input = ${"kCommand" + host}, .output = ${"kCommand" + device}, .command_type = ${"kCommandType" + uc.type_map[device]}},
% endfor
};
  