__all__ = ['get_rows']


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from import_gs.credentials import get_credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def parse_sheet_id_from_url(sheet_id):
    if sheet_id.startswith('http'):
        return sheet_id.split('/')[5]
    else:
        return sheet_id


def get_rows(sheet_id, range_name):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = get_credentials(SCOPES)
    sheet_id = parse_sheet_id_from_url(sheet_id)
    result = []

    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        values = (
                sheet.values()
                .get(spreadsheetId=sheet_id, range=range_name)
                .execute()
        ).get("values", [])

        if not values:
            print("No data found.")

        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            result.append(row)

    except HttpError as err:
        print(err)

    return result
