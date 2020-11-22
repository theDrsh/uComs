cmake_minimum_required (VERSION 3.10.2)
project (uComs)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -O3 -g")

add_subdirectory(generated_files)
add_subdirectory(tests)