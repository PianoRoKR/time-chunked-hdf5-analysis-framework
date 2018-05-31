# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Searches through a specified file path, applying a process to a file and aggregating
results over a series of time chunks """

from glob import glob
import numpy as np
import h5py
import math 
import time
import csv
import operator

CHUNK_SIZE = 30
OUT_FIELD_NAMES = []
SEARCH_PATH = "./*.fast5"

def display_percent(chunk_size, chunk_percent, last_percent, progress):

    """
    Used to monitor progress of a process. Example usage:

        Progress = 0
        chunk_percent = 10.0
        chunk_size = int(math.ceil(all_files*(chunk_percent/100)))

        for x in all_files:
            Progress += 1 
            last_percent = display_percent(chunk_size, chunk_percent, last_percent, Progress)
    """

    percent = int(progress / chunk_size)

    if percent > last_percent:
        print("{0}%".format(percent * chunk_percent))

    return percent

def colease(n):
    return 1 if n == 0 else n


def process_file(file):

def reduce_results(file_details, main_details):

def process_chunk(files, start_time):

    event_details = {}

    for f in files:
        with h5py.File(f[0], 'r') as hdf:
            
            Events = findEvents(hdf)
            file_details = process_file(Events)

    event_details = reduce_results(file_details, event_details)

    return event_details

def get_file_chunks(sorted_dict, chunk_size_in_sec):
    start_chunk = 0
    end_chunk = 0
    chunked_files = []
    total_events = len(sorted_dict)
    time1 = sorted_dict[start_chunk][1]
    search_time = int(time1)

    while start_chunk < total_events - 1:
        search_time += chunk_size_in_sec

        if sorted_dict[start_chunk][1] > search_time:
            continue

        end_chunk = start_chunk + 1

        while end_chunk != total_events - 1 and sorted_dict[end_chunk][1] < search_time:
            end_chunk += 1

        curr_chunk = sorted_dict[start_chunk:(end_chunk + 1)]

        chunked_files.append([curr_chunk, search_time - chunk_size_in_sec])

        start_chunk = end_chunk + 1

    if start_chunk == total_events - 1:
        chunked_files.append([[sorted_dict[start_chunk]], search_time - chunk_size_in_sec])

    return chunked_files

def main():
    print("Searching for fast5 files...")
    files = glob(SEARCH_PATH, recursive=True)
    num_of_files = len(files)
    print("Constructing dictionary of file start times...")
    start_times = {}
    files_not_processed = []

    for fast5 in files:
        try:
            with h5py.File(fast5,'r') as hdf:
                events = findEvents(hdf)
                start_times[fast5] = findTime(events, 0)

        except Exception as e:
            print("Error processing {}.".format(fast5))
            files_not_processed.append(fast5)

    sorted_start_times = sorted(start_times.items(), key=operator.itemgetter(1))
    print("Finished")
    print("Splitting up files into corrosponding chunks of {} seconds".format(CHUNK_SIZE))
    chunks = get_file_chunks(sorted_start_times, CHUNK_SIZE)
    
    print("Found {} chunks.".format(len(chunks)))

    total_events = 0

    details = []
    with open('output.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=OUT_FIELD_NAMES)

        writer.writeheader()

        for chunk in chunks:
            print("Processing chunk {0} of {1} with {2} files...".format(i + 1, len(chunks), len(chunk[0])))
            try:
                curr_detail = process_chunk(chunk[0], chunk[1])
                writer.writerow(curr_detail)
            except Exception as e:
                print("Error processing chunk {}".format(i))
            else:
                print('processed')
        print("Finished processing chunks.")

def findEvents(fast5):
    return None
           
def findTime(events, idx):
    return None

main()
