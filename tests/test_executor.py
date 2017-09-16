import unittest
import os

from pydown.executor import opentraining_executor
from pydown.executor import say_hello
from pydown.executor import download_opentrain_from_json

class ExecutorTests(unittest.TestCase):
    def test_opentrain(self):
        #say_hello()
        #opentraining_executor()
        self.assertTrue(True)
    
    def test_read_json(self):
        download_opentrain_from_json("result.json")
        self.assertTrue(False)

        

if __name__ == '__main__':
    unittest.main()