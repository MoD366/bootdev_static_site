import unittest

from helper import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_titles(self):
        md1 = "# This is a headline 1."
        md2 = "## This is a headline 2."
        md3 = "#       This headline has way too many whitespaces."
        self.assertEqual("This is a headline 1.", extract_title(md1))
        with self.assertRaises(Exception) as cm:
            extract_title(md2)
        self.assertEqual(str(cm.exception), "There is no h1 header in the given Markdown")
        self.assertEqual("This headline has way too many whitespaces.", extract_title(md3))