from configparser import ConfigParser
from datetime import datetime, timedelta
from pathlib import Path
import sys


class TokenDataBuilder:
    def __init__(self):
        super().__init__()
        self.token_data = {}

    def with_profile(self, profile):
        self.token_data["profile"] = profile
        return self

    def with_credentials_directory(self, credentials_dir):
        self.token_data["credentials_dir"] = credentials_dir
        config_file_path = str(Path(credentials_dir) / "config")
        if Path(config_file_path).is_file():
            self.token_data["config_file_path"] = config_file_path
        else:
            sys.exit("No config file found at " + self.token_data["credentials_dir"] + " create one to proceed")
        return self

    def with_serial_number(self, mfa_serial):
        config = ConfigParser()
        config.read(self.token_data["config_file_path"])
        if mfa_serial is not None:
            self.token_data["mfa_serial"] = mfa_serial
        else:
            try:
                self.token_data["mfa_serial"] = config[self.token_data["profile"]]["mfa_serial"]
            except KeyError:
                sys.exit("Device ARN needed as argument as it isn't populated yet in config")
        return self

    def with_token_code(self, token_code):
        if token_code is not None:
            self.token_data["token_code"] = token_code
        else:
            sys.exit("Cannot generate credentials without MFA token code")
        return self

    def with_expires_in(self, expires):
        if expires is not None:
            self.token_data["lifetime"] = int(expires)
        else:
            self.token_data["lifetime"] = "43200"
        self.token_data["expires"] = datetime.now() + timedelta(seconds=int(expires))
        return self

    def get_token_builder_data(self):
        return self.token_data
