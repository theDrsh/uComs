import microplot
import unittest

class TestMicroPlot(unittest.TestCase):


    def test_instantiation(self):
        mp = microplot.MicroPlot("example_protocol.yml")

if __name__ == "__main__":
    unittest.main()
