import os
import io
import flask
import random
import string
from flask import Flask, request, send_from_directory , jsonify , session
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload
import GoogleSheetData
 
app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=30))

##    ---Complete your folder id---;
DRIVE_FOLDER_1 = '----'
DRIVE_FOLDER_2 = '----'
DRIVE_FOLDER_3 = '----'

##    ---Complete your username and password---;
username_val ="-----"
password_val = "-----"
#Login page
@app.route('/')
def main():
    return flask.send_from_directory("HtmlPages", "LoginPage.html")

@app.route('/Disconnected')
def Disconnected():
    session['authenticated'] = False
    return flask.send_from_directory("HtmlPages", "LoginPage.html")

#Get response and check details
@app.route('/Check', methods=['POST'])
def check():
    username = request.form.get('username')
    password = request.form.get('password')
    if(username ==username_val and password==password_val):
        session['authenticated'] = True
        return 'True'
    else:
        session['authenticated'] = False
        return 'False'
    
#If response correct - move to this page
@app.route('/Submit_Files')
def Submit_files():
    if session.get('authenticated'):
        return flask.send_from_directory("HtmlPages", "DataPage.html")
    else:
        return 'You are not authorized to access this page'

#return 'Done' html page;
@app.route('/Done')    
def Done():
        return flask.send_from_directory("HtmlPages", "Done.html")

#Upload the images to your google drive
@app.route('/upload-image', methods=['POST'])    
def upload_image():
    try:
        #       ---Complete your json file path---
        creds = service_account.Credentials.from_service_account_file('---------')
        IDs = [DRIVE_FOLDER_1, DRIVE_FOLDER_2,DRIVE_FOLDER_3]
        unique_name = request.form.get('fname') + "_" + request.form.get('lname') + "_" + request.form.get('idname')
        arr = ['-','-','-']
        for i in range(1, 4):
            image_file = request.files.get(f'image-file-{i}')
            if image_file:
                arr[i-1] = 'Upload'
                file_metadata = {'name': unique_name, 'parents': [IDs[i-1]]}
                media = MediaIoBaseUpload(io.BytesIO(image_file.read()), mimetype='image/jpeg/pdf', chunksize=1024*1024, resumable=True)
                drive_service = build('drive', 'v3', credentials=creds)
                file = drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id'
                ).execute()
        #Update the google sheet file
        GoogleSheetData.update(request.form.get('fname') ,request.form.get('lname') , request.form.get('idname'),arr[0],arr[1],arr[2])
        return jsonify({'message': 'Images uploaded successfully!'})

    except Exception as e:
        print(str(e))
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run()
