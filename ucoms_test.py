import ucoms
import unittest
import yaml


class TestuComs(unittest.TestCase):

    def test_instantiation(self):
        unused_uc = ucoms.uComs("example_protocol.yml")
        print(unused_uc)
        try:
            unused_uc2 = ucoms.uComs("")
            print(unused_uc2)
        except SystemExit as e:
            print("Caught %s as expected" % (e))

    def test_commands(self):
        mp = ucoms.uComs("example_protocol.yml")
        with open("test.yml") as file_pointer:
            yaml_data = yaml.full_load(file_pointer)
        iteration = 0
        for command in yaml_data['test_commands']:
            response = mp.parse(yaml_data['test_commands'][command])
            self.assertNotEqual(None, response)
            self.assertEqual(command, list(response.keys())[0])
            if "Analog" in list(response.keys())[0]:
                self.assertEqual(response[command], 1000 + iteration)
            elif "Digital" in response.keys():
                self.assertEqual(response[command], (-100 - iteration + 9))
            iteration += 1

    def test_generate(self):
        uc = ucoms.uComs("example_protocol.yml")
        uc.generate(False, False)
        uc.generate(False, True)
        uc.generate(True, False)
        uc.generate(True, True)


if __name__ == "__main__":
    unittest.main()
