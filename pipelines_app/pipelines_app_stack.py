from os import path

from aws_cdk import core
import aws_cdk.aws_lambda as lmb
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_codedeploy as codedeploy
import aws_cdk.aws_cloudwatch as cloudwatch
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_lambda as es
import aws_cdk.aws_iam as iam
import aws_cdk.aws_s3_notifications as s3_notifications
import aws_cdk.aws_dynamodb as dynamodb


 

class PipelinesAppStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here
        this_dir = path.dirname(__file__)

        bucket = s3.Bucket(self, id='my-bucket-id', bucket_name='s3-lamda-dynamo')


        handler = lmb.Function(self, 'Handler',
            runtime=lmb.Runtime.PYTHON_3_7,
            handler='handler.handler',
            code=lmb.Code.from_asset(path.join(this_dir, 'lambda')))

        table = dynamodb.Table.from_table_arn(self, "ImportedTable", "arn:aws:dynamodb:ap-south-1:402122568686:table/movieDetails")
        bucket.grant_read(handler)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED,s3_notifications.LambdaDestination(handler))
        table.grant_read_write_data(handler)



        alias = lmb.Alias(self, 'HandlerAlias',
            alias_name='Current',
            version=handler.current_version)

        gw = apigw.LambdaRestApi(self, 'Gateway',
            description='Endpoint for a simple Lambda-powered web service',
            handler=alias)

        failure_alarm = cloudwatch.Alarm(self, 'FailureAlarm',
            metric=cloudwatch.Metric(
                metric_name='5XXError',
                namespace='AWS/ApiGateway',
                dimensions={
                    'ApiName': 'Gateway',
                },
                statistic='Sum',
                period=core.Duration.minutes(1)),
            threshold=1,
            evaluation_periods=1)

        codedeploy.LambdaDeploymentGroup(self, 'DeploymentGroup',
            alias=alias,
            deployment_config=codedeploy.LambdaDeploymentConfig.CANARY_10_PERCENT_10_MINUTES,
            alarms=[failure_alarm])

        self.url_output = core.CfnOutput(self, 'Url',
            value=gw.url)

