#include "generated_ucoms.h"
#include <gtest/gtest.h>

class test_uComsUtils : public testing::Test {
};

TEST_F(test_uComsUtils, getKeyTest) {
    for (int32_t host_key = kCommandNoneHost + 1; host_key < kLenCommandsHost; (int32_t)host_key++) {
        uComsCommandsDevice device_key = GetDeviceKey(static_cast<uComsCommandsHost>(host_key));
        EXPECT_LT(host_key, kLenCommandsDevice);
        EXPECT_GT(host_key, kCommandNoneDevice);
        EXPECT_EQ(host_key, device_key);
    }   
    for (int32_t device_key = kCommandNoneDevice + 1; device_key < kLenCommandsDevice; (int32_t)device_key++) {
        uComsCommandsDevice host_key = GetDeviceKey(static_cast<uComsCommandsHost>(device_key));
        EXPECT_EQ(host_key, device_key);
        EXPECT_LT(device_key, kLenCommandsHost);
        EXPECT_GT(device_key, kCommandNoneHost);
    }   
}

TEST_F(test_uComsUtils, getKeyStringTest) {
    // Have to start at None + 1 since none will return empty string
    for (int32_t host_key = kCommandNoneHost + 1; host_key < kLenCommandsHost; (int32_t)host_key++) {
        std::string test_string = GetHostKeyString((uComsCommandsHost)host_key);
        std::cout << test_string << std::endl;
        EXPECT_GT(test_string.length(), 0);
    }   
    for (int32_t device_key = kCommandNoneDevice + 1; device_key < kLenCommandsDevice; (int32_t)device_key++) {
        std::string test_string = GetDeviceKeyString((uComsCommandsDevice)device_key);
        std::cout << test_string << std::endl;
        EXPECT_GT(test_string.length(), 0);
    }   
}

TEST_F(test_uComsUtils, getCommandTypeTest) {
    // Have to start at None + 1 since none will return empty string
    for (int32_t host_key = kCommandNoneHost + 1; host_key < kLenCommandsHost; (int32_t)host_key++) {
        uComsCommandTypes type = GetCommandType((uComsCommandsHost)host_key);
        EXPECT_GT(type, kCommandTypeNone);
        EXPECT_LT(type, kLenCommandTypes);
    }   
    for (int32_t device_key = kCommandNoneDevice + 1; device_key < kLenCommandsDevice; (int32_t)device_key++) {
        uComsCommandTypes type = GetCommandType((uComsCommandsDevice)device_key);
        EXPECT_GT(type, kCommandTypeNone);
        EXPECT_LT(type, kLenCommandTypes);
    }   
}

int main(int argc, char **argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}