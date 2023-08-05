import configparser
from pathlib import Path
import boto3


class CredentialsManager:
    def __init__(self, credentials_dir, mfa_serial, profile, token_code,
                 expires, lifetime):
        super().__init__()
        self.credentials_dir = credentials_dir
        self.mfa_serial = mfa_serial
        self.profile = profile
        self.token_code = token_code
        self.expires = expires
        self.lifetime = lifetime

    def generate_token(self):
        sts_client = boto3.client('sts')
        credentials = sts_client.get_session_token(DurationSeconds=int(self.lifetime), SerialNumber=self.mfa_serial,
                                                   TokenCode=self.token_code)
        credentials = configparser.ConfigParser()
        credentials[self.profile] = {
            "aws_access_key_id": credentials['Credentials']['AccessKeyId'],
            "aws_secret_access_key": credentials['Credentials']['SecretAccessKey'],
            "aws_session_token": credentials['Credentials']['SessionToken']
        }
        with open(str(Path(self.credentials_dir) / "credentials"), 'w') as creds_file:
            credentials.write(creds_file)
        print("Updated credentials at location " + self.credentials_dir + "/credentials for profile " + self.profile)
        config = configparser.ConfigParser()
        config_file_path = str(Path(self.credentials_dir) / "config")
        config.read(config_file_path)
        config.set(self.profile, "mfa_serial", self.mfa_serial)
        with open(config_file_path, 'w') as config_file:
            config.write(config_file)
        print(
            "Updated mfa_serial for profile " + self.profile
            + " in config you can skip serial number for subsequent refresh token calls")
