from collections import Counter
import pandas as pd


class Node:

    def __init__(self, value, left=None, right=None):
        self.right = right
        self.left = left
        self.value = value


def count_string(string):
    string_count = Counter(string)

    if len(string_count) < 1:
        raise AssertionError('Введите что-нибудь')

    elif len(string_count) == 1:
        node = Node(None)
        for i in string_count:
            node.left = Node([i][0])
        node.right = Node(None)

        string_count = {node: 1}

    if len(string_count) > 1:
        while len(string_count) != 1:
            node = Node(None)
            string_count_2 = string_count.most_common()[:-3:-1]

            if isinstance(string_count_2[0][0], str):
                node.left = Node(string_count_2[0][0])

            else:
                node.left = string_count_2[0][0]

            if isinstance(string_count_2[1][0], str):
                node.right = Node(string_count_2[1][0])

            else:
                node.right = string_count_2[1][0]

            del string_count[string_count_2[0][0]]
            del string_count[string_count_2[1][0]]
            string_count[node] = string_count_2[0][1] + string_count_2[1][1]

    return [i for i in string_count][0]


def coding(origin, codes={}, space=''):

    if origin is None:
        return

    if isinstance(origin.value, str):
        codes[origin.value] = space
        return codes

    coding(origin.left, codes, space + '0')
    coding(origin.right, codes, space + '1')

    return codes


def final_step(string):
    tree = count_string(string)
    final = coding(tree)
    final = (pd.DataFrame(list(final.items()), columns=['Символ', 'Значение']))
    return final


string = 'Hello! How are you? What are you doing?'
print(final_step(string))
