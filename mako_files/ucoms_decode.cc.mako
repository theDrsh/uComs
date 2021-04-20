// ucoms generates this file
// DO NOT EDIT
// This file contains implementations of a decoder in C++

#include "generated_ucoms_decode.h"
#include <string.h>

char uComsDecode::Increment(int* index, const char* input) {
    *index += 1;
    if(*index > (strlen(input) - 1)) {
        return '\0';
    }
    return input[*index];
}

int uComsDecode::ParseSubstring(int index, const char* input, const char end_char) {
  for (int i = index; i < strlen(input); i++) {
    if(input[i] == end_char) {
      return i;
    }
  }
  return -1;
}

uComsValue_t uComsDecode::ValueHandler(int index, int end_index, const char* input, uComsValue_e value_type) {
  uComsValue_t ret_val = INIT_VALUE_STRUCT;
  int len = (end_index - index) + 1;
  char substr[len] = "\0";
  memcpy(substr, &input[index], len);
  switch(value_type) {
    case uComsValueInt: {
      char* end_ptr = 0;
      // Be strict about leading chars
      if (isdigit(input[index]) || (input[index] == '-')) {
        ret_val.value_int = strtol(substr, &end_ptr, 0);
        // This validates no trailing chars/wonky input
        if (*end_ptr == input[end_index]) {
          ret_val.stored_type = uComsValueInt;
        }
      }
      break;
    }
    case uComsValueBool:
      ret_val.value_bool = strtol(substr, nullptr, 0);
      if ((ret_val.value_bool > 1) || (ret_val.value_bool < 0)) {
        ret_val.value_bool = BOOL_NA;
        ret_val.stored_type = uComsValueError;
      } else {
        ret_val.stored_type = uComsValueBool;
      }
      break;
    case uComsValueFloat:
      ret_val.value_float = strtod(substr, nullptr);
      ret_val.stored_type = uComsValueFloat;
      break;
    case uComsValueNone:
    case uComsValueError:
    default:
      ret_val.stored_type = uComsValueError;
  }
  return ret_val;
}

## NOTE: remember we are using the host decoder here, because we are decoding host commands
uComsDecodedCommand uComsDecode::Decode(const char* input) {
  int index = 0;
  char working_char = input[index];
  int length = strlen(input);
  int end_index = 0;
  uComsDecodedCommand command = INIT_DECODE_STRUCT;
  ${uc.host_decoder.decoder_string}
  return INIT_DECODE_STRUCT;
}