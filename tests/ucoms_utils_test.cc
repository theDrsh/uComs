#include "generated_ucoms.h"
#include <gtest/gtest.h>

class test_uComsUtils : public testing::Test {
};

TEST_F(test_uComsUtils, getKeyTest) {
    for (int32_t host_key = kCommandNoneHost; host_key < kLenCommandsHost; (int32_t)host_key++) {
        uComsCommandsDevice device_key = GetDeviceKey(static_cast<uComsCommandsHost>(host_key));
        EXPECT_EQ(host_key, (int32_t)device_key);
    }   
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}