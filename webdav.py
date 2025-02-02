from webdav3.client import Client
import os
import json
import tempfile 
import librosa
from time import time

class WebDAVClient:
    def __init__(self, base_url, username, password):
        options = {
            'webdav_hostname': base_url,
            'webdav_login': username,
            'webdav_password': password,
            'chunk_size': 65536,
        }
        self.client = Client(options)

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

    def get_audio(self, remote_path): 
        with tempfile.TemporaryDirectory() as tempdirname:
            tempfilename = os.path.join(tempdirname, "temp.wav")
            self.download_file(remote_path, tempfilename)
            data, sr = librosa.load(tempfilename, sr=None)
        return data, sr

    def upload_file(self, local_path, remote_path):
        self.client.upload_sync(remote_path=remote_path, local_path=local_path)
        os.remove(local_path)

    def download_file(self, remote_path, local_path):
        self.client.download_sync(remote_path=remote_path, local_path=local_path)

    def delete_file(self, remote_path):
        self.client.clean(remote_path)

    def list_directory(self, remote_path):
        return self.client.list(remote_path)

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
