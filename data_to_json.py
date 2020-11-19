#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 11:45:50 2020

@author: clarekirkland
"""

import csv
import pandas as pd
from collections import defaultdict


def ctree():
    """ One of the python gems. Making possible to have dynamic tree structure.

    """
    return defaultdict(ctree)


def build_leaf(name, leaf):
    """ Recursive function to build desired custom tree structure

    """
    res = {"name": name}

    # add children node if the leaf actually has any children
    if len(leaf.keys()) > 0:
        res["children"] = [build_leaf(k, v) for k, v in leaf.items()]

    return res


def main():
    """ The main thread composed from two parts.

    First it's parsing the csv file and builds a tree hierarchy from it.
    Second it's recursively iterating over the tree and building custom
    json-like structure (via dict).

    And the last part is just printing the result.

    """
    tree = ctree()
    # NOTE: you need to have test.csv file as neighbor to this file
    with open('PPP_data_150k_plus_vis2.csv') as csvfile:
        reader = csv.reader(csvfile)
        
        #Count instances
        reader_df = pd.DataFrame(reader)
        #Drop header
        reader_df = reader_df.iloc[1:]
        reader_df.columns = ['BusinessType', 'Range']
        reader_df = reader_df.groupby(['BusinessType', 'Range']).size().to_frame('Count').reset_index()
        print(reader_df)
        
        reader_df.to_csv('new_csv.csv', index=False)
        with open('new_csv.csv') as new_csvfile:
            reader = csv.reader(new_csvfile)
            
            for rid, row in enumerate(reader):
        
                # skipping first header row. remove this logic if your csv is
                # headerless
                if rid == 0:
                    continue
        
                # usage of python magic to construct dynamic tree structure and
                # basically grouping csv values under their parents
                leaf = tree[row[0]]
                for cid in range(1, len(row)):
                    leaf = leaf[row[cid]]

    # building a custom tree structure
    res = []
    for name, leaf in tree.items():
        res.append(build_leaf(name, leaf))

    # printing results into the terminal
    import json
    
    with open('PPP_data_150k_plus.json', 'w') as json_file:
        json.dump(res, json_file, indent=4)
    
    print(json.dumps(res, indent=4))


# so let's roll
main()