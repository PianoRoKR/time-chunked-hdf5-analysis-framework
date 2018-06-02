# Time Chunked HDF5 Analysis Framework
Note: This is not an officially supported Google product.

## Purpose

This framework is designed to help with analysis of large groups of HDF5
files. By providing a method of extracting events and time info for these files,
the framework will split the files into chunks of the specified time span. It
will then process the chunks and aggregate the results. 

## Required Modules

The HDF5 file processing is handled by the [h5py](https://www.h5py.org/)
library. All other modules are included in the standard python3 library.

h5py can be installed by using pip:
```
pip3 install h5py
```

## Usage
The end user needs to implement the following methods in main.py:
```python
findEvents(fast5)
findTime(events, idx)
process_file(events)
reduce_results(file_details,main_details)
```
See comments in the code for their particular usages.

`OUT_FIELD_NAMES` determines the names of the output fields for the CSV.

`SEARCH_PATH` determines where to find the HDF5 files. By default, it searches
the directory `main.py` is launched from.

`CHUNK_SIZE_IN_TICKS` determines the size in ticks that the framework should
use to chunk the HDF5 files. This should be a unit related to the time returned
by the `findTime` function.

After implementing these methods and installing the h5py module, running main.py
will generate `output.csv` with the resulting analysis.
