from apriori import prefix_match
from apriori import generate, initial_candidates
from index import InvertedIndex
from apriori import apriori


TEST_DATASET_1 = """
1,2,3,4,5,6
7,8,9,10,11,12
13,14
13,14
13,14,15
13,14,15,9
"""


def test_index_count():
    index = InvertedIndex()
    index.load(TEST_DATASET_1)
    expected = [
        ([1], 1),
        ([2], 1),
        ([3], 1),
        ([4], 1),
        ([5], 1),
        ([6], 1),
        ([7], 1),
        ([8], 1),
        ([9], 2),
        ([10], 1),
        ([11], 1),
        ([12], 1),
        ([13], 4),
        ([14], 4),
        ([15], 2),
        ([13, 14], 4),
        ([13, 14, 15], 2),
    ]
    for (itemset, expected_count) in expected:
        observed_count = index.count(itemset)
        assert(observed_count == expected_count)


def test_generate():
    index = InvertedIndex()
    index.load(TEST_DATASET_1)
    assert(index.count([6]) == 1)
    min_count = 2
    candidates = initial_candidates(index, min_count)
    assert(candidates == [([9], 2), ([13], 4), ([14], 4), ([15], 2)])

    candidates = generate(candidates, index, min_count)
    expected = [([13, 14], 4), ([13, 15], 2), ([14, 15], 2)]
    assert(candidates == expected)

    candidates = generate(candidates, index, min_count)
    expected = [([13, 14, 15], 2)]
    assert(candidates == expected)

    candidates = generate(candidates, index, min_count)
    expected = []
    assert(candidates == expected)


def test_prefix_match():
    cases = [
        ([1], [2], True),
        ([1, 2, 3], [1, 2, 4], True),
        ([4, 5, 6], [1, 2, 4], False),
        ([13, 14], [13, 15], True),
        ([13, 14], [14, 15], False),
        ([13, 15], [14, 15], False),
    ]
    for (a, b, expected) in cases:
        observed = prefix_match(a, b)
        assert(observed == expected)


def test_apriori():
    expected = [
        ([9], 2), ([13], 4), ([14], 4), ([15], 2),
        ([13, 14], 4), ([13, 15], 2), ([14, 15], 2),
        ([13, 14, 15], 2),
    ]

    index = InvertedIndex()
    index.load(TEST_DATASET_1)
    itemsets = apriori(index, 2 / 6)
    assert(itemsets == expected)
