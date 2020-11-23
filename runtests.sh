set -e
pytest-3
cmake CMakeLists.txt
make
./tests/decodeTest.test