// ucoms generates this file
// DO NOT EDIT
// This file contains function prototypes for ucoms_decoder
#include "generated_ucoms.h"

class uComsDecode {
 public:
  uComsDecodedCommand Decode(const char* input);
 private:
  char Increment(int* index, const char* input);
};
