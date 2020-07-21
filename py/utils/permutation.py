from collections import Counter

def is_permutation(list1, list2):
    return Counter(list1) == Counter(list2)
