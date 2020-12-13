set -e
pytest
cmake CMakeLists.txt
make
./tests/decodeTest.test
./tests/utilsTest.test