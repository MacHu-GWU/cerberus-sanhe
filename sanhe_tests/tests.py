#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, date
import cerberus
import unittest
import pickle

class SanheUnittest(unittest.TestCase):
    def setUp(self):
        schema = {
            "a_date": {
                "type": "date", 
                "after": date(2000, 1, 1), "before": date(2015, 1, 1),
            },
            "a_datetime": {
                "type": "datetime",
                "after": datetime(2000, 1, 1), "before": datetime(2015, 1, 1),
            },
            "a_bytes": {
                "type": "bytes",
                "minsize": 100, "maxsize": 1000,
            },
        }
        self.v = cerberus.Validator(schema)
        
    def test_date(self):
        """If date can pass the test, then datetime also should.
        """
        self.assertFalse(self.v.validate({"a_date": "2010-01-01"}))
        self.assertTrue(self.v.validate({"a_date": date(2010, 1, 1)}))
        self.assertFalse(self.v.validate({"a_date": date(1990, 1, 1)}))
        self.assertEqual(self.v.errors["a_date"], 
                         "min value is datetime.date(2000, 1, 1)")
        self.assertFalse(self.v.validate({"a_date": date(2020, 1, 1)}))
        self.assertEqual(self.v.errors["a_date"], 
                         "max value is datetime.date(2015, 1, 1)")
    
    def test_bytes(self):
        self.assertFalse(self.v.validate({"a_bytes": "abcdefg"}))
        self.assertTrue(self.v.validate({"a_bytes": b"abcdefg" * 100}))
        
        value = pickle.dumps({i: i for i in range(1)})
        self.assertFalse(self.v.validate({"a_bytes": value}))
        self.assertEqual(self.v.errors["a_bytes"],
                         "min size is 100 bytes")
     
        value = pickle.dumps({i: i for i in range(1000)})
        self.assertFalse(self.v.validate({"a_bytes": value}))
        self.assertEqual(self.v.errors["a_bytes"],
                         "max size is 1000 bytes")

if __name__ == "__main__":
    unittest.main()