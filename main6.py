from file_IO import load_from_html
from data_processing import print_stats


# load data
filename = './A1_partial_solution/student_dataset.txt'
table = load_from_html(filename)

# print table statistics
print_stats(table)