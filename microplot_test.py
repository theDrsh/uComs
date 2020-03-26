import microplot
import unittest
import yaml


class TestMicroPlot(unittest.TestCase):

    def test_instantiation(self):
        unused_mp = microplot.MicroPlot("example_protocol.yml")
        print(unused_mp)
        try:
            unused_mp2 = microplot.MicroPlot("")
            print(unused_mp2)
        except SystemExit as e:
            print("Caught %s as expected" % (e))

    def test_commands(self):
        mp = microplot.MicroPlot("example_protocol.yml")
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
        mp = microplot.MicroPlot("example_protocol.yml")
        mp.generate(False, False)
        mp.generate(False, True)
        mp.generate(True, False)
        mp.generate(True, True)


if __name__ == "__main__":
    unittest.main()
