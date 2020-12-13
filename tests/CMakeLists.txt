cmake_minimum_required(VERSION 3.10.2)
set(CMAKE_BUILD_TYPE Debug)
 
# Locate GTest
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})
 
 add_library(uComsDecode STATIC ../generated_files/generated_ucoms_decode.cc ../generated_files/generated_ucoms.cc)
add_executable(decodeTest.test ucoms_decode_test.cc)
target_include_directories(decodeTest.test PUBLIC ../generated_files/)
target_link_libraries(decodeTest.test ${GTEST_LIBRARIES} pthread uComsDecode)


 add_library(uComsUtils STATIC ../generated_files/generated_ucoms.cc)
add_executable(utilsTest.test ucoms_utils_test.cc)
target_include_directories(utilsTest.test PUBLIC ../generated_files/)
target_link_libraries(utilsTest.test ${GTEST_LIBRARIES} pthread uComsUtils)