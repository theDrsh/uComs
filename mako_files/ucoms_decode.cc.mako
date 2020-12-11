// ucoms generates this file
// DO NOT EDIT
// This file contains implementations of a decoder in C++

#include "generated_ucoms_decode.h"
#include <string.h>

bool uComsDecode::Increment(int* index, char* working_char, char* input) {
    *index++;
    if(*index > (strlen(input) - 1)) {
        return false;
    }
    *working_char = input[*index];
    return true;
}

## NOTE: remember we are using the host decoder here, because we are decoding host commands
uComsDecodedCommand uComsDecode::Decode(const char* input) {
  int index = 0;
  char working_char = input[index];
  int length = strlen(input);
  ${uc.host_decoder.decoder_string}
}