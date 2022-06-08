import csv
import validators


def unique(list1):
    # initialize a null list
    unique_list = []

    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list and validators.url(x[0]):
            unique_list.append(x)
    print(len(unique_list))
    return unique_list


def get_csv_data(file_name):
    # filename = "search1.csv"
    # opening the file using "with"
    # statement
    csv_data = []
    with open(file_name, 'r') as data:
        for line in csv.reader(data):
            # print(line)
            csv_data.append(line)
    print(len(csv_data))

    return csv_data


def save_unique_data(file_name, data):
    # filename = "sheet_unique.csv"
    with open(file_name, 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        for row in data:
            writer.writerow(row)


filename = "sheet1.csv"
data_sheet_1 = get_csv_data(filename)
save_unique_data(filename, unique(data_sheet_1))

filename = "sheet2.csv"
data_sheet_1 = get_csv_data(filename)
save_unique_data(filename, unique(data_sheet_1))

filename = "sheet3.csv"
data_sheet_1 = get_csv_data(filename)
save_unique_data(filename, unique(data_sheet_1))
