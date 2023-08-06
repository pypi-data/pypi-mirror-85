from unittest import TestCase

from aws_cdk import core, aws_cognito

from awscdk_components.tests import unittest_utils
from awscdk_components.cognito import cognito

CUSTOM_ATTRIBUTES = ['attr1', 'attr2', 'attr3']
STANDARD_ATTRIBUTES = aws_cognito.StandardAttributes(
    email=aws_cognito.StandardAttribute(
        mutable=True,
        required=True
    ),
    gender=aws_cognito.StandardAttribute(
        mutable=True,
        required=False
    )
)


def default_user_pool_cfg() -> cognito.CognitoUserPoolCfg:
    return cognito.CognitoUserPoolCfg(user_pool_name='myuserpool')


def default_user_pool_client_cfg() -> cognito.CognitoAppClientCfg:
    return cognito.CognitoAppClientCfg(name='myuserpoolappclient')


def default_oidc_idp_cfg() -> cognito.CognitoOidcIdpCfg:
    return cognito.CognitoOidcIdpCfg(
        name='myidp',
        client_id='oidcclient',
        client_secret='topsecret',
        issuer='https://my.idp.com'
    )


def domain_prefix_cfg() -> cognito.CognitoUserPoolDomainCfg:
    return cognito.CognitoUserPoolDomainCfg(domain_prefix='myprefix')


def domain_name_cfg(scope: core.Construct, sid: str) -> cognito.CognitoUserPoolDomainCfg:
    return cognito.CognitoUserPoolDomainCfg(
        domain_name='auth.mydomain.com',
        certificate=unittest_utils.import_certificate(scope=scope, sid=sid)
    )


def lambda_trigger_cfg(stack: unittest_utils.GenericTestStack):
    post_auth_lambda = unittest_utils.create_lambda(stack=stack, sid='post_auth')
    pre_token_lambda = unittest_utils.create_lambda(stack=stack, sid='pre_token')
    return aws_cognito.UserPoolTriggers(
        post_authentication=post_auth_lambda,
        pre_token_generation=pre_token_lambda
    )


