import json

from aws_cdk import (
    core,
    aws_ec2,
    aws_certificatemanager as acm,
    aws_lambda
)

ACM_CERT_ARN = 'arn:aws:acm:us-east-1:023475735288:certificate/ff6967d7-0fdf-4967-bd68-4caffc983447'


class GenericTestStack(core.Stack):
    vpc: aws_ec2.IVpc
    subnets: aws_ec2.SubnetSelection

    def __init__(self, scope: core.Construct, sid: str, **kwargs) -> None:
        super().__init__(scope, sid, **kwargs)
        self.vpc = aws_ec2.Vpc(self, 'TestVPC', cidr='10.0.0.0/16')
        self.subnets = aws_ec2.SubnetSelection(subnets=self.vpc.select_subnets(one_per_az=True).subnets)


def get_template(app: core.App, stack_name: str):
    template = app.synth().get_stack_by_name(stack_name).template
    return json.dumps(template)


def import_certificate(scope: core.Construct, sid: str, certificate_arn: str = ACM_CERT_ARN) -> acm.ICertificate:
    return acm.Certificate.from_certificate_arn(scope, sid, certificate_arn)


def create_lambda(stack: GenericTestStack, sid: str = 'lambda_function', body: str = None) -> aws_lambda.IFunction:
    func_body = body if body else "def handler(event, context): return { 'statusCode': 200, 'body': 'Lambda was " \
                                  "invoked successfully.' }"
    return aws_lambda.Function(
        stack,
        sid,
        runtime=aws_lambda.Runtime.PYTHON_3_7,
        handler="index.handler",
        code=aws_lambda.Code.from_inline(func_body),
        vpc=stack.vpc
    )
