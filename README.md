# summarize
A commandline tool to summarize file data.
Before executing the script for the first time, run the setup.py file to resolve library dependencies.

```
Usage: summarize.py [options]

Summarize information

Options:
  -h, --help            show this help message and exit
  --summary_type=SUMMARY_TYPE
                        Type of summary
  --file_type=FILE_TYPE
                        Type of input file
  --graph_type=GRAPH_TYPE
                        Type of graph
  --label_regex=LABEL_REGEX
                        Regex to search for
  --legend_regex=LEGEND_REGEX
                        Regex to search for
  --label_column_index=LABEL_COLUMN_INDEX
                        Column index for label to summarize
  --legend_column_index=LEGEND_COLUMN_INDEX
                        Column index for legend to summarize
  --label_frequency=LABEL_FREQUENCY
                        Label frequency, if label type is date, this value is
                        parsed as seconds else it's parsed as number of rows
  --rows_limit=ROWS_LIMIT
                        Column index for legend to summarize
```

Here are a few examples:

```
# Search for the "normal|neptune" regex in the provided CSV file and display an overall frequency distribution in descending order. 
python summarize.py --summary_type fd --file_type CSV --graph_type term --label_regex "normal|neptune" tests/data/NSL_KDD.csv
CSV found! - tests/data/NSL_KDD.csv
normal : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  - 67343 occurrences
neptune: ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  - 41214 occurrences
```

```
# Search for the values in the specified column index in the provided CSV file and display an overall frequency distribution in descending order. 
python summarize.py --summary_type fd --file_type CSV --graph_type term --label_column_index -2 tests/data/NSL_KDD.csv
CSV found! - tests/data/NSL_KDD.csv
normal         : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  - 67343 occurrences
neptune        : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇  - 41214 occurrences
satan          : ▇▇  - 3633 occurrences
ipsweep        : ▇▇  - 3599 occurrences
portsweep      : ▇▇  - 2931 occurrences
smurf          : ▇  - 2646 occurrences
nmap           : ▇  - 1493 occurrences
back           : ▏  - 956 occurrences
teardrop       : ▏  - 892 occurrences
warezclient    : ▏  - 890 occurrences
pod            : ▏  - 201 occurrences
guess_passwd   : ▏  - 53 occurrences
buffer_overflow: ▏  - 30 occurrences
warezmaster    : ▏  - 20 occurrences
land           : ▏  - 18 occurrences
imap           : ▏  - 11 occurrences
rootkit        : ▏  - 10 occurrences
loadmodule     : ▏  - 9 occurrences
ftp_write      : ▏  - 8 occurrences
multihop       : ▏  - 7 occurrences
phf            : ▏  - 4 occurrences
perl           : ▏  - 3 occurrences
spy            : ▏  - 2 occurrences
```

```
# Provide a timeline of occurences aggregated in the specified time label_frequency over the specified number of records
summarize.py --summary_type timeline --file_type CSV --graph_type term --legend_column_index -2 --legend_regex ^n\w+ --label_frequency 40 --rows_limit 10000 tests/data/NSL_KDD.csv
CSV found! - tests/data/NSL_KDD.csv
40  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 19 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ neptune - 18 occurrences
80  : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ neptune - 15 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 19 occurrences
      ▇ nmap - 1 occurrence
120 : ▇▇▇▇▇▇▇▇▇▇ neptune - 10 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 27 occurrences
160 : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ neptune - 17 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 19 occurrences
      ▇ nmap - 1 occurrence
200 : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 22 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇ neptune - 11 occurrences
240 : ▇▇▇▇▇▇▇▇▇▇▇▇ neptune - 12 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 23 occurrences
280 : ▇▇▇▇▇▇▇▇▇▇▇ neptune - 11 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 21 occurrences
      ▇ nmap - 1 occurrence
320 : ▇▇▇▇▇▇▇▇▇▇▇▇▇ neptune - 13 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 19 occurrences
      ▇ nmap - 1 occurrence
360 : ▇▇▇▇▇▇▇▇▇▇▇▇▇▇ neptune - 14 occurrences
      ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ normal - 21 occurrences
....
```