class TestCognitoConstruct(TestCase):

    def test_construct_with_default_values(self):
        app = core.App()
        stack = unittest_utils.GenericTestStack(app, 'test-stack')
        cognito.CognitoUserPoolWithOidcIdpAndAppClientConstruct(
            scope=stack,
            cid='test_default_cfg',
            user_pool_cfg=default_user_pool_cfg(),
            idp_cfg=default_oidc_idp_cfg(),
            app_client_cfg=default_user_pool_client_cfg(),
            user_pool_domain_cfg=domain_prefix_cfg()
        )
        template = unittest_utils.get_template(app, stack.stack_name)
        print(template)
        self.assertIn(
            '{"Type": "AWS::Cognito::UserPool", "Properties": {"AccountRecoverySetting": {"RecoveryMechanisms": [{'
            '"Name": "admin_only", "Priority": 1}]}, "AdminCreateUserConfig": {"AllowAdminCreateUserOnly": true}, '
            '"EmailVerificationMessage": "The verification code to your new account is {####}", '
            '"EmailVerificationSubject": "Verify your new account", '
            '"MfaConfiguration": "OFF", "SmsVerificationMessage": "The verification code to your new account is '
            '{####}", "UserPoolName": "myuserpool", "VerificationMessageTemplate": {"DefaultEmailOption": '
            '"CONFIRM_WITH_CODE", "EmailMessage": "The verification code to your new account is {####}", '
            '"EmailSubject": "Verify your new account", "SmsMessage": "The verification code to your new account is {'
            '####}"}}},',
            template,
            'User Pool with default settings is available'
        )
        self.assertIn(
            '{"Type": "AWS::Cognito::UserPoolIdentityProvider", "Properties": {"ProviderName": "myidp", '
            '"ProviderType": "OIDC", "UserPoolId": {"Ref": "testdefaultcfgmyuserpool',
            template,
            'OIDC Idp is available'
        )
        self.assertIn(
            '"ProviderDetails": {"client_id": "oidcclient", "client_secret": "topsecret", "oidc_issuer": '
            '"https://my.idp.com", "attributes_request_method": "POST", "authorize_scopes": "email profile openid"}}}',
            template,
            'IDP has correct default settings'
        )
        self.assertIn(
            '{"Type": "AWS::Cognito::UserPoolClient", "Properties": {"UserPoolId": {"Ref": "testdefaultcfgmyuserpool',
            template,
            'UserPool App Client available'
        )
        self.assertIn(
            '"AllowedOAuthFlows": ["code"], "AllowedOAuthFlowsUserPoolClient": true, "AllowedOAuthScopes": ["openid", '
            '"profile"], "CallbackURLs": ["https://example.com"], "ClientName": "myuserpoolappclient", '
            '"GenerateSecret": true, "PreventUserExistenceErrors": '
            '"ENABLED", "SupportedIdentityProviders": ["myidp"]}, "DependsOn": ["testdefaultcfgmyidp',
            template,
            'UserPool App Client has the correct default settings'
        )
        self.assertIn(
            '{"Type": "AWS::Cognito::UserPoolDomain", "Properties": {"Domain": "myprefix", "UserPoolId": {"Ref": '
            '"testdefaultcfgmyuserpool',
            template,
            'Domain prefix is available'
        )

    def test_custom_domain(self):
        app = core.App()
        stack = unittest_utils.GenericTestStack(app, 'test-stack')
        cognito.CognitoUserPoolWithOidcIdpAndAppClientConstruct(
            scope=stack,
            cid='test_default_cfg',
            user_pool_cfg=default_user_pool_cfg(),
            idp_cfg=default_oidc_idp_cfg(),
            app_client_cfg=default_user_pool_client_cfg(),
            user_pool_domain_cfg=domain_name_cfg(stack, 'myacm')
        )
        template = unittest_utils.get_template(app, stack.stack_name)
        self.assertIn(
            '{"Type": "AWS::Cognito::UserPoolDomain", "Properties": {"Domain": "auth.mydomain.com", "UserPoolId": {'
            '"Ref": "testdefaultcfgmyuserpool',
            template,
            'UserPoolDomain with custom domain exists'
        )
        self.assertIn(
            '"CustomDomainConfig": {"CertificateArn": '
            '"arn:aws:acm:us-east-1:023475735288:certificate/ff6967d7-0fdf-4967-bd68-4caffc983447"}}}}}',
            template,
            'UserPoolDomain has the correct certificate assigned'
        )

    def test_attribute_mappings(self):
        app = core.App()
        stack = unittest_utils.GenericTestStack(app, 'test-stack')
        idp_cfg = default_oidc_idp_cfg()
        attr_mappings = cognito.CognitoOidcIdpCfg.create_attribute_mapping(CUSTOM_ATTRIBUTES, STANDARD_ATTRIBUTES)
        idp_cfg.attribute_mapping = attr_mappings
        user_pool_cfg = cognito.CognitoUserPoolCfg(
            user_pool_name='myuserpool',
            custom_attribute_names_string_type=CUSTOM_ATTRIBUTES,
            standard_attributes=STANDARD_ATTRIBUTES
        )
        cognito.CognitoUserPoolWithOidcIdpAndAppClientConstruct(
            scope=stack,
            cid='test_default_cfg',
            user_pool_cfg=user_pool_cfg,
            idp_cfg=idp_cfg,
            app_client_cfg=default_user_pool_client_cfg(),
            user_pool_domain_cfg=domain_name_cfg(stack, 'myacm')
        )
        template = unittest_utils.get_template(app, stack.stack_name)
        self.assertIn(
            '"Schema": [{"Mutable": true, "Name": "email", "Required": true}, {"Mutable": true, "Name": "gender", '
            '"Required": false}, {"AttributeDataType": "String", "Mutable": true, "Name": "attr1", '
            '"StringAttributeConstraints": {"MaxLength": "2048"}}, {"AttributeDataType": "String", "Mutable": true, '
            '"Name": "attr2", "StringAttributeConstraints": {"MaxLength": "2048"}}, {"AttributeDataType": "String", '
            '"Mutable": true, "Name": "attr3", "StringAttributeConstraints": {"MaxLength": "2048"}}],',
            template,
            'UserPool schema is correct'
        )
        self.assertIn(
            '"AttributeMapping": {"email": "email", "gender": "gender", "custom:attr1": "attr1", "custom:attr2": '
            '"attr2", "custom:attr3": "attr3"},',
            template,
            'IDP Attribute mappings are correct'
        )

    def test_user_pool_triggers(self):
        app = core.App()
        stack = unittest_utils.GenericTestStack(app, 'test-stack')
        idp_cfg = default_oidc_idp_cfg()
        attr_mappings = cognito.CognitoOidcIdpCfg.create_attribute_mapping(CUSTOM_ATTRIBUTES, STANDARD_ATTRIBUTES)
        idp_cfg.attribute_mapping = attr_mappings
        user_pool_cfg = cognito.CognitoUserPoolCfg(
            user_pool_name='myuserpool',
            custom_attribute_names_string_type=CUSTOM_ATTRIBUTES,
            standard_attributes=STANDARD_ATTRIBUTES,
            user_pool_triggers=lambda_trigger_cfg(stack)
        )
        cognito.CognitoUserPoolWithOidcIdpAndAppClientConstruct(
            scope=stack,
            cid='test_default_cfg',
            user_pool_cfg=user_pool_cfg,
            idp_cfg=idp_cfg,
            app_client_cfg=default_user_pool_client_cfg(),
            user_pool_domain_cfg=domain_name_cfg(stack, 'myacm')
        )
        template = unittest_utils.get_template(app, stack.stack_name)
        self.assertIn(
            '"postauthServiceRole',
            template,
            'Post auth IAM Role available'
        )
        self.assertIn(
            '{"Type": "AWS::IAM::Role", "Properties": {"AssumeRolePolicyDocument": {"Statement": [{"Action": '
            '"sts:AssumeRole", "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}}], "Version": '
            '"2012-10-17"}, "ManagedPolicyArns": [{"Fn::Join": ["", ["arn:", {"Ref": "AWS::Partition"}, '
            '":iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"]]}, {"Fn::Join": ["", ["arn:", '
            '{"Ref": "AWS::Partition"}, ":iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole"]]}]}},',
            template,
            'Post auth IAM assignes the correct policies'
        )
        self.assertIn(
            '{"Type": "AWS::EC2::SecurityGroup", "Properties": {"GroupDescription": "Automatic security group for '
            'Lambda Function teststackpostauth',
            template,
            'Post auth default SG created'
        )
        self.assertIn('"postauth', template, 'Post auth lambda available')
        self.assertIn('"postauthPostAuthenticationCognito', template, 'Post auth permission created')
        self.assertIn(
            '{"Type": "AWS::Lambda::Permission", "Properties": {"Action": "lambda:InvokeFunction", "FunctionName": {'
            '"Fn::GetAtt": ["postauth',
            template,
            'Post auth permissions added for cognito to be able to execute the lambda'
        )
        self.assertIn(
            '"LambdaConfig": {"PostAuthentication": {"Fn::GetAtt": ["postauth',
            template,
            'Post auth added to the lambda triggers config of the user pool'
        )
        self.assertIn(
            '"PreTokenGeneration": {"Fn::GetAtt": ["pretoken',
            template,
            'Pre token added to the lambda triggers config of the user pool'
        )

    def test_refresh_validity(self):
        app = core.App()
        stack = unittest_utils.GenericTestStack(app, 'test-stack')
        app_client_cfg = cognito.CognitoAppClientCfg(name='myuserpoolappclient', refresh_token_validity_in_days=1)
        cognito.CognitoUserPoolWithOidcIdpAndAppClientConstruct(
            scope=stack,
            cid='test_default_cfg',
            user_pool_cfg=default_user_pool_cfg(),
            idp_cfg=default_oidc_idp_cfg(),
            app_client_cfg=app_client_cfg,
            user_pool_domain_cfg=domain_prefix_cfg()
        )
        template = unittest_utils.get_template(app, stack.stack_name)
        self.assertIn(
            '"RefreshTokenValidity": 1, "SupportedIdentityProviders": ["myidp"]}, "DependsOn": ['
            '"testdefaultcfgmyidp',
            template,
            'Refresh validity is applied'
        )
