import unittest
import os
import count_verbs as cv


class TestCountVerbsMethods(unittest.TestCase):

    def test_file_names_from_path(self):
        file_names = cv.get_file_names(os.path.join('test_data/django'))
        file_names.sort()
        self.assertEqual(file_names, ['test_data/django/__init__.py',
                                      'test_data/django/error.py',
                                      'test_data/django/make.py',
                                      'test_data/django/test.py']
                         )
        file_names = cv.get_file_names(os.path.join('test_data/empty'))
        self.assertEqual(file_names, ['test_data/empty/__init__.py'])

    def test_function_names_from_path(self):
        path = os.path.join('test_data/django')
        file_names = cv.get_file_names(path)
        files_syntax_trees = cv.get_syntax_trees(file_names)
        function_names = cv.get_all_function_names(files_syntax_trees)
        self.assertEqual(function_names, ['make', 'get', 'take', '__author__', 'get_to_it'])

    def test_remove_special_names(self):
        list_to_filter = ['__remove__', '__remove2__', 'leave_this', '_leave']
        filtered_list = cv.remove_special_names(list_to_filter)
        self.assertEqual(filtered_list, ['leave_this', '_leave'])


if __name__ == '__main__':
    unittest.main()
