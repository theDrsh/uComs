// ucoms generates this file
// DO NOT EDIT
// This file contains function prototypes for ucoms_decoder
#include "generated_ucoms.h"

class uComsDecode {
 public:
  uComsDecodedCommand Decode(const char* input);
 private:
  char Increment(int* index, const char* input);
  // ParseValue takes in the input/index then finds the end char and returns the length of the arg
  int ParseSubstring(int index, const char* input, const char end_char);
  uComsValue_t ValueHandler(int index, int end_index, const char* input, uComsValue_e value_type);
};
