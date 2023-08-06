from unittest import TestCase

from aws_cdk import (
    core,
    aws_ec2,
    aws_cognito
)

from awscdk_components.elb import alb_https, alb_utils

from awscdk_components.tests import unittest_utils


class AlbUtilsTest(TestCase):

    def test_register_lambda_target_group_with_cognito_auth_rule(self):
        app = core.App()
        stack = unittest_utils.GenericTestStack(app, 'test-stack')
        alb_cfg = alb_https.AlbCfg(
            alb_name='TestALB',
            vpc=stack.vpc,
            subnets=stack.subnets,
            certificate_arns=['arn:aws:acm:us-east-1:023475735288:certificate/ff6967d7-0fdf-4967-bd68-4caffc983447'],
            cidr_ingress_ranges=[],
            icmp_ranges=[]
        )
        alb_construct = alb_https.AlbHttpsConstruct(stack, 'albhttps', alb_cfg)
        function = unittest_utils.create_lambda(stack)
        user_pool = aws_cognito.UserPool(scope=stack, id='userpool', user_pool_name='my-test-pool')
        user_pool_cfn = user_pool.node.default_child
        user_pool_app_client = user_pool.add_client('my-test-app-client')
        user_pool_app_client_cfn = user_pool_app_client.node.default_child
        user_pool_domain = user_pool.add_domain(
            'my-test-domain',
            cognito_domain=aws_cognito.CognitoDomainOptions(
                domain_prefix='my-domain'
            )
        )
        user_pool_domain_cfn = user_pool_domain.node.default_child
        alb_utils.register_lambda_target_group_with_cognito_auth_rule(
            scope=stack,
            fn=function,
            vpc=stack.vpc,
            listener=alb_construct.https_listener,
            user_pool=user_pool_cfn,
            user_pool_app_client=user_pool_app_client_cfn,
            user_pool_domain=user_pool_domain_cfn,
            path_pattern_values=['/mylambda', '/mylambda/*']
        )
        alb_https.add_access_denied_fix_response('fix401resp', alb_construct.https_listener)
        alb_https.add_favicon_fix_response('favicon', alb_listener=alb_construct.https_listener)
        template = unittest_utils.get_template(app, stack.stack_name)
        self.assertIn(
            '{"Type": "AWS::Lambda::Function", "Properties": {"Code": {"ZipFile": "def handler(event, context): '
            'return { \'statusCode\': 200, \'body\': \'Lambda was invoked successfully.\' }"}, "Handler": '
            '"index.handler"',
            template,
            'Lambda function is created'
        )
        self.assertIn(
            '"Type": "AWS::ElasticLoadBalancingV2::TargetGroup", "Properties": {"Targets": [{"Id": {"Fn::GetAtt": ['
            '"lambdafunction',
            template,
            'Target group is created'
        )
        self.assertIn(
            '"TargetType": "lambda"}',
            template,
            'from type lambda'
        )
        self.assertIn(
            '"lambdaalblrule": {"Type": "AWS::ElasticLoadBalancingV2::ListenerRule", "Properties": {"Actions": [{'
            '"AuthenticateCognitoConfig": {"OnUnauthenticatedRequest": "authenticate", "Scope": "openid", '
            '"SessionTimeout": 3600, "UserPoolArn": ',
            template,
            'Cognito authentication rule exists'
        )
        self.assertIn(
            '"Type": "forward"}], "Conditions": [{"Field": "path-pattern", "Values": ["/mylambda", "/mylambda/*"]}]',
            template,
            'Forward to lambda with the path is available'
        )

    def test_register_ec2_as_alb_target(self):
        app = core.App()
        stack = unittest_utils.GenericTestStack(app, 'test-stack')
        alb_cfg = alb_https.AlbCfg(
            alb_name='TestALB',
            vpc=stack.vpc,
            subnets=stack.subnets,
            certificate_arns=['arn:aws:acm:us-east-1:023475735288:certificate/ff6967d7-0fdf-4967-bd68-4caffc983447'],
            cidr_ingress_ranges=[],
            icmp_ranges=[]
        )
        alb_construct = alb_https.AlbHttpsConstruct(stack, 'albhttps', alb_cfg)
        ec2 = aws_ec2.Instance(
            scope=stack,
            id='ec2foralb',
            vpc=stack.vpc,
            instance_type=aws_ec2.InstanceType(instance_type_identifier='t3.micro'),
            machine_image=aws_ec2.MachineImage.latest_amazon_linux()
        )
        alb_utils.register_ec2_as_alb_target(
            stack,
            ec2=ec2,
            listener=alb_construct.https_listener,
            vpc=stack.vpc,
            path_pattern_values=['/ec2'],
            port=8443
        )
        alb_https.add_access_denied_fix_response('fix401resp', alb_construct.https_listener)
        alb_https.add_favicon_fix_response('favicon', alb_listener=alb_construct.https_listener)
        template = unittest_utils.get_template(app, stack.stack_name)
        self.assertIn(
            '{"Type": "AWS::EC2::Instance"',
            template,
            'EC2 instance is created'
        )
        self.assertIn(
            '{"Type": "AWS::ElasticLoadBalancingV2::TargetGroup", "Properties": {"Port": 8443, "Protocol": "HTTPS", '
            '"Targets": [{"Id": {"Ref": "ec2foralb',
            template,
            'Target group is created'
        )
        self.assertIn(
            '"TargetType": "instance"',
            template,
            'The TG type is instance'
        )
        self.assertIn(
            '"ec2alblrule": {"Type": "AWS::ElasticLoadBalancingV2::ListenerRule", "Properties": {"Actions": [{'
            '"Order": 20, "TargetGroupArn": {"Ref": "ec2tg',
            template,
            'Listener rule for the TG is created'
        )
        self.assertIn(
            '"Type": "forward"}], "Conditions": [{"Field": "path-pattern", "Values": ["/ec2"]}]',
            template,
            'From type forward to the provided path /ec2'
        )
