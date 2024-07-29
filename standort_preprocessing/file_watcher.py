import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
load_dotenv()

DIRECTORY_TO_WATCH = os.getenv('DIRECTORY_TO_WATCH')
POST_URL = os.getenv('POST_URL')

class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            filename = os.path.basename(file_path)
            if not filename.endswith('.swp'):
                self.upload_file(file_path, filename)

    def upload_file(self, file_path, filename):
        with open(file_path, 'rb') as file:
            files = {'file': (filename, file)}
            headers = {'Filename': filename}
            try:
                response = requests.post(
                    POST_URL,
                    files=files,
                    headers=headers,
                    # auth=HTTPBasicAuth(USERNAME_UNI, PASSWORD_UNI),
                    verify=True  # Disable SSL verification
                )
                if response.status_code == 200:
                    print(f"File {filename} uploaded successfully.")
                else:
                    print(f"Failed to upload {filename}. Status code: {response.status_code}  \nIp: {POST_URL}")
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("File-watcher started")
    event_handler = NewFileHandler()
    observer = Observer()
    observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=False)
    
    print(f"Watching directory: {DIRECTORY_TO_WATCH}")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
