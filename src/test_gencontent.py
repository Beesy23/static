import unittest
from gencontent import *

class TestExtractTitle(unittest.TestCase):

    def test_extract_title(self):
        title1 = "# Simple title\nSome content"
        title2 = "# Title with extra spaces\nContent"
        title3 = "## This is an h2\n# This is an h1"
        title4 = "Content\nMore content\n# Title at the end"
        title5 = "No title here"
        result1 = extract_title(title1)
        result2 = extract_title(title2)
        result3 = extract_title(title3)
        result4 = extract_title(title4)

        self.assertEqual(result1, "Simple title")
        self.assertEqual(result2, "Title with extra spaces")
        self.assertEqual(result3, "This is an h1")
        self.assertEqual(result4, "Title at the end")
        with self.assertRaises(Exception):
            extract_title(title5)
      
if __name__ == "__main__":
    unittest.main()