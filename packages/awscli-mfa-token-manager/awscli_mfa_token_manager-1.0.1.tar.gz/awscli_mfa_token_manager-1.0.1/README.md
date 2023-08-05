# Credentials Manager for AWS CLI v2

This program helps generate Credential for IAM users with MFA enabled. It's build to ease out generating credentials and storing them in a credentials file for further use.

## Installation

Install the module

```bash
pip install awscli_mfa_token_manager
```

## How it works

This tool needs a basic config file with one or more profiles and region, output settings to work. Let's say you want to generate tokens using a config file in `/opt/app/cloud/.aws` directory. When you are running it for the first time, for an IAM user that has for example, a virtual MFA device use the following arguments

```bash
manage_credentials --profile mfa --serial-number arn:aws:iam::[IAM-ACCOUNTID]:mfa/[IAM-USERNAME[] --credentials-dir /opt/app/cloud/.aws --token XXXXXX --expires 86400
```

Where 
1. `mfa`: is the profile you want to use
2. `serial_number`: is the MFA device ARN
3. `credentials-dir` is the location of `config` file , this is location where credentials file will also be saved
4. `token` is the MFA token code
5. expires is lifetime duration of the token in seconds

This command would:
1. Fetch credentials using the serial and token code
2. Create the `credentials` file in directory `/opt/app/cloud/.aws`
3. Update the `config` file to add `mfa_serial`

You can then run 

```bash
manage_credentials --profile mfa --token XXXXXX --credentials-dir /opt/app/cloud/.aws
```

to refresh token for this config / profile

### Default Values

The following default values are used, which makes these parameters optional
1. profile: `default`
2. credentials-dir: defaults to `[user.home]/.aws`
3. expires: defaults to `43200` (sts default value)
