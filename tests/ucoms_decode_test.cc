#include "generated_ucoms_decode.h"
#include "generated_ucoms_decode_test.h"
#include <gtest/gtest.h>

class test_uComsDecode : public testing::Test {
 protected:
  virtual void SetUp();
};

void test_uComsDecode::SetUp() {
  return;
}

TEST_F(test_uComsDecode, spewTest) {
  for (int i = 0; i < kLenTestKeys; i++) {
    // Testing that I can fill in a string like this
    char test_string[256];
    int result;
    result = sprintf(test_string, TestCommandOutputValues[i].c_str(), i);
    EXPECT_GT(TestCommandInputValues[i].length(), 0);
    EXPECT_GT(strlen(test_string), 0);
    EXPECT_GT(result, 0);
  }
}

TEST_F(test_uComsDecode, decoderTest) {
  uComsDecode decoder;
  int max_len = 0;
  for (int i = 0; i < kLenTestKeys; i++) {
    int cur_length = TestCommandInputValues[i].length();
    max_len = (cur_length > max_len) ? cur_length : max_len;
  }
  char input_string[max_len * 2] = "\0";
  for (int i = 0; i < kLenTestKeys; i++) {
    snprintf(input_string, max_len * 2, TestCommandInputValues[i].c_str(), i);
    uComsDecodedCommand decode_struct = decoder.Decode(input_string);
    EXPECT_EQ(decode_struct.input, TestStructs[i].input);
    EXPECT_EQ(decode_struct.output, TestStructs[i].output);
    EXPECT_EQ(decode_struct.command_type, TestStructs[i].command_type);
    EXPECT_EQ(decode_struct.value.stored_type, TestStructs[i].value.stored_type);
    EXPECT_EQ(decode_struct.value.value_int, TestStructs[i].value.value_int);
    EXPECT_EQ(decode_struct.value.value_float, TestStructs[i].value.value_float);
    EXPECT_EQ(decode_struct.value.value_bool, TestStructs[i].value.value_bool);
  }
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
