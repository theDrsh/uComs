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
  for (int i = 0; i < kLenTestKeys; i++) {
    uComsDecodedCommand decode_struct = decoder.Decode(TestCommandInputValues[i].c_str());
    EXPECT_EQ(decode_struct.input, TestStructs[i].input);
    EXPECT_EQ(decode_struct.output, TestStructs[i].output);
    EXPECT_EQ(decode_struct.command_type, TestStructs[i].command_type);
  }
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
