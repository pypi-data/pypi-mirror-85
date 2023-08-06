#!/bin/env python3
"""
Psi-calc is an algorithm for clustering protein multiple sequence alignments (MSAs)
utilizing normalized mutual information.

    Copyright (C) 2020 Thomas Townsley, MSSE, Joe Deweese, PhD., Kirk Durston, PhD., et. al.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact: thomas@mandosoft.dev, joe.deweese@lipscomb.edu, kirkdurston@gmail.com
"""

import re
import time
import csv
import pandas as pd
from itertools import combinations
from sklearn.metrics.cluster import normalized_mutual_info_score as nmis


def select_subset(df: pd.DataFrame, s: int):
    """Selects the width of the sample subset from the MSA"""
    each_nth_col = df[df.columns[::s]]
    return each_nth_col


def durston_schema(df: pd.DataFrame, value: int) -> pd.DataFrame:
    """Labels index based on first value given. For example making the value 3
    will label the columns 3-N."""
    df = df.drop_duplicates()
    df.columns = range(len(df.columns))
    label_val = value
    df = df.rename(columns=lambda x: int(x) + label_val)

    return df


def deweese_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Labels data based on the range on the first row of the MSA.
    For example, if the first row is labelled TOP2 YEAST/59-205, then all
    columns with individuals in the first row are kept and labeled 59-205."""
    df = df.drop_duplicates()
    try:
        df = df.rename(columns=lambda x: x - 1)
        first_row_ix = df.index[0]
        ix_label = first_row_ix.rsplit('/', 1)
        ix_label = ix_label[1]
        ix_label = ix_label.rsplit('-', 1)
        df_label = int(ix_label[0])
        column_lab_dict = dict()

        pattern = '^-'

        for i in df:
            if not re.search(pattern, df[i].iloc[0]):
                column_lab_dict[df.columns[i]] = df_label
                df_label += 1
            else:
                column_lab_dict[df.columns[i]] = ''
        df = df.rename(columns=column_lab_dict)
        df = df.drop(columns=[''])
        df = df.rename(columns=lambda x: int(x))
    except IndexError or KeyError:
        exit()
    return df


def read_txt_file_format(file) -> pd.DataFrame:
    """Reads FASTA files or text file-based MSAs into a dataframe."""
    nucs_dict = dict()
    with open(file, "r") as a_file:
        string_without_line_breaks = ""
        for line in a_file:
            stripped_line = line.rstrip()
            string_without_line_breaks += stripped_line
        a_file.close()

    vals = string_without_line_breaks.split('>')
    for line in vals:
        line = re.split('(\w+/\d*-?\d*)', line)
        line.remove('')
        for i in enumerate(line):
            g = list(line[1])
            nucs_dict.update({line[0]: g})

    df = pd.DataFrame.from_dict(nucs_dict, orient='index')
    df = df.replace({'.': '-'})
    df.index.name = 'SEQUENCE_ID'

    return df


def read_csv_file_format(file) -> pd.DataFrame:
    """Reads CSV MSAs into a dataframe."""
    df = pd.read_csv(file, encoding='utf-8', engine='c', header=None)
    df = df.rename(columns={df.columns[0]: 'SEQUENCE_ID'})
    df = df.set_index('SEQUENCE_ID', drop=True)

    return df


def return_pairwise_cluster(c: pd.DataFrame, list_store: list, pretty_list: list, k, csv_dict: dict) -> pd.DataFrame:
    """Calculates the sr_mode of a pairwise cluster and returns the cluster."""
    cc = len(list(combinations(c.columns, 2)))
    c = return_new_mode(c)
    if len(c.columns) < 2:
        return c
    elif len(c.columns) == 2:
        max_sum = nmis(c[c.columns[0]], c[c.columns[1]], average_method='geometric')
    else:
        max_sum = max([sum([nmis(c[i], c[j], average_method='geometric')
                            for location, j in enumerate(c) if location != loc]) for loc, i in enumerate(c)])

    sr_mode = max_sum / cc
    list_store.append([sr_mode, c])
    pretty_list.append([sr_mode, tuple(c)])
    csv_dict[tuple(sorted(tuple(c)))] = [round(sr_mode, 6), k]
    return c


def return_sr_mode(c: pd.DataFrame, csv_dict: dict, k) -> float:
    """Calculates the sr_mode of a cluster and returns the sr_mode."""
    cc = len(list(combinations(c.columns, 2)))
    if len(c.columns) == 2:
        max_sum = nmis(c[c.columns[0]], c[c.columns[1]], average_method='geometric')
    else:
        max_sum = max([sum([nmis(c[i], c[j], average_method='geometric')
                            for location, j in enumerate(c) if location != loc]) for loc, i in enumerate(c)])
    sr_mode = max_sum / cc
    csv_dict[tuple(sorted(tuple(c)))] = [round(sr_mode, 6), k]
    return sr_mode


def return_new_mode(c: pd.DataFrame) -> pd.DataFrame:
    """Calculates the new mode of a cluster and returns the updated cluster.
    The mode of a cluster is the left-most column in the dataframe."""
    max_sum = 0
    mode, m_ix = c[c.columns[0]], 0
    for loc, i in enumerate(c):
        sum_rii = 0
        for j in c:
            if c[i].name != c[j].name:
                sum_rii += nmis(c[i], c[j], average_method='geometric')
        if sum_rii > max_sum:
            max_sum, mode, m_ix = sum_rii, c[i], loc
    c = c.drop(c.columns[m_ix], axis=1)
    c = pd.concat([c, mode], axis=1)
    cols = c.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    c = c[cols]
    return c


def list_contains(list1, list2, capture_sets):
    """Finds clusters with overlapping attributes"""
    set1 = set(list1)
    for each in list2:
        set2 = set(each)
        if set1 != set2 and set1.intersection(set2):
            set1 = set1.union(set2)
        else:
            pass
    if set1 not in capture_sets:
        capture_sets.append(set1)


def map_identities(capture_set, dataframe, list1):
    """Re-maps cluster labels after overlapping values have been found."""
    series = pd.DataFrame()
    for label in capture_set:
        series = pd.concat([series, dataframe[label]], axis=1)
    list1.append(series)


def write_output_data(spread: int, csv_dict: dict):
    """Writes the CSV output file"""
    filename = "data_out_width" + str(spread) + ".csv"
    a_file = open(filename, "w")
    writer = csv.writer(a_file)
    writer.writerow(["Cluster", "Sr_mode", "Discovered"])
    for key, value in csv_dict.items():
        val1, val2 = value
        writer.writerow([key, val1, val2])
    a_file.close()


def find_clusters(spread: int, df: pd.DataFrame):
    """Discovers cluster sights with high shared normalized mutual information.
    Provide a dataframe and a sample spread-width and returns a CSV."""
    csv_dict = dict()
    k = "pairwise"
    start_time = time.time()
    hash_list = list()
    pretty_list = list()
    subset = select_subset(df, spread)

    cluster_list = [pd.DataFrame(df[i]) for i in df]
    subset_list = [pd.DataFrame(subset[i]) for i in subset]

    for item, each in enumerate(subset_list):
        max_rii = 0
        for location, cluster in enumerate(cluster_list):
            cluster_mode = cluster[cluster.columns[0]]
            subset_mode = each[each.columns[0]]
            if subset_mode.name != cluster_mode.name:
                rii = nmis(subset_mode, cluster_mode, average_method='geometric')
                if rii > max_rii:
                    max_rii, best_cluster = rii, location
        subset_list[item] = pd.concat([subset_list[item], cluster_list[best_cluster]], axis=1)

    for cluster in subset_list:
        return_pairwise_cluster(cluster, hash_list, pretty_list, k, csv_dict)
    sorted_list = sorted(hash_list, key=lambda x: x[0], reverse=True)
    N = int(len(sorted_list) * 1 / 3)
    out_list = sorted_list[:N]
    dataframe_label_list = [[col for col in j.columns] for x, j in out_list]

    # check for repeat attributes between pairwise clusters
    capture_list = list()
    for each in dataframe_label_list:
        list_contains(each, dataframe_label_list, capture_list)

    final_df_set = list()
    for eachset in capture_list:
        map_identities(eachset, df, final_df_set)

    unranked = list()
    post_aggregation = list()
    k = "post-agg"  # means clusters which were merged during post-aggregation
    for cluster in final_df_set:
        return_pairwise_cluster(cluster, unranked, post_aggregation, k, csv_dict)

    stg_ranked_list = sorted(unranked, key=lambda x: x[0], reverse=True)
    remove = [col for x, j in stg_ranked_list for col in j.columns]

    for k in remove:
        df = df.drop(k, axis=1)

    # Sets the number of clusters we're actually iterating over
    R = len(stg_ranked_list)

    for remaining in df:
        stg_ranked_list.append([0, pd.DataFrame(df[remaining])])

    # Stage Two
    k = len(stg_ranked_list)

    # Move through the pairs in the list
    # and find their best attribute
    print(len(stg_ranked_list))
    num_clusters = len(stg_ranked_list[0:R])

    while len(stg_ranked_list) >= 2:
        print("\nNumber of Clusters Remaining: ", num_clusters)
        i = 0
        while i < num_clusters:
            location = None
            cluster_mode = stg_ranked_list[i][1][stg_ranked_list[i][1].columns[0]]
            max_rii = 0
            for loc, entry in enumerate(stg_ranked_list):
                sr_mode, cluster = entry
                attr_mode = cluster[cluster.columns[0]]
                if cluster_mode.name != attr_mode.name:
                    rii = nmis(attr_mode, cluster_mode, average_method='geometric')
                    if rii > max_rii:
                        max_rii, best_cluster, location = rii, cluster, loc
            stg_ranked_list[i][1] = pd.concat([stg_ranked_list[i][1], best_cluster], axis=1)
            stg_ranked_list[i][1] = return_new_mode(stg_ranked_list[i][1])
            stg_ranked_list[i][0] = return_sr_mode(stg_ranked_list[i][1], csv_dict, k)
            stg_ranked_list.pop(location)
            i += 1
            k -= 1
            print("k = ", k)
            if len(stg_ranked_list) == 2:
                break
            if location <= num_clusters:
                num_clusters -= 1

        # Resort the list
        stg_ranked_list = sorted(stg_ranked_list, key=lambda x: x[0], reverse=True)
        print(" Next run at ", len(stg_ranked_list))

        if num_clusters <= 2:
            break

    print("--- took " + str(time.time() - start_time) + " seconds ---")

    write_output_data(spread, csv_dict)

