from webdav3.client import Client
import os
import json
import tempfile 
import librosa
from time import time, sleep
import pandas as pd

class WebDAVClient:
    def __init__(self, base_url, username, password, num_tries = 3, pause = 3):
        options = {
            'webdav_hostname': base_url,
            'webdav_login': username,
            'webdav_password': password,
            'chunk_size': 65536,
        }
        self.client = Client(options)
        self.num_tries = num_tries
        self.pause = pause

    def get_json(self, remote_path):
        with tempfile.TemporaryDirectory() as tempdirname:
            tempfilename = os.path.join(tempdirname, "temp.json")
            self.download_file(remote_path, tempfilename)
            with open(tempfilename, "r") as f:
                data = json.load(f)
        return data
        
    def put_json(self, remote_path, data):
        if isinstance(data, dict):
            data = json.dumps(data)
        with tempfile.TemporaryDirectory() as tempdirname:
            tempfilename = os.path.join(tempdirname, "temp.json")
            with open(tempfilename, "w") as f:
                f.write(data)
            self.upload_file(tempfilename, remote_path)

    def get_csv(self, remote_path):
        with tempfile.TemporaryDirectory() as tempdirname:
            tempfilename = os.path.join(tempdirname, "temp.csv")
            self.download_file(remote_path, tempfilename)
            if ".xlsx" in remote_path:
                data = pd.read_excel(tempfilename, sheet_name="Streamlit")
            elif ".csv" in remote_path:
                data = pd.read_csv(tempfilename)
            else:
                raise ValueError(f"Not a valid file format for {remote_path}")
        return data

    def file_exists(self, remote_path):
        for _ in range(self.num_tries):
            try:
                return self.client.check(remote_path)
            except:
                self.num_tries -= 1
                if self.num_tries == 0:
                    return False
                sleep(self.pause) 
        raise ValueError("Could not check if file exists")
         
    def get_audio(self, remote_path):             
        with tempfile.TemporaryDirectory() as tempdirname:
            tempfilename = os.path.join(tempdirname, "temp.wav")
            self.download_file(remote_path, tempfilename)
            data, sr = librosa.load(tempfilename, sr=None)
        return data, sr

    def upload_file(self, local_path, remote_path):
        for _ in range(self.num_tries):
            try:
                self.client.upload_sync(remote_path=remote_path, local_path=local_path)
                os.remove(local_path)
                return
            except Exception as e:
                error = e
                sleep(self.pause)
        raise ValueError(f"Could not upload {local_path} to {remote_path} with error {error}")
        

    def download_file(self, remote_path, local_path):
        for _ in range(self.num_tries):
            try:
                self.client.download_sync(remote_path=remote_path, local_path=local_path)
                return
            except Exception as e:
                error = e
                sleep(self.pause)
        raise ValueError(f"Could not download {remote_path} to {local_path} with error {error}")

    def delete_file(self, remote_path):
        for _ in range(self.num_tries):
            try:
                self.client.clean(remote_path)
                return
            except:
                sleep(self.pause)
        
        raise ValueError(f"Could not delete {remote_path}")

    def list_directory(self, remote_path):
        for _ in range(self.num_tries):
            try:
                return self.client.list(remote_path)
            except:
                sleep(self.pause)
        
        raise ValueError(f"Could not list directory {remote_path}")

if __name__ == "__main__": 
    link = r"https://dox.ulg.ac.be/remote.php/dav/files/memoirehypnotherapie@gmail.com/"
    username = r"memoirehypnotherapie@gmail.com"
    password = r"Hypnotherapie2025!"

    client = WebDAVClient(link, username, password)
    data = {"a": 1, "b": 2, "c": ["Hello", "World"]}
    client.put_json(r"Base de données hypnose/test.json", data)
    result = client.get_json(r"Base de données hypnose/test.json")
    print(result, type(result))
    audio, sr = client.get_audio(r"Base de données hypnose/S2/Avec filtre/Conversation_ch1_band.wav")
    print(audio, sr)
