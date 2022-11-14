import requests
from datetime import datetime
import time

from csv import reader, writer

def get_profile(cfcid):
    URL = f"https://server.chess.ca/api/player/v1/{cfcid}"
    page = requests.get(URL)
    return page.json()


def read_from_file():
    # information of the event
    event_date = datetime(2022,12,11) # date of the event
    # event_date = datetime.now() # if the event is today
    file_path = "holidaysOpenOct13.csv" # file to read. First 3 csv columns must be what we want to keep
    cfc_id_index = 2 # index of the id number. Assume everything to the left of the index is what we want to keep

    id_list = []

    with open(file_path, 'r') as f:
        csv_reader = reader(f)
        header = next(csv_reader) # skip the header

        new_csv_rows = []

        for row in csv_reader:
            # iterate through each row
            print(row)
            cfc_id = row[cfc_id_index] # the location of the csv file
            data_to_write = row[0:cfc_id_index] # we want to keep the first few indices
            if cfc_id != '': # if the id is not empty
                id_list.append(cfc_id)

                cfc_expiry = get_profile(cfc_id)["player"]["cfc_expiry"]
                if not cfc_expiry.strip():
                    data_to_write.append("NA")
                else:
                    expiry_date = datetime.strptime(cfc_expiry, '%Y-%m-%d')
                    if expiry_date < event_date:
                        data_to_write.append("Expired")
                    else:
                        data_to_write.append("Valid")

                # add current rating of player to the end of the list
                data_to_write.append(get_profile(cfc_id)["player"]["regular_rating"])
                print(data_to_write)

            new_csv_rows.append(data_to_write)

    print(new_csv_rows)
    f.close()

    new_header = header[0:cfc_id_index] + ["CFC Membership"] + ["CFC Rating"] # new header based on what we want to print
    write_to_file("updated" + file_path, new_header, new_csv_rows)


def write_to_file(filename, header, contents):
    # writes
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        write = writer(f)
        write.writerow(header)

        for content in contents:
            write.writerow(content)

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