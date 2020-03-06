import microplot
import logging
import unittest
import yaml

class TestMicroPlot(unittest.TestCase):


    def test_instantiation(self):
        mp = microplot.MicroPlot("example_protocol.yml")
        try:
            mp2 = microplot.MicroPlot("")
        except SystemExit as e:
            print("Caught %s as expected" % (e))
    def test_commands(self):
        mp = microplot.MicroPlot("example_protocol.yml")
        with open("test.yml") as file_pointer:
            yaml_data = yaml.load(file_pointer)
        for command in yaml_data['test_commands']:
            response = mp.parse(yaml_data['test_commands'][command])
            self.assertNotEqual(None, response)
            self.assertEqual(command, list(response.keys())[0])



if __name__ == "__main__":
    unittest.main()
