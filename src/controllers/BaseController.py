from helpers.config import get_settings, Settings
import os

class BaseController:
    def __init__(self):
        self.app_settings: Settings = get_settings()
        self.app_root: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
        self.files_root: str = os.path.join(self.app_root, 'assets/files')