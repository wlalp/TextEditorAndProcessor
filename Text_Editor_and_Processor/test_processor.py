'''Unit test module for text processor'''
import unittest
from text_processor import TextProcessor


class TestProcessor(unittest.TestCase):
    '''Test class for the text processor'''
    def test_count_words(self):
        '''Tests the count_words() method'''
        ex_processor = TextProcessor('test7.txt')
        self.assertEqual(ex_processor.count_words(),8)

    def test_count_chars(self):
        '''Tests the count_chars() method'''
        ex_processor = TextProcessor('test7.txt')
        self.assertEqual(ex_processor.count_chars(),43)

    def test_count_occurence(self):
        '''Tests the count_occurence method'''
        ex_processor = TextProcessor('hobbit1.txt')
        self.assertEqual(ex_processor.count_occurences("hobbit"),5)
        self.assertEqual(ex_processor.count_occurences("hobbit"),ex_processor.count_occurences("HObBit"))

        self.assertTrue(ex_processor.count_occurences("non-existent-word") == 0)

    def test_top_ten(self):
        '''Tests the top_most_frequent method'''
        ex_processor = TextProcessor('hobbit1.txt')
        self.assertEqual(len(ex_processor.top_most_frequent()),10)
        ex_processor2 = TextProcessor('test7.txt')
        self.assertFalse(len(ex_processor2.top_most_frequent())==10)

if __name__ == "__main__":
    unittest.main()