from aws_cdk import core
from pipelines_app.pipelines_app_stack import PipelinesAppStack

def test_lambda_handler():
  # GIVEN
  app = core.App()

  # WHEN
  PipelinesAppStack(app, 'Stack')

  # THEN
  template = app.synth().get_stack_by_name('Stack').template
  functions = [resource for resource in template['Resources'].values()
               if resource['Type'] == 'AWS::Lambda::Function']

  assert len(functions) == 2