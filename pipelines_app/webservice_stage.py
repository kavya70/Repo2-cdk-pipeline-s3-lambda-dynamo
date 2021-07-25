from aws_cdk import core

from .pipelines_app_stack import PipelinesAppStack

class WebServiceStage(core.Stage):
  def __init__(self, scope: core.Construct, id: str, **kwargs):
    super().__init__(scope, id, **kwargs)

    service = PipelinesAppStack(self, 'WebService')

    self.url_output = service.url_output

