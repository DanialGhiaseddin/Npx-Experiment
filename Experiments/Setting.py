import json
import os


class Settings:
    def __init__(self, file_path='assets/settings.json'):
        self.file_path = file_path
        self._settings = {}
        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self._settings = json.load(f)
        else:
            self._settings = {
                'log_dir': './experiment_logs',
            }
            self.save_settings()

    def save_settings(self):
        with open(self.file_path, 'w') as f:
            json.dump(self._settings, f, indent=4)

    def __getattr__(self, item):
        return self._settings.get(item)

    def __setattr__(self, key, value):
        if key in ['_settings', 'file_path']:
            super().__setattr__(key, value)
        else:
            self._settings[key] = value
            self.save_settings()


if __name__ == "__main__":
    # Example Usage
    settings = Settings()
    print(settings.log_dir)  # Output: default_value1
    settings.color_space = 'rgb'
    print(settings.color_space)  # Output: new_value1

    # Reload settings to see if the change persists
    settings = Settings()
    print(settings.color_space)  # Output: new_value1
