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

## NOTE: remember we are using the host decoder here, because we are decoding host commands
uComsDecodedCommand uComsDecode::Decode(const char* input) {
  int index = 0;
  char working_char = input[index];
  int length = strlen(input);
  uComsDecodedCommand command;
  ${uc.host_decoder.decoder_string}
  return INIT_DECODE_STRUCT;
}