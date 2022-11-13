import requests
from datetime import datetime
import time


def get_profile(cfcid):
    URL = f"https://server.chess.ca/api/player/v1/{cfcid}"
    page = requests.get(URL)
    return page.json()


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
    main()
