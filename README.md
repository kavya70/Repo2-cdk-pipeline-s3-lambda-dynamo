# Repo2-cdk-pipeline-s3-lambda-dynamo

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

> Note: Application has CDK pipeline and need to be deployed using CLI(CDK deploy) for the pipeline creation. once deployed, it will poll for the changes in the git repo. Later all the stages in the pipeline will be triggered 

> The csv_data_s3 has the file moviedata.csv that can be used to upload to s3 bucket (s3-lamda-dynamo) which triggers a lambda and populates the dynamo db(movieDetails)



