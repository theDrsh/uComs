import microplot
import unittest

class TestMicroPlot(unittest.TestCase):


    def test_instantiation(self):
        mp = microplot.MicroPlot("example_protocol.yml")
        try:
            mp2 = microplot.MicroPlot("")
        except SystemExit as e:
            print("Caught %s as expected" % (e))

if __name__ == "__main__":
    unittest.main()
