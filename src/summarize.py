import re
import sys
from src import termgraph
import matplotlib.pyplot as plt


def summarize(
        summary_type: str,
        file_type: str,
        graph_type: str,
        file_path: str,
        label_regex: str = None,
        legend_regex: str = None,
        label_column_index: int = None,
        legend_column_index: int = None,
        label_frequency: int = None,
        rows_limit: int = None,
        delimiter: str = ','
):
    if summary_type == 'fd':
        if label_regex is not None:
            label_regex = label_regex
        elif file_type == "CSV" and label_column_index is not None:
            label_column_index = label_column_index
        else:
            print("At least regex or label column index (For a CSV file) should be specified for the frequency "
                  "distribution!")
            exit(1)
    elif summary_type == 'timeline':
        if file_type != "CSV" and legend_regex is not None:
            legend_regex = legend_regex
        elif file_type == "CSV" and legend_column_index is not None and label_frequency is not None:
            label_column_index = label_column_index
            legend_column_index = legend_column_index
            label_frequency = label_frequency
        else:
            print("At least a label regex and label frequency needs to be specified for a timeline!")
            exit(1)

    supported_colors = [94, 92, 91, 93, 96, 95, 90, 98]
    term_data = list()
    labels = list()
    term_legend = list()
    sys.argv = [sys.argv[0]]
    args = termgraph.init_args(cmd=False)
    args["width"] = 50
    normal_type = None
    y_data = dict()

    if summary_type.lower() == 'timeline':
        normal_type = 'normal'
        i = 0
        previous_i = 0
        occurrences = dict()
        legend_set = set()
        with open(file_path, 'r') as csv_file:
            for line in csv_file:
                row = line.split(delimiter)
                legend = row[legend_column_index]
                current_label = str(i) if label_column_index is None else row[label_column_index]
                if legend not in occurrences \
                        and (legend_regex is None or (file_type == "CSV" and re.match(legend_regex, legend))
                             or (file_type != "CSV" and re.findall(legend_regex, legend))):
                    occurrences[legend] = 0
                if legend not in legend_set \
                        and (legend_regex is None or (file_type == "CSV" and re.match(legend_regex, legend))
                             or (file_type != "CSV" and re.findall(legend_regex, legend))):
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
                    label = line.split(delimiter)[label_column_index]
                    if label not in frequency_distribution:
                        frequency_distribution[label] = 0
                    frequency_distribution[label] += 1
                    pass
                else:
                    print('label_regex is None and either file is not a CSV or label_column_index is None! '
                          'Please check.')
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
        termgraph.chart(
            supported_colors,
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
        print(f"Unsupported graph type {file_type}")
