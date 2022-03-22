import unittest

from src.runner.Loader import TraceLoader
from src.runner.Comparator import Comparator

class MyTestCase(unittest.TestCase):

    def test_read_trace(self):
        path = "/Users/Nann/eclipse-workspace/mobileCameras/trace/sample.txt"
        loader = TraceLoader("")
        traces = loader.read_trace(path)
        comparator = Comparator("action")
        comparator.compare(traces[1:10], traces[2:10])


if __name__ == '__main__':
    unittest.main()
