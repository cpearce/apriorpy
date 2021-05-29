from typing import List, Tuple, Set
from index import InvertedIndex
import math


# Returns list of tuples containing the itemset (list of int) and their
# count (int)
def apriori(index: InvertedIndex,
            minsup: float) -> List[Tuple[List[int], int]]:
    min_count = math.ceil(minsup * len(index))
    candidates = initial_candidates(index, min_count)
    results = candidates
    itemset_size = 1
    while len(candidates) > 0:
        print(f"Generating itemsets of size {itemset_size}")
        generation = generate(candidates, index, min_count)
        print(f"Generated {len(generation)} itemsets of size {itemset_size}")
        itemset_size += 1
        results.extend(generation)
        candidates = generation
    return results


def generate(
    candidates: List[Tuple[List[int], int]],
    index: InvertedIndex,
    min_count: int,
) -> List[Tuple[List[int], int]]:
    # Create a lookup of the candidates in the previous generation.
    previous_generation: Set[Tuple[int, ...]] = set(
        tuple(t[0]) for t in candidates)

    generation: List[Tuple[List[int], int]] = []
    for i, a in enumerate(candidates):
        for b in candidates[i + 1:]:
            a_items = a[0]
            b_items = b[0]
            if not prefix_match(a_items, b_items):
                break
            candidate = a_items + [b_items[-1]]
            if contains_all_subsets(candidate, previous_generation):
                count = index.count(candidate)
                if count >= min_count:
                    generation.append((candidate, count))
    return generation


def initial_candidates(index: InvertedIndex,
                       min_count: int) -> List[Tuple[List[int], int]]:
    candidates = []
    for item in sorted(index.items()):
        count = index.count([item])
        if count >= min_count:
            candidates.append(([item], count))
    return candidates


def prefix_match(a: List[int], b: List[int]) -> bool:
    return a[0: -1] == b[0: -1]


def contains_all_subsets(
        candidate: List[int], previous_generation: Set[Tuple[int, ...]]) -> bool:
    for i in range(len(candidate)):
        subset = tuple(candidate[: i] + candidate[i + 1:])
        if subset not in previous_generation:
            return False
    return True
