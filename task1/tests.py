import unittest
import os
import count_verbs as cv


class TestCountVerbsMethods(unittest.TestCase):

    def test_file_names_from_path(self):
        file_names = cv.get_file_names(os.path.join('test_data/django'))
        self.assertEqual(file_names, ['test_data/django/hui.py', 'test_data/django/__init__.py', 'test_data/django/test.py', 'test_data/django/make.py'])
        file_names = cv.get_file_names(os.path.join('test_data/empty'))
        self.assertEqual(file_names, ['test_data/empty/__init__.py'])

    def test_function_names_from_path(self):
        path = os.path.join('test_data/django')
        file_names = cv.get_file_names(path)
        files_syntax_trees = cv.get_syntax_trees(file_names)
        function_names = cv.get_all_function_names(files_syntax_trees)
        self.assertEqual(function_names, ['make', 'get', 'take', '__author__', 'get_to_it'])

if __name__ == '__main__':
    unittest.main()