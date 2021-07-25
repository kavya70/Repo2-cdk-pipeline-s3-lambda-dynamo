from aws_cdk import core
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as cpactions
from aws_cdk import pipelines

from .webservice_stage import WebServiceStage

APP_ACCOUNT = '402122568686'
APP_REGION = 'ap-south-1'

class PipelineStack(core.Stack):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    source_artifact = codepipeline.Artifact()
    cloud_assembly_artifact = codepipeline.Artifact()

    pipeline = pipelines.CdkPipeline(self, 'Pipeline',
      cloud_assembly_artifact=cloud_assembly_artifact,
      pipeline_name='WebinarPipeline',

      source_action=cpactions.GitHubSourceAction(
        action_name='GitHub',
        output=source_artifact,
        oauth_token=core.SecretValue.secrets_manager('/my/github/token'),
        owner='kavya70',
        repo='Repo2-cdk-pipeline-s3-lambda-dynamo',
        trigger=cpactions.GitHubTrigger.POLL),

      synth_action=pipelines.SimpleSynthAction(
        source_artifact=source_artifact,
        cloud_assembly_artifact=cloud_assembly_artifact,
        install_command='npm install -g aws-cdk && pip install -r requirements.txt',
        build_command='pytest unittests',
        synth_command='cdk synth'))

    pipeline.add_application_stage(WebServiceStage(self, 'pre-prod', env={
      'account': APP_ACCOUNT,
      'region': APP_REGION,
    }))
    # pipeline.add_application_stage(WebServiceStage(self, 'Prod', env={
    #   'account': APP_ACCOUNT,
    #   'region': APP_REGION,
    # }))

