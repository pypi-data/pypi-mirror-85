from aws_cdk import (
    core,
    aws_cognito,
    aws_certificatemanager
)


class CognitoOidcIdpCfg:
    name: str
    client_id: str
    client_secret: str
    issuer: str
    attribute_request_method: str
    authorized_scopes: str
    attribute_mapping: dict

    def __init__(
            self,
            name: str,
            client_id: str,
            client_secret: str,
            issuer: str,
            attribute_mapping: dict = None,
            attribute_request_method: str = 'POST',
            authorized_scopes: str = 'email profile openid'
    ) -> None:
        """Configuration options for OIDC Id provider

        :param name: the name of the IDP
        :param client_id: the client ID as registered on the IDP side
        :param client_secret: the secret for the client on the IDP side
        :param issuer: the OIDC issue
        :param attribute_mapping: mapping for the attributes from IDP and the user pool
        :param attribute_request_method: the HTTP method used for the requests to the IDP, defaults to POST
        :param authorized_scopes: list of the oauth2 scopes
        """
        self.name = name
        self.client_id = client_id
        self.client_secret = client_secret
        self.issuer = issuer
        self.attribute_mapping = attribute_mapping
        self.attribute_request_method = attribute_request_method
        self.authorized_scopes = authorized_scopes

    @staticmethod
    def create_attribute_mapping(
            custom_attributes: [],
            standard_attributes: aws_cognito.StandardAttributes = None
    ) -> dict:
        """Helper to generate proper mappings for the attributes -the custom attributes must be prefixed with custom: in
        the mappings opposite to the standard attributes, which are directly mapped

        :param custom_attributes: the user pool custom attribute names, without the custom: prefix
        :param standard_attributes: the user pool standard attributes, optional
        :return dict with the mappings in the form custom:attr1=attr1 for the custom attributes and attr1=attr1 for the
        standard attributes
        """
        mappings = dict()
        if standard_attributes:
            for attr in standard_attributes.__dict__['_values'].keys():
                mappings[attr] = attr
        for attr in custom_attributes:
            mappings['custom:' + attr] = attr
        return mappings


class CognitoAppClientCfg:
    auth_flows: aws_cognito.AuthFlow
    name: str
    callback_urls: []
    oauth_flows: []
    oauth_scopes: []
    prevent_user_existence_errors: bool
    generate_secret: bool
    refresh_token_validity_in_days: int

    def __init__(
            self,
            name: str,
            generate_secret: bool = True,
            refresh_token_validity_in_days: int = None,
            auth_flows: aws_cognito.AuthFlow = aws_cognito.AuthFlow(),
            oauth_flows: aws_cognito.OAuthFlows = aws_cognito.OAuthFlows(authorization_code_grant=True),
            oauth_scopes: [] = [aws_cognito.OAuthScope.OPENID, aws_cognito.OAuthScope.PROFILE],
            prevent_user_existence_errors: bool = True,
            callback_urls: [] = None
    ) -> None:
        """Configuration for cognito app client

        :param refresh_token_validity_in_days: the expiration time for the refresh token
        :param generate_secret: controls if a secret for the client should be generated, default True
        :param auth_flows: AuthFlow configuration
        :param oauth_flows: used in the aws_cognito.OAuthSettings config
        :param oauth_scopes: used in the aws_cognito.OAuthSettings config
        :param callback_urls: used in the aws_cognito.OAuthSettings config
        :param prevent_user_existence_errors: default is True for Enabled
        :param name: the name of the app client, will be also used for the id parameter
        """
        self.auth_flows = auth_flows
        self.oauth_flows = oauth_flows
        self.oauth_scopes = oauth_scopes
        self.prevent_user_existence_errors = prevent_user_existence_errors
        self.name = name
        self.callback_urls = callback_urls
        self.generate_secret = generate_secret
        self.refresh_token_validity_in_days = refresh_token_validity_in_days


class CognitoUserPoolCfg:
    user_pool_name: str
    custom_attributes: dict
    user_pool_triggers: aws_cognito.UserPoolTriggers
    standard_attributes: aws_cognito.StandardAttributes
    account_recovery: aws_cognito.AccountRecovery
    mfa: aws_cognito.Mfa
    mfa_second_factor: aws_cognito.MfaSecondFactor

    def __init__(
            self,
            user_pool_name: str,
            custom_attribute_names_string_type: [] = None,
            standard_attributes: aws_cognito.StandardAttributes = None,
            user_pool_triggers: aws_cognito.UserPoolTriggers = None,
            account_recovery: aws_cognito.AccountRecovery = aws_cognito.AccountRecovery.NONE,
            mfa: aws_cognito.Mfa = aws_cognito.Mfa.OFF,
            mfa_second_factor: aws_cognito.MfaSecondFactor = None,
    ) -> None:
        """Construct for CognitoUserPoolCfg

        :param user_pool_name: the name of the user pool
        :param standard_attributes: optional standard attributes configuration for the user pool
        :param user_pool_triggers: lambda triggers configuration
        :param custom_attribute_names_string_type: list of names of custom attributes to be defined in the user pool
        :param account_recovery: the AccountRecovery options, default NONE - only the admin can recover the account
        """
        self.user_pool_name = user_pool_name
        self.custom_attributes = self.prepare_custom_attributes(custom_attribute_names_string_type)
        self.standard_attributes = standard_attributes
        self.user_pool_triggers = user_pool_triggers
        self.account_recovery = account_recovery
        self.mfa = mfa
        self.mfa_second_factor = mfa_second_factor

    @staticmethod
    def prepare_custom_attributes(custom_attribute_names_string_type: []) -> dict:
        if custom_attribute_names_string_type:
            mapping = dict()
            for name in custom_attribute_names_string_type:
                mapping[name] = aws_cognito.StringAttribute(max_len=2048, mutable=True)
            return mapping
        return None


class CognitoUserPoolDomainCfg:
    domain_name: str
    certificate: aws_certificatemanager.ICertificate
    domain_prefix: str

    def __init__(
            self,
            domain_name: str = None,
            certificate: aws_certificatemanager.ICertificate = None,
            domain_prefix: str = None
    ) -> None:
        """Configuration for the user pool domain.

        There are two variants for domains in cognito - prefix only and custom domain. The first one requires only a
        domain_prefix to be provided, the latter the domain_name and a valid certificate for the domain. A validation
        will be done for these two exclusive cases and an Exception is thrown in case of invalid config.

        :param domain_name: the full domain name in case of custom domain, optional if domain_prefix is provided
        :param certificate: the certificate, valid for the provided domain_name, optional if domain_prefix is provided
        :param domain_prefix: the domain prefix in case of prefix only, optional if the domain_name and \
        certificate are provided
        """
        self.domain_prefix = domain_prefix
        self.domain_name = domain_name
        self.certificate = certificate
        if not self.validate():
            raise Exception(
                'Invalid parameters provided. Possible input is either only domain_prefix '
                'OR domain_name and certificate'
            )

    def validate(self) -> bool:
        return self.domain_name and self.certificate or self.domain_prefix


class CognitoUserPoolWithOidcIdpAndAppClientConstruct(core.Construct):
    user_pool: aws_cognito.UserPool
    user_pool_app_client: aws_cognito.UserPoolClient
    user_pool_oidc_provider: aws_cognito.UserPoolClientIdentityProvider
    user_pool_domain: aws_cognito.UserPoolDomain

    def __init__(
            self,
            scope: core.Construct,
            cid: str,
            user_pool_cfg: CognitoUserPoolCfg,
            idp_cfg: CognitoOidcIdpCfg,
            app_client_cfg: CognitoAppClientCfg,
            user_pool_domain_cfg: CognitoUserPoolDomainCfg,
            **kwargs
    ) -> None:
        """This construct wires the necessary components together to create a user pool with OIDC IDP, app client and
        domain

        :param scope: the scope of the construct
        :param cid: the construct unique id within the stack
        :param user_pool_cfg: the configuration for the User Pool
        :param idp_cfg: the configuration for the IDP
        :param app_client_cfg: the configuration for the app client
        :param user_pool_domain_cfg: the user pool domain name configuration
        :param kwargs:
        """
        super().__init__(scope, cid, **kwargs)
        self.user_pool = create_user_pool(self, user_pool_cfg)
        self.user_pool_oidc_provider = create_oidc_idp_provider(self, idp_cfg, self.user_pool)
        self.user_pool_app_client = create_app_client(
            self,
            app_client_cfg,
            self.user_pool,
            [self.user_pool_oidc_provider]
        )
        self.user_pool_domain = create_user_pool_domain(self, user_pool_domain_cfg, self.user_pool)
        self.user_pool_app_client.node.add_dependency(self.user_pool_oidc_provider)


class CognitoUserPoolWithOidcIdpAndAppClientStack(core.Stack):

    def __init__(
            self,
            scope: core.Construct,
            sid: str,
            user_pool_cfg: CognitoUserPoolCfg,
            user_pool_client_cfg: CognitoAppClientCfg,
            user_pool_domain_cfg: CognitoUserPoolDomainCfg,
            user_pool_oidc_idp_cfg: CognitoOidcIdpCfg,
            **kwargs
    ) -> None:
        super().__init__(scope, sid, **kwargs)

        CognitoUserPoolWithOidcIdpAndAppClientConstruct(
            self, sid, user_pool_cfg, user_pool_oidc_idp_cfg, user_pool_client_cfg, user_pool_domain_cfg
        )


