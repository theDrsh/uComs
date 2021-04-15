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

    def test_reply_parse(self):
        mp = ucoms.uComs("example_protocol.yml")
        with open("test.yml") as file_pointer:
            yaml_data = yaml.full_load(file_pointer)
        iteration = 0
        d_counter = True
        for command in yaml_data['test_reply']:
            response = mp.parse(yaml_data['test_reply'][command])
            self.assertNotEqual(None, response)
            self.assertEqual(command, list(response.keys())[0])
            if "Analog" in list(response.keys())[0]:
                self.assertEqual(response[command], 1000 + iteration)
            elif "Digital" in response.keys():
                self.assertEqual(response[command], int(d_counter))
                d_counter = not d_counter
            iteration += 1

    def test_generate(self):
        uc = ucoms.uComs("example_protocol.yml")
        uc.generate(False)
        uc.generate(True)


if __name__ == "__main__":
    unittest.main()
