# Custom AWS CDK Constructs

![Upload Python Package](https://github.com/raiffeisenbankinternational/awscdk-components-py/workflows/Upload%20Python%20Package/badge.svg?branch=v0.5.0)
![PyPI - Status](https://img.shields.io/pypi/status/rbi-oss-awscdk-components-pkg)

Contains a set of higher level AWS CDK constructs.

see also [AWS CDK](https://github.com/aws/aws-cdk)

Following components are available:

- ALB
- Cognito

Support for HTTPS is implemented. There are additional methods to register target groups of type EC2 and lambda.
Create a simple ALB on port 443 with security groups and with "401 Access denied" fix response as default action:

```python
from awscdk_components.elb.alb_https import (
    AlbHttpsConstruct,
    AlbCfg, 
    add_access_denied_fix_response
)

# create the config
app = core.App()
stack = GenericTestStack(app, 'test-stack')
alb_cfg = AlbCfg(
    alb_name='TestALB',
    vpc=stack.vpc,
    subnets=stack.subnets,
    certificate_arns=['arn:aws:acm:us-east-1:023475735288:certificate/ff6967d7-0fdf-4967-bd68-4caffc983447'],
    cidr_ingress_ranges=['10.0.0.0/16'],
    icmp_ranges=['10.0.0.0/16']
)
alb_construct = AlbHttpsConstruct(stack, 'albhttps', alb_cfg)
add_access_denied_fix_response('fix401resp', alb_construct.https_listener)
```

To add a target group for a given EC2 instance, accessible under /ec2 path, which has a service run also on port 443 (change the port parameter if necessary, i.e. port=8443):

```python
from awscdk_components.elb.alb_utils import (
    register_ec2_as_alb_target
)

alb_construct = AlbHttpsConstruct(stack, 'albhttps', alb_cfg)
ec2 = aws_ec2.Instance(
    scope=stack,
    id='ec2foralb',
    vpc=stack.vpc,
    instance_type=aws_ec2.InstanceType(instance_type_identifier='t3.micro'),
    machine_image=aws_ec2.MachineImage.latest_amazon_linux()
)
register_ec2_as_alb_target(
    stack,
    ec2=ec2,
    listener=alb_construct.https_listener,
    vpc=stack.vpc,
    path_pattern_values=['/ec2'],
    port=443
)
add_access_denied_fix_response('fix401resp', alb_construct.https_listener)
```

More complicated utility method is registering lambda function behind authentication with AWS Cognito rule (currently the low level Cfn constructs for the UserPool are implemented only):

```python
from awscdk_components.elb.alb_utils import (
    register_lambda_target_group_with_cognito_auth_rule
)

alb_construct = AlbHttpsConstruct(stack, 'albhttps', alb_cfg)
function = aws_lambda.Function(
    stack,
    "lambda_function",
    runtime=aws_lambda.Runtime.PYTHON_3_7,
    handler="index.handler",
    code=aws_lambda.Code.from_inline(
        "def handler(event, context): return { 'statusCode': 200, 'body': 'Lambda was invoked successfully.' }"
    ),
    vpc=stack.vpc
)
register_lambda_target_group_with_cognito_auth_rule(
    scope=stack,
    fn=function,
    vpc=stack.vpc,
    listener=alb_construct.https_listener,
    user_pool=user_pool_cfn,
    user_pool_app_client=user_pool_app_client_cfn,
    user_pool_domain=user_pool_domain_cfn,
    path_pattern_values=['/mylambda', '/mylambda/*']
)
add_access_denied_fix_response('fix401resp', alb_construct.https_listener)
```

For more details see the unittests in the tests package.
