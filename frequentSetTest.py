#/usr/bin/env python
#-*- coding: UTF-8 -*-
#__author__ = 'shuai'

####
import json
from itertools import combinations, permutations
from pprint import pprint

def load_data():
    """
    load data from json file
    """
    dataFile = open('transactions.json', 'r')
    data = json.load(dataFile)
    transactions = data['transactions']#TID
    items = data['items']#item sets
    return items, transactions


def gen_L1(items, transactions):
    """
    generate L1
    """
    frequentItemSet = [{} for x in range(len(items))]
    frequentItems = {}
    count = 0
    for item in items:
        for trans in transactions:
            if item in trans['itemId']:
                count += 1
        temp = [item]
        if count >= 2:
            frequentItems[frozenset(temp)] = count
        count = 0
    frequentItemSet[0] = frequentItems
    L1 = frozenset(frequentItemSet[0].keys())

    return L1, frequentItemSet


def apriori_gen(Ls):
    """
    generate Ck for Apriori
    """
    Lks = Ls[len(Ls) -1] #L(k-1)
    LLength = len(Ls)
    Lc = combinations(Lks, r = LLength+1)
    fs = frozenset([i for i in Lc])

    Ck =[] #L(k)
    for s in fs:
        ckItem = frozenset()
        for ss in s:
            ckItem = ckItem.union(ss)
        if not has_infrequent_subset(ckItem, Lks):
            Ck.append(ckItem)

#    print "Ck:",Ck
    return Ck


def has_infrequent_subset(Ck, Lks):
    """
    check whether a candidate set has infrequent subset
    """
    ksSubset = combinations(Ck, r=len(Ck)-1)
    for ks in ksSubset:
        if not Lks.issuperset([frozenset(ks)]):
            return True
    return False

def supportCk(ckItem, transactions):
    """
    count support for ckItem
    """
    count = 0
    for trans in transactions:
        if ckItem.issubset(frozenset(trans['itemId'])):
            count += 1
    return count


def supportItemSet(itemSet, frequentItemSets):
    """

    """
    for itemSets in frequentItemSets:
        if itemSet in itemSets.keys():
            return itemSets[frozenset(itemSet)]

def ar_gen(frequentItemSets):
    """
    generate association rules from frequentItemSet
    """
#    print frequentItemSets
    for fItemSet in frequentItemSets:
        if fItemSet:
            itemSets = fItemSet.keys()
            for itemSet in itemSets:
                subsets = subset_gen(itemSet)
#                print itemSet
#                print subsets
                if subsets:
                    for subset in subsets:
                        sptSubSet = supportItemSet(subset, frequentItemSets)
                        sptSubSets = supportItemSet(itemSet, frequentItemSets)
                        print subset,'->', itemSet.difference(subset), 'confidence=',sptSubSets/float(sptSubSet)


def subset_gen(itemSet):
    """
    generate all proper subsets excluding empty set
    """
    subsets = []
    for i in range(1, len(itemSet)):
        c = combinations(itemSet, r=i)
        for cc in c:
            subsets.append(set(cc))
    return subsets

def main():
    """

    """
    items, transactions = load_data()
    L1, frequentItemSet = gen_L1(items, transactions)
#    print "frequentItemSet: ", frequentItemSet
#    print "transactions: ", transactions
    Ls = [L1] #L(1)~L(k)
    for k in range(1, len(items)):
        Ck = apriori_gen(Ls)
        for c in Ck[:]:
            spt = supportCk(c, transactions)
            if spt<2:
                Ck.remove(c)
                continue
            else:
                frequentItemSet[k][frozenset(c)] = spt
        Ls.append(frozenset(Ck))

    ar_gen(frequentItemSet)
#    print len(Ls)
#    pprint(Ls)
#    print "frequentItemSet: ", frequentItemSet

#    associationRules = []
#    for i in range(1, len(frequentItemSet)):
#        for s in frequentItemSet[i].keys():
#            c = combinations(s, r=i+1)
#            for  cc in c:
#                print cc,

if __name__ == '__main__':
    main()