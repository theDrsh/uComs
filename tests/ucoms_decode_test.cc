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

TEST_F(test_uComsDecode, fooTest) {
}

TEST_F(test_uComsDecode, spewTest) {
  for (int i = 0; i < kLenTestKeys; i++) {
    // Testing that I can fill in a string like this
    char test_string[256];
    sprintf(test_string, TestCommandOutputValues[i].c_str(), i);
    std::cout << "TEST:" << i
              << " IN:" << TestCommandInputValues[i] 
              << " OUT:" << test_string << std::endl;
  }
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
