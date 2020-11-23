// ucoms generates this file
// DO NOT EDIT
// This file contains function prototypes for ucoms_decoder
#include "generated_ucoms.h"

class uComsDecode {
 public:
  uComsDecodedCommand Decode(char* input);
 private:
  bool Increment(int* index, char* working_char, char* input);
};
