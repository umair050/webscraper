import csv
import validators

SEARCH_DICT = []


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


def get_csv_data():
    filename = "search1.csv"
    # opening the file using "with"
    # statement
    with open(filename, 'r') as data:
        for line in csv.reader(data):
            # print(line)
            SEARCH_DICT.append(line)
    print(len(SEARCH_DICT))


def save_unique_data(data):
    filename = "sheet_unique.csv"
    with open(filename, 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        # write a row to the csv file
        for row in data:
            writer.writerow(row)


get_csv_data()

save_unique_data(unique(SEARCH_DICT))
