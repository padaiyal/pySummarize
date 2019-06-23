import optparse

from src.summarize import summarize

parser = optparse.OptionParser(description='Summarize information')
parser.add_option('--summary_type', type=str, help='Type of summary')
parser.add_option('--file_type', type=str, help='Type of input file', default='unknown')
parser.add_option('--graph_type', type=str, help='Type of graph')
parser.add_option('--label_regex', type=str, help='Regex to search for')
parser.add_option('--legend_regex', type=str, help='Regex to search for')
parser.add_option('--label_column_index', type=int, help='Column index for label to summarize')
parser.add_option('--legend_column_index', type=int, help='Column index for legend to summarize')
parser.add_option('--label_frequency', type=int, help='Label frequency, if label type is date, this value is parsed '
                                                      'as seconds else it\'s parsed as number of rows')
parser.add_option('--rows_limit', type=int, help='Column index for legend to summarize', default=0)
parser.add_option('--delimiter', type=str, help='Column delimiter', default=',')

(options, args) = parser.parse_args()

summary_type = options.summary_type
file_type = options.file_type.upper()
graph_type = options.graph_type
label_regex = options.label_regex
legend_regex = options.legend_regex
label_column_index = options.label_column_index
legend_column_index = options.legend_column_index
label_frequency = options.label_frequency
rows_limit = options.rows_limit
delimiter = options.delimiter
file_path = None
if len(args) == 1:
    print(args)
    file_path = args[0]
    summarize(
        summary_type=summary_type,
        file_type=file_type,
        file_path=file_path,
        graph_type=graph_type,
        legend_regex=legend_regex,
        label_frequency=label_frequency,
        legend_column_index=legend_column_index,
        label_column_index=label_column_index,
        label_regex=label_regex,
        rows_limit=rows_limit,
        delimiter=delimiter

    )
else:
    print('Only one argument should be provided and that should be the path to the file to be analyzed.')
