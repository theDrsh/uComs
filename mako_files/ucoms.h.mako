// ucoms generates this file
// DO NOT EDIT
// This file contains definitions of:
//    actions - this is the code that is run when a command is parsed, big switch statement
//    init - this is the code that is run that connects ucoms to hardware interfaces
//    parse - tree based parser for parsing commands to an enum, and generates reply

typedef enum {
  kCommandTypeNone = 0,
% for command_type in range(len(uc.pattern_types)):
  ${'kCommandType' + uc.pattern_types[command_type]} = ${command_type + 1},
% endfor
  kLenCommandTypes = ${len(uc.pattern_types) + 1},
} uComsCommandTypes_e;

typedef enum {
  kCommandNone = 0,
% for command in range(len(uc.commands)):
  ${'kCommand' + uc.commands[command]} = ${command + 1},
% endfor
  kLenCommands = ${len(uc.commands) + 1},
} uComsCommands_e;

typedef struct  {
  uComsCommands_e command;
  uComsCommandTypes_e command_type;
} uComsDecodedCommand_t;
