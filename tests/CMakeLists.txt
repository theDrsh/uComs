cmake_minimum_required(VERSION 3.10.2)
 
# Locate GTest
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})
 
add_executable(decodeTest.test ucoms_decode_test.cc)
target_include_directories(decodeTest.test PUBLIC ../generated_files/)
target_link_libraries(decodeTest.test ${GTEST_LIBRARIES} pthread)