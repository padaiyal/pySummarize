import re
import sys
from src import termgraph
import matplotlib.pyplot as plt
import optparse

parser = optparse.OptionParser(description='Summarize information')
parser.add_option('--summary_type', type=str, help='Type of summary')
parser.add_option('--file_type', type=str, help='Type of input file')
parser.add_option('--graph_type', type=str, help='Type of graph')
parser.add_option('--label_regex', type=str, help='Regex to search for')
parser.add_option('--legend_regex', type=str, help='Regex to search for')
parser.add_option('--label_column_index', type=int, help='Column index for label to summarize')
parser.add_option('--legend_column_index', type=int, help='Column index for legend to summarize')
parser.add_option('--label_frequency', type=int, help='Label frequency, if label type is date, this value is parsed '
                                                      'as seconds else it\'s parsed as number of rows')
parser.add_option('--rows_limit', type=int, help='Column index for legend to summarize', default=0)

(options, args) = parser.parse_args()

summary_type = options.summary_type
file_type = options.file_type
graph_type = options.graph_type
label_regex = options.label_regex
legend_regex = options.legend_regex
label_column_index = None
legend_column_index = None
label_frequency = None
rows_limit = options.rows_limit
if summary_type == 'fd':
    if options.label_regex is not None:
        label_regex = options.label_regex
    elif file_type == "CSV" and options.label_column_index is not None:
        label_column_index = options.label_column_index
    else:
        print("At least regex or label column index (FOr a CSV file) should be specified for the frequency "
              "distribution!")
        exit(1)
if summary_type == 'timeline':
    if file_type != "CSV" and options.legend_regex is not None:
        legend_regex = options.legend_regex
    elif file_type == "CSV" and options.legend_column_index is not None and options.label_frequency is not None:
        label_column_index = options.label_column_index
        legend_column_index = options.legend_column_index
        label_frequency = options.label_frequency
    else:
        print("At least a label regex and label frequency needs to be specified for a timeline!")
        exit(1)

file_path = None
if len(args) == 1:
    file_path = args[0]
else:
    print('Only one argument should be provided and that should be the path to the file to be analyzed.')

supported_colors = [94, 92, 91, 93, 96, 95, 90, 98]
term_data = list()
labels = list()
term_legend = list()
normal_data = dict()
sys.argv = [sys.argv[0]]
args = termgraph.init_args(cmd=False)
args["width"] = 50
delimiter = ','
normal_type = None
y_data = dict()

if file_type.upper() == "CSV":
    print(f"CSV found! - {file_path}")
    if summary_type.lower() == 'timeline':
        normal_type = 'normal'
        i = 0
        previous_i = 0
        occurrences = dict()
        current_label = None
        previous_label = None
        legend_set = set()
        with open(file_path, 'r') as csv_file:
            for line in csv_file:
                row = line.split(delimiter)
                legend = row[legend_column_index]
                if i == 0:
                    previous_label = str(i) if label_column_index is None else row[label_column_index]
                current_label = str(i) if label_column_index is None else row[label_column_index]
                if legend not in occurrences \
                        and (legend_regex is None or (summary_type == "CSV" and re.match(legend_regex, legend))
                             or (summary_type != "CSV" and re.findall(legend_regex, legend))):
                    occurrences[legend] = 0
                if legend not in legend_set \
                        and (legend_regex is None or (summary_type == "CSV" and re.match(legend_regex, legend))
                             or (summary_type != "CSV" and re.findall(legend_regex, legend))):
                    legend_set.add(legend)
                    y_data[legend] = [0] * len(labels)
                if legend in occurrences:
                    occurrences[legend] += 1
                if i - previous_i >= label_frequency:
                    labels.append(current_label)
                    term_data.append(list(occurrences.values()))
                    term_legend.append(list(occurrences.keys()))
                    for unique_legend in legend_set:
                        y_datum = occurrences[unique_legend] if unique_legend in occurrences else 0
                        y_data[unique_legend].append(y_datum)
                    occurrences = dict()
                    previous_label = current_label
                    previous_i = i
                i += 1
                if rows_limit != 0 and i == rows_limit:
                    break
    elif summary_type.lower() == 'fd':
        normal_type = 'bar'
        frequency_distribution = dict()
        i = 0
        with open(file_path, 'r') as file:
            for line in file:
                if label_regex is not None:
                    matches = re.findall(label_regex, line)
                    for match in matches:
                        if match not in frequency_distribution:
                            frequency_distribution[match] = 0
                        frequency_distribution[match] += 1
                elif label_column_index is not None:
                    label = line.split(',')[label_column_index]
                    if label not in frequency_distribution:
                        frequency_distribution[label] = 0
                    frequency_distribution[label] += 1
                    pass
                else:
                    print('label_regex and label_column_index are None! Please check.')
                    exit(1)
                i += 1
                if rows_limit != 0 and i == rows_limit:
                    break
        frequency_distribution_sorted = sorted(frequency_distribution.items(), key=lambda x: x[1], reverse=True)
        y_data = {label_regex: [item[1] for item in frequency_distribution_sorted]}
        term_data = [[item[1]] for item in frequency_distribution_sorted]
        labels = [item[0] for item in frequency_distribution_sorted]
        term_legend = [['']] * len(term_data)

    if graph_type.lower() == 'term':
        termgraph.chart(supported_colors,
                        term_data,
                        args,
                        labels,
                        term_legend
                        )
    elif graph_type.lower() == 'normal':
        for label, data in y_data.items():
            if normal_type == 'bar':
                fig, ax = plt.subplots()
                for i, v in enumerate(data):
                    ax.text(i - .4, v + 0.01 * v, str(v), color='blue', fontweight='bold')
                plt.bar(labels, data, label=label)
            else:
                plt.plot(labels, data, label=label)
            plt.xticks(labels, labels, rotation='vertical')
        plt.legend(loc='upper center')
        plt.title(file_path)
        plt.tight_layout()
        plt.show()

else:
    print(f"Unsupported file type {file_type}")
