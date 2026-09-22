from file_IO import load_data, save_to_json
from data_processing import print_stats

# load data
filename = 'student_dataset.txt'
table = load_data(filename)

# print table statistics
print_stats(table)

#save to json
save_to_json(table, 'output.json')