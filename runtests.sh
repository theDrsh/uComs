set -e
python3 ucoms_test.py
cmake CMakeLists.txt
make
./tests/decodeTest.test
./tests/utilsTest.test