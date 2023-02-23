#!/usr/bin/env python3
import matplotlib
matplotlib.use('Agg')

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
parser.add_argument('--output_folder',default='plots')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

#stores the top 10 - sorted by value
top_10 = sorted(sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)[:10], key=lambda x: x[1])

key = []
val = []
for k, v in top_10: 
    key.append(k)
    val.append(v)


#create bar graph 

plt.bar(key, val)

#if reduce.lang 
if args.input_path == "reduced.lang":
    plt.xlabel("Language")
    plt.ylabel("Count")
    plt.title("Number of " + args.key + " tweets across Languages")

#if reduce.country 
if args.input_path == "reduced.country":
    plt.xlabel("Country")
    plt.ylabel("Count")
    plt.title("Number of " + args.key + " tweets in Countries")


#make output folder
try:
    os.makedirs(args.output_folder)
except FileExistsError:
    pass

output_path_base = os.path.join(args.output_folder,os.path.basename(args.input_path) + '.' + os.path.basename(args.key))

print("output_path_base for plot is ", output_path_base)

#save plot to plots folder 
try:
    plt.savefig(output_path_base + '.png')
except:
    print('error saving plot')