def create_user_pool(scope: core.Construct, config: CognitoUserPoolCfg) -> aws_cognito.UserPool:
    """Creates AWS Cognito User Pool with the provided configuration

    :param scope: the scope for the construct
    :param config: the configuration for the User Pool
    :return: the user pool
    """
    user_pool = aws_cognito.UserPool(
        scope=scope,
        id=config.user_pool_name,
        user_pool_name=config.user_pool_name,
        custom_attributes=config.custom_attributes,
        mfa=config.mfa,
        mfa_second_factor=config.mfa_second_factor,
        lambda_triggers=config.user_pool_triggers,
        standard_attributes=config.standard_attributes,
        account_recovery=config.account_recovery
    )
    return user_pool


def create_app_client(
        scope: core.Construct,
        config: CognitoAppClientCfg,
        user_pool: aws_cognito.IUserPool,
        id_providers: [] = None
) -> aws_cognito.UserPoolClient:
    """Creates cognito application client

    :param user_pool: the user pool to add the client to
    :param scope: the scope for the construct
    :param config: the configuration for the app client as CognitoAppClientCfg
    :param id_providers: list of IDPs to be registered to the app client, optional
    :return: aws_aws_cognito.UserPoolClient
    """
    callback_urls = config.callback_urls
    user_pool_client_name = config.name
    supported_identity_providers = [
        aws_cognito.UserPoolClientIdentityProvider.custom(idp.provider_name) for idp in id_providers
    ] if id_providers else None
    app_client = aws_cognito.UserPoolClient(
        scope=scope,
        id=user_pool_client_name,
        user_pool=user_pool,
        auth_flows=config.auth_flows,
        user_pool_client_name=user_pool_client_name,
        generate_secret=config.generate_secret,
        o_auth=aws_cognito.OAuthSettings(
            callback_urls=callback_urls,
            flows=config.oauth_flows,
            scopes=config.oauth_scopes
        ),
        prevent_user_existence_errors=config.prevent_user_existence_errors,
        supported_identity_providers=supported_identity_providers
    )
    if config.refresh_token_validity_in_days:
        cfn: aws_cognito.CfnUserPoolClient = app_client.node.default_child
        cfn.refresh_token_validity = config.refresh_token_validity_in_days
    return app_client


def create_oidc_idp_provider(
        scope: core.Construct,
        config: CognitoOidcIdpCfg,
        user_pool: aws_cognito.IUserPool
) -> aws_cognito.CfnUserPoolIdentityProvider:
    """Creates custom OIDC provider.

    It seems that at the moment there is no high level construct for this in CDK, that's why
    the Cfn form is used.

    :param scope: the scope for the construct
    :param config: the configuration for the IDP
    :param user_pool: the user pool where the IDP is defined
    :return: aws_cognito.CfnUserPoolIdentityProvider
    """
    oidc_provider = aws_cognito.CfnUserPoolIdentityProvider(
        scope,
        id=config.name,
        provider_type='OIDC',
        provider_name=config.name,
        user_pool_id=user_pool.user_pool_id,
        provider_details={
            'client_id': config.client_id,
            'client_secret': config.client_secret,
            'oidc_issuer': config.issuer,
            'attributes_request_method': config.attribute_request_method,
            'authorize_scopes': config.authorized_scopes
        },
        attribute_mapping=config.attribute_mapping
    )
    return oidc_provider


def create_user_pool_domain(
        scope: core.Construct,
        config: CognitoUserPoolDomainCfg,
        user_pool: aws_cognito.IUserPool
) -> aws_cognito.UserPoolDomain:
    """Creates User Pool domain with the provided configuration

    :param user_pool: the user pool for the domain
    :param scope: the scope of the construct
    :param config: the configuration for the domain
    :return: the created UserPoolDomain
    """
    return aws_cognito.UserPoolDomain(
        scope=scope,
        id=config.domain_prefix,
        user_pool=user_pool,
        cognito_domain=aws_cognito.CognitoDomainOptions(domain_prefix=config.domain_prefix)
    ) if config.domain_prefix else aws_cognito.UserPoolDomain(
        scope=scope,
        id=config.domain_name,
        user_pool=user_pool,
        custom_domain=aws_cognito.CustomDomainOptions(
            certificate=config.certificate,
            domain_name=config.domain_name
        )
    )
