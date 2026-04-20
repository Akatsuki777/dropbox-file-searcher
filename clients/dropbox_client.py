import dropbox
import dotenv
import os

class DropboxClient:

    def __init__(self, dotenv_path='.env', logger=None):
        dotenv.load_dotenv(dotenv_path)
        self.dbx = dropbox.Dropbox(os.getenv('DROPBOX_TOKEN'))
        self.logger = logger

    def search_files(self, query, path=''):
        try:
            result = self.dbx.files_search(path, query)
            return result.matches
        except dropbox.exceptions.ApiError as e:
            if self.logger:
                self.logger.error(f"API error: {e}")
            return []
    
    def get_file_metadata(self, file_id):
        try:
            metadata = self.dbx.files_get_metadata(file_id)
            return metadata
        except dropbox.exceptions.ApiError as e:
            if self.logger:
                self.logger.error(f"API error: {e}")
            return None
    
    def create_folder(self, path):
        try:
            self.dbx.files_create_folder_v2(path)
            if self.logger:
                self.logger.info(f"Folder created at: {path}")
        except dropbox.exceptions.ApiError as e:
            if self.logger:
                self.logger.error(f"API error: {e}")
            return e

    def verify_folder_exists(self, path):
        try:
            self.dbx.files_get_metadata(path)
        except dropbox.exceptions.ApiError as e:
            if isinstance(e.error, dropbox.files.GetMetadataError) and e.error.is_path() and e.error.get_path().is_not_found():
                self.create_folder(path)
            else:
                if self.logger:
                    self.logger.error(f"API error: {e}")
                return e
            
    def move_file(self, from_path, to_path):
        try:
            self.verify_folder_exists(os.path.dirname(to_path))
            self.dbx.files_move_v2(from_path, to_path)
            if self.logger:
                self.logger.info(f"File moved from {from_path} to {to_path}")
        except dropbox.exceptions.ApiError as e:
            if self.logger:
                self.logger.error(f"API error: {e}")
            return e
    