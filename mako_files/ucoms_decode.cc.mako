// ucoms generates this file
// DO NOT EDIT
// This file contains implementations of a decoder in C++

#include "generated_ucoms_decode.h"

bool uComsDecode::increment(int* index, char* working_char, char* input) {
    *index++;
    if(*index > (strlen(input) - 1)) {
        return false;
    }
    *working_char = input[index] 
    return true;
}

## NOTE: remember we are using the host decoder here, because we are decoding host commands
uComsDecodedCommand uComsDecode::Decode(char* input) {
  int index = 0;
  char working_char = input[index];
  int length = strlen(input);
  switch(working_char) {
    ${uc.host_decoder.decoder_string}
  }
}