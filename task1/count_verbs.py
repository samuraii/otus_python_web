import ast
import os
import collections
import nltk


def make_list_flat(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def get_file_content(filename):
    with open(filename, 'r', encoding='utf-8') as file_handler:
        return file_handler.read()


def is_verb(word):
    if not word:
        return False
    pos_info = nltk.pos_tag([word])
    return pos_info[0][1] == 'VB'


def split_snake_case_name_to_words(name):
    return [n for n in name.split('_') if n]


def get_file_names(path_to_dir):
    filenames = []
    for dirname, dirs, files in os.walk(path_to_dir, topdown=True):
        for file in files:
            if file.endswith('.py'):
                filenames.append(os.path.join(dirname, file))
            if len(filenames) == 100:
                break
    return filenames


def get_syntax_trees(filenames, with_filenames=False, with_file_content=False):
    trees = []

    for filename in filenames:
        file_content = get_file_content(filename)

        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            continue

        if with_filenames:
            if with_file_content:
                trees.append((filename, file_content, tree))
            else:
                trees.append((filename, tree))
        else:
            trees.append(tree)
    return trees


def get_all_functions_from_tree(tree):
    return [node.name.lower() for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]


def remove_special_names(function_names_list):
    return [name for name in function_names_list if not (name.startswith('__') and name.endswith('__'))]


def verbs_from_function_name(function_name):
    return [word for word in function_name.split('_') if is_verb(word)]


def get_all_function_names(trees):
    name_lists = [get_all_functions_from_tree(tree) for tree in trees]
    return make_list_flat(name_lists)


def get_all_verbs(function_names_list):
    verb_lists = [verbs_from_function_name(function_name) for function_name in function_names_list]
    return make_list_flat(verb_lists)


def get_top_verbs(name_list, top_size=10):
    user_defined_names_list = remove_special_names(name_list)
    all_verbs = get_all_verbs(user_defined_names_list)
    return collections.Counter(all_verbs).most_common(top_size)


if __name__ == '__main__':
    wds = []
    projects = [
        'test_data/django',
        'test_data/flask',
        'test_data/empty'
    ]
    for project in projects:
        path = os.path.join(project)
        file_names = get_file_names(path)
        files_syntax_trees = get_syntax_trees(file_names)
        function_names = get_all_function_names(files_syntax_trees)
        print(function_names)
        verbs = get_all_verbs(function_names)
        wds += get_top_verbs(verbs)

    top_size = 200
    print('total %s words, %s unique' % (len(wds), len(set(wds))))
    for word, occurrence in collections.Counter(wds).most_common(top_size):
        print(word, occurrence)
