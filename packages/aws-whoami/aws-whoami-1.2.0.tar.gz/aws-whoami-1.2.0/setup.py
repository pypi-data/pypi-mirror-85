# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['aws_whoami']
install_requires = \
['boto3']

entry_points = \
{'console_scripts': ['aws-whoami = aws_whoami:main']}

setup_kwargs = {
    'name': 'aws-whoami',
    'version': '1.2.0',
    'description': "A tool and library for determining what AWS account and identity you're using",
    'long_description': "# aws-whoami\n**Show what AWS account and identity you're using**\n\nYou should know about [`aws sts get-caller-identity`](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html),\nwhich sensibly returns the identity of the caller. But even with `--output table`, I find this a bit lacking.\nThat ARN is a lot to visually parse, it doesn't tell you what region your credentials are configured for,\nand I am not very good at remembering AWS account numbers. `aws-whoami` makes it better.\n\n```\n$ aws-whoami\nAccount:         123456789012\n                 my-account-alias\nRegion:          us-east-2\nAssumedRole:     MY-ROLE\nRoleSessionName: ben\nUserId:          SOMEOPAQUEID:ben\nArn:             arn:aws:sts::123456789012:assumed-role/MY-ROLE/ben\n```\n\nNote: if you don't have permissions to [iam:ListAccountAliases](https://docs.aws.amazon.com/IAM/latest/APIReference/API_ListAccountAliases.html),\nyour account alias won't appear. See below for disabling this check if getting a permission denied on this call raises flags in your organization.\n\n## Install\n\nI recommend you install `aws-whoami` with [`pipx`](https://pipxproject.github.io/pipx/), which installs the tool in an isolated virtualenv while linking the script you need.\n\n```bash\n# with pipx\npipx install aws-whoami\n\n# without pipx\npython -m pip install --user aws-whoami\n```\n\nIf you don't want to install it, the `aws_whoami.py` file can be used on its own, with only a dependency on `botocore` (which comes with `boto3`).\n\n## Options\n\n`aws-whoami` uses [`boto3`](boto3.amazonaws.com/v1/documentation/api/latest/index.html), so it'll pick up your credentials in [the normal ways](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#config-settings-and-precedence),\nincluding with the `--profile` parameter.\n\nIf you'd like the output as a JSON object, that's the `--json` flag.\nThe output is the `WhoamiInfo` object (see below) as a JSON object.\n\nTo full disable account alias checking, set the environment variable `AWS_WHOAMI_DISABLE_ACCOUNT_ALIAS` to `true`.\nTo selectively disable it, you can also set it to a comma-separated list of values that will be matched against the following:\n* The beginning or end of the account number\n* The principal Name or ARN\n* The role session name\n\n## As a library\n\nThe library has a `whoami()` function, which optionally takes a `Session` (either `boto3` or `botocore`), and returns a `WhoamiInfo` namedtuple.\n\nThe fields of `WhoamiInfo` are:\n* `Account`\n* `AccountAliases` (NOTE: this is a list)\n* `Arn`\n* `Type`\n* `Name`\n* `RoleSessionName`\n* `UserId`\n* `Region`\n* `SSOPermissionSet`\n\n`Type`, `Name`, and `RoleSessionName` (and `SSOPermissionSet`) are split from the ARN for convenience.\n`RoleSessionName` is `None` for IAM users.\n\n`SSOPermissionSet` is set if the assumed role name conforms to the format `AWSReservedSSO_{permission-set}_{random-tag}`.\n\nTo disable the account alias check, pass `disable_account_alias=True` to `whoami()`.\nNote that the `AccountAliases` field will then be an empty list, not `None`.\n\n`format_whoami()` takes a `WhoamiInfo` object and returns the formatted string used for display.\n",
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/aws-whoami',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*',
}


setup(**setup_kwargs)
