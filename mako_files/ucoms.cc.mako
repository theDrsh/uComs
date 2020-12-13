// ucoms generates this file
// DO NOT EDIT
// This file contains definitions of:
//    actions - this is the code that is run when a command is parsed, big switch statement
//    init - this is the code that is run that connects ucoms to hardware interfaces
//    parse - tree based parser for parsing commands to an enum, and generates reply
#include "generated_ucoms.h"

uComsCommandsDevice GetDeviceKey(uComsCommandsHost host_key) {
  switch (host_key) {
% for host,device in uc.command_mapping.items():
    case ${"kCommand" + host}:
      return ${"kCommand" + device};
% endfor
    default:
      break;
  }
  return kCommandNoneDevice;
}

uComsCommandsHost GetHostKey(uComsCommandsDevice device_key) {
  switch (device_key) {
% for host,device in uc.command_mapping.items():
    case ${"kCommand" + device}:
      return ${"kCommand" + host};
% endfor
    default:
      break;
  }
  return kCommandNoneHost;
}

std::string GetHostKeyString(uComsCommandsHost host_key) {
  switch (host_key) {
% for host in uc.command_mapping.keys():
    case ${"kCommand" + host}:
      return "${"kCommand" + host}";
% endfor
    default:
      break;
  }
  return "";
}

std::string GetDeviceKeyString(uComsCommandsDevice device_key) {
  switch (device_key) {
% for device in uc.command_mapping.values():
    case ${"kCommand" + device}:
      return "${"kCommand" + device}";
% endfor
    default:
      break;
  }
  return "";
}