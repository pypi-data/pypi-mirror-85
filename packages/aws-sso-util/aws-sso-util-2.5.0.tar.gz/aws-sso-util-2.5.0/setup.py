# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_sso_util',
 'aws_sso_util.cfn',
 'aws_sso_util.cli',
 'aws_sso_util.vendored_botocore']

package_data = \
{'': ['*']}

install_requires = \
['aws-error-utils>=1.0.4,<2.0.0',
 'boto3>=1.16.13,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['aws-sso-util = aws_sso_util.cli:cli']}

setup_kwargs = {
    'name': 'aws-sso-util',
    'version': '2.5.0',
    'description': 'Utilities to make AWS SSO easier',
    'long_description': "# aws-sso-util\n## Making life with AWS SSO a little easier\n\n[AWS SSO](https://aws.amazon.com/single-sign-on/) has some rough edges, and `aws-sso-util` is here to smooth them out, hopefully temporarily until AWS makes it better.\n\n`aws-sso-util` contains utilities for the following:\n* Configuring `.aws/config`\n* AWS SDK support\n* Looking up identifiers\n* CloudFormation\n* Python library for AWS SSO authentication\n\n`aws-sso-util` supersedes `aws-sso-credential-process`, which is still available in its original form [here](https://github.com/benkehoe/aws-sso-credential-process).\nRead the updated docs for `aws-sso-util credential-process` [here](docs/credential-process.md).\n\n## Quickstart\n\n0. Make sure you've [installed the AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) (which has AWS SSO support).\n\n1. I recommend you install [`pipx`](https://pipxproject.github.io/pipx/), which installs the tool in an isolated virtualenv while linking the script you need.\n\nMac:\n```bash\nbrew install pipx\npipx ensurepath\n```\n\nOther:\n```bash\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\n```\n\n2. Install\n```bash\npipx install aws-sso-util\n```\n\n3. Learn\n```bash\naws-sso-util --help\n```\n\n4. Autocomplete\n\n`aws-sso-util` uses [click](https://click.palletsprojects.com/en/7.x/), which supports autocompletion.\nThe details of enabling shell completion with click vary by shell ([instructions here](https://click.palletsprojects.com/en/7.x/bashcomplete/)), but here is an example that updates the completion in the background.\n\n```bash\nAWS_SSO_UTIL_COMPLETE_SCRIPT_DIR=~/.local/share/aws-sso-util\nAWS_SSO_UTIL_COMPLETE_SCRIPT=$AWS_SSO_UTIL_COMPLETE_SCRIPT_DIR/complete.sh\nif which aws-sso-util > /dev/null; then\n  mkdir -p $AWS_SSO_UTIL_COMPLETE_SCRIPT_DIR\n  (_AWS_SSO_UTIL_COMPLETE=source_bash aws-sso-util > $AWS_SSO_UTIL_COMPLETE_SCRIPT.tmp ;\n    mv $AWS_SSO_UTIL_COMPLETE_SCRIPT.tmp $AWS_SSO_UTIL_COMPLETE_SCRIPT &)\n  if [ -f $AWS_SSO_UTIL_COMPLETE_SCRIPT ]; then\n    source $AWS_SSO_UTIL_COMPLETE_SCRIPT\n  fi\nfi\n```\n\n## Configuring `.aws/config`\n\nRead the full docs for `aws-sso-util configure` [here](docs/configure.md).\n\n`aws-sso-util configure` has two subcommands, `aws-sso-util configure profile` for configuring a single profile, and `aws-sso-util configure populate` to add _all_ your permissions as profiles, in whatever region(s) you want (with highly configurable profile names).\n\nYou probably want to set the environment variables `AWS_CONFIGURE_SSO_DEFAULT_SSO_START_URL` and `AWS_CONFIGURE_SSO_DEFAULT_SSO_REGION`, which will inform these commands of your start url and SSO region (that is, the region that you've configured AWS SSO in), so that you don't have to pass them in as parameters every time.\n\n`aws-sso-util configure profile` takes a profile name and prompts you with the accounts and roles you have access to, to configure that profile.\n\n`aws-sso-util configure populate` takes one or more regions, and generates a profile for each account+role+region combination.\nThe profile names are completely customizable.\n\n## Adding AWS SSO support to AWS SDKs\n\nRead the full docs for `aws-sso-util credential-process` [here](docs/credential-process.md).\n\nNot all AWS SDKs have support for AWS SSO (which will change eventually).\nHowever, they all have support for `credential_process`, which allows an external process to provide credentials.\n`aws-sso-util credential-process` uses this to allow these SDKs to get credentials from AWS SSO.\nIt's added automatically (by default) by the `aws-sso-util configure` commands.\n\n## Looking up identifiers and assignments\n\nRead the full docs for `aws-sso-util lookup` and `aws-sso-util assignments` [here](docs/lookup.md).\n\nWhen you're creating assignments through the API or CloudFormation, you're required to use identifiers like the instance ARN, the principal ID, etc.\nThese identifiers aren't readily available through the console, and the principal IDs are not the IDs you're familiar with.\n`aws-sso-util lookup` allows you to get these identifers, even en masse.\n\nThere is no simple API for retrieving all assignments or even a decent subset.\nThe current best you can do is [list all the users with a particular PermissionSet on a particular account](https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_ListAccountAssignments.html).\n`aws-sso-util assigments` takes the effort out of looping over the necessary APIs.\n\n## CloudFormation support\n\nYou'll want to read the full docs [here](docs/cloudformation.md).\n\nAWS SSO's CloudFormation support currently only includes [`AWS::SSO::Assignment`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sso-assignment.html), which means for every combination of principal (group or user), permission set, and target (AWS account), you need a separate CloudFormation resource.\nAdditionally, AWS SSO does not support OUs as targets, so you need to specify every account separately.\n\nObviously, this gets verbose, and even an organization of moderate size is likely to have tens of thousands of assignments.\n`aws-sso-util cfn` provides two mechanisms to make this concise.\n\nI look forward to discarding this part of the tool once there are two prerequisites:\n1. OUs as targets for assignments\n2. An `AWS::SSO::AssignmentGroup` resource that allows specifications of multiple principals, permission sets, and targets, and performs the combinatorics directly.\n\n### CloudFormation Macro\n`aws-sso-util` defines a resource format for an AssignmentGroup that is a combination of multiple principals, permission sets, and targets, and provides a CloudFormation Macro you can deploy that lets you use this resource in your templates.\n\n### Client-side generation\n\nI am against client-side generation of CloudFormation templates, but if you don't want to trust this 3rd party macro, you can generate the CloudFormation templates directly.\n\n`aws-sso-util cfn` takes one or more input files, and for each input file, generates a CloudFormation template and potentially one or more child templates.\nThese templates can then be packaged and uploaded using [`sam`](), for example.\n\nThe input files can either be templates using the Macro (using the `--macro` flag), or somewhat simpler configuration files using a different syntax.\nThese configuration files can define permission sets inline, have references that turn into template parameters, and you can provide a base template that the resulting resources are layered on top of.\n",
    'author': 'Ben Kehoe',
    'author_email': 'ben@kehoe.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benkehoe/aws-sso-util',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
