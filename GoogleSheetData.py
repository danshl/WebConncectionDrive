import os
import google.auth
from googleapiclient.discovery import build

#Read from the Googlesheet data - in this case, the counter row;
def get_data():
    #       ---Complete your json file path---
    credentials_path = "-----"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

    #Authenticate and construct the service object;
    credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/spreadsheets'])

    #        ---Set the spreadsheet ID and range---
    SPREADSHEET_ID = "------"
    RANGE_NAME = 'Sheet1!B2'

    # Build the service client and call the Sheets API to get the data;
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    # Get the value from the result
    value = result.get('values', [[]])[0][0]
    return value


#Fill in the fields in the google sheet
def update(fname,lname,id,val1,val2,val3):
    #       ---Complete your json file path---
    credentials_path = "-------"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path
    # Authenticate and construct the service object;
    credentials, project = google.auth.default(scopes=['https://www.googleapis.com/auth/spreadsheets'])
    service = build('sheets', 'v4', credentials=credentials)
    #        ---Set the spreadsheet ID and range---
    spreadsheet_id = "------"
    val = get_data()
    range_name = 'Sheet1!B' + str(val) + ':H' + str(val);

    # The values to set in the cells
    new_values = [[int(val)-4,fname,lname,id,val1,val2,val3]]
    # Prepare the request body
    request_body = {
        'range': range_name,
        'values': new_values,
    }
    # Make the API request to update the cells
    try:
        response = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='USER_ENTERED',
            body=request_body
        ).execute()
        response = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='sheet1!B2',
            valueInputOption='USER_ENTERED',
            body={
                'range': 'sheet1!B2',
                'values': [[int(val)+1]],
            }
        ).execute()
        print(f"{response.get('updatedCells')} cells updated.")
    except:
        print("Error")
