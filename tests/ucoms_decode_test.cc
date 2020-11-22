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

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
