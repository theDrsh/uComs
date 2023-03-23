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
    result = sprintf(test_string, TestCommandOutputValues[i], i);
    EXPECT_GT(strlen(TestCommandInputValues[i]), 0);
    EXPECT_GT(strlen(test_string), 0);
    EXPECT_GT(result, 0);
  }
}

TEST_F(test_uComsDecode, decoderTest) {
  uComsDecode decoder;
  int max_len = 0;
  for (int i = 0; i < kLenTestKeys; i++) {
    int cur_length = strlen(TestCommandInputValues[i]);
    max_len = (cur_length > max_len) ? cur_length : max_len;
  }
  char input_string[max_len * 2] = "\0";
  for (int i = 0; i < kLenTestKeys; i++) {
    snprintf(input_string, max_len * 2, TestCommandInputValues[i], i);
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

TEST_F(test_uComsDecode, noArgBadCmd) {
  uComsDecode decoder;
  // hardcode some bad commands, maybe figure out how to introduce noise later
  int num_test_commands = 7;
  std::string test_commands[num_test_commands] = {
    "$ GA0>\n",
    "$G A0\n",
    "$GA 0> \n",
    "$GA0 >\n",
    "$GA0> \n",
    "$GA10>\n",
    "$G0>\n",
  };
  for(int i = 0; i < num_test_commands; i++) {
    uComsDecodedCommand decode_struct = decoder.Decode(test_commands[i].c_str());
    // These should all return 0(bad command)
    EXPECT_EQ(decode_struct.input, INIT_DECODE_STRUCT.input);
    EXPECT_EQ(decode_struct.output, INIT_DECODE_STRUCT.output);
    EXPECT_EQ(decode_struct.command_type, INIT_DECODE_STRUCT.command_type);
    EXPECT_EQ(decode_struct.value.stored_type, INIT_DECODE_STRUCT.value.stored_type);
    EXPECT_EQ(decode_struct.value.value_int, INIT_DECODE_STRUCT.value.value_int);
    EXPECT_EQ(decode_struct.value.value_float, INIT_DECODE_STRUCT.value.value_float);
    EXPECT_EQ(decode_struct.value.value_bool, INIT_DECODE_STRUCT.value.value_bool);
  }
}

TEST_F(test_uComsDecode, oneArgBadCmd) {
  uComsDecode decoder;
  // hardcode some bad commands, maybe figure out how to introduce noise later
  int num_test_commands = 8;
  std::string test_commands[num_test_commands] = {
    "$ SD0 42>",
    "$S D0 42>",
    "$SD 0 42>",
    "$SD0  42>",
    "$SD0 4 2>",
    "$SD0 42 >",
    "$SD0 42> ",
    "$SD0 .15>",
    "$SD0 asdf>",
  };
  for(int i = 0; i < num_test_commands; i++) {
    uComsDecodedCommand decode_struct = decoder.Decode(test_commands[i].c_str());
    // These should all return 0(bad command)
    EXPECT_EQ(decode_struct.input, INIT_DECODE_STRUCT.input);
    EXPECT_EQ(decode_struct.output, INIT_DECODE_STRUCT.output);
    EXPECT_EQ(decode_struct.command_type, INIT_DECODE_STRUCT.command_type);
    EXPECT_EQ(decode_struct.value.stored_type, INIT_DECODE_STRUCT.value.stored_type);
    EXPECT_EQ(decode_struct.value.value_int, INIT_DECODE_STRUCT.value.value_int);
    EXPECT_EQ(decode_struct.value.value_float, INIT_DECODE_STRUCT.value.value_float);
    EXPECT_EQ(decode_struct.value.value_bool, INIT_DECODE_STRUCT.value.value_bool);
  }
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
