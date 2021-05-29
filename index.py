import csv
from item import item_id
from typing import Iterable


class InvertedIndex:
    def __init__(self):
        self.index = dict()
        self.num_transactions = 0

    def add(self, transaction: Iterable[int]):
        self.num_transactions += 1
        for item in transaction:
            if item not in self.index:
                self.index[item] = set()
            self.index[item].add(self.num_transactions)

    def load(self, data: str):
        for transaction in filter(bool, data.splitlines()):
            itemset = list(set(map(item_id, transaction.split(","))))
            if itemset:
                self.add(itemset)

    def items(self):
        return self.index.keys()

    def count(self, itemset: Iterable[int]):
        return len(set.intersection(*[self.index[i]
                                      for i in itemset]))

    def support(self, itemset):
        return self.count(itemset) / self.num_transactions

    def __len__(self):
        return self.num_transactions
