# Repo1-cdk-factorial-rest-service
## _This repo has following components_
 _1. AWS lambda funtion, which gets notified on object creation of S3._
 _2. cdk pipeline written using python to automate complete CICD of the application._

## Features
- Python lamda function which reads event notification of object creation of S3, parses the data and updates the same in dynamo db
- Any commits into github triggers the deployment of code in aws infra


## Tech

- [Python] - Application language for lambda!,CDK pipeline for CICD automation.
- [AWS services] - lambda,s3,dynamodb

## Installation

App requires [Python 3](https://www.python.org/downloads/) to run.

Local environment bootstrapping to start the application
```sh
python3 -m venv .venv # To manually create a virtualenv on MacOS and Linux
source .venv/bin/activate # activate the virtualenv in mac
.venv\Scripts\activate.bat # activate the virtualenv in windows
pip install -r requirements.txt # install all the python dependencies
```

For deployment into aws environment

```sh
 cdk ls          list all stacks in the app
 cdk synth       emits the synthesized CloudFormation template
 cdk bootstrap   bootstrap the required roles and permission to create the pipeline and maintain its                        lifecycle 
 git commit/git push To be able to pool the new code when the pipeline gets deployed.
 cdk deploy      deploy this stack to your default AWS account/region
 cdk diff        compare deployed stack with current state
 cdk docs        open CDK documentation
```

> Note: CDK reference taken from 



