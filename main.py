import requests
from datetime import datetime
import time

from csv import reader, writer


def get_profile(cfcid):
    URL = f"https://server.chess.ca/api/player/v1/{cfcid}"
    page = requests.get(URL)
    return page.json()


def read_from_file():
    # file is recommend to be in the following format: starting rank, Name of Player, CFC ID
    # information of the event
    event_date = datetime(2022, 12, 11)  # date of the event
    # event_date = datetime.now() # if the event is today
    file_path = "resources/"  # file to read. First 3 csv columns must be what we want to keep
    file_name = "holidays.csv"
    cfc_id_index = 3  # index of the id number. Assume everything to the left of the index is what we want to keep

    id_list = []

    with open(file_path + file_name, 'r') as f:
        csv_reader = reader(f)
        header = next(csv_reader)  # skip the header

        new_csv_rows = []

        for row in csv_reader:
            # iterate through each row
            print(row)
            cfc_id = row[cfc_id_index]  # the location of the csv file

            # if not row[0]:
            #     continue  # skip empty values

            data_to_write = row[0:cfc_id_index + 1]  # we want to keep the first few indices
            if cfc_id != '':  # if the id is not empty

                if cfc_id == "NA":
                    data_to_write.append("0")
                    data_to_write += [] + [] + [] + row[cfc_id_index + 2:]  # add remaining indexes
                    print(data_to_write)
                    new_csv_rows.append(data_to_write)
                    continue

                if cfc_id in id_list: continue
                id_list.append(cfc_id)
                print(cfc_id)

                profile = get_profile(cfc_id)

                if profile["player"]["events"] == []:
                    data_to_write.append("0")
                    data_to_write += [] + [] + [] + row[cfc_id_index + 2:]  # add remaining indexes
                    print(data_to_write)
                    new_csv_rows.append(data_to_write)
                    continue
                else:
                    data_to_write.append(profile["player"]["regular_rating"])

                cfc_expiry = profile["player"]["cfc_expiry"]
                if not cfc_expiry.strip():
                    data_to_write.append("NA")
                else:
                    expiry_date = datetime.strptime(cfc_expiry, '%Y-%m-%d')
                    if expiry_date < event_date:
                        data_to_write.append("Expired")
                    else:
                        data_to_write.append("Valid")

                # add current rating of player to the end of the list
                data_to_write.append(profile["player"]["fide_id"])
                data_to_write.append(profile["player"]["name_first"])
                data_to_write.append(profile["player"]["name_last"])
                data_to_write += row[cfc_id_index + 4:]  # add remaining indexes
                print(data_to_write)

                new_csv_rows.append(data_to_write)

    print(new_csv_rows)
    f.close()

    new_header = header[0:cfc_id_index + 1] + [
        "CFC Rating"] + ["CFC Membership"] + ["FIDE ID"] + ["First Name"] + ["Last Name"] + header[cfc_id_index + 4:]  # new header based on what we want to print
    sorted_data = sort_by_rating(new_csv_rows,
                                 cfc_id_index + 1)  # sort by the index of the rating. Rating index is 1 above the CFC index
    print(sorted_data)
    # sorted_data = list(dict.fromkeys(sorted_data))  # remove duplicates
    write_to_file(file_path + "updated_" + file_name, new_header, sorted_data)


def write_to_file(filename, header, contents):
    # writes to file based on the filename, header, and contents that we want to write
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        write = writer(f)
        write.writerow(header)

        for content in contents:
            write.writerow(content)


def sort_by_rating(data, ratings_index):
    # sorts the data by ratings and updates the rank of the players
    data.sort(key=lambda row: int(row[ratings_index]), reverse=True)

    rankings_number = 1
    for line in data:
        line[0] = rankings_number  # assume that the first value is the rankings
        rankings_number += 1

    return data


def main():
    print('Insert new line separated cfc ids. Then end with "done".')

    id_list = []
    while (inp := input()) != "done":
        id_list.append(inp)

    for cfcid in id_list:
        if not cfcid.strip():
            print("NA")
            continue

        cfc_expiry = get_profile(cfcid)["player"]["cfc_expiry"]
        if not cfc_expiry.strip():
            print("NA")
            continue

        expiry_date = datetime.strptime(cfc_expiry, '%Y-%m-%d')
        if expiry_date < datetime.now():
            print("Expired")
        else:
            print("Valid")

        time.sleep(0.5)


if __name__ == "__main__":
    # main()
    read_from_file()
