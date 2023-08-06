import sgqlc.types


schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class AWSDateTime(sgqlc.types.Scalar):
    __schema__ = schema


class AWSEmail(sgqlc.types.Scalar):
    __schema__ = schema


class AWSJSON(sgqlc.types.Scalar):
    __schema__ = schema


class AlertEvent(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('ASSESSMENT_START', 'ASSESSMENT_END', 'ASSESSMENT_SUMMARY', 'CRITICAL_FINDINGS', 'HIGH_FINDINGS', 'MEDIUM_FINDINGS', 'LOW_FINDINGS', 'INFO_FINDINGS')


class AssessmentState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('PENDING', 'RECON', 'RUNNING', 'COMPLETE', 'FAILED', 'CANCELED')


class AssessmentType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('EXTERNAL', 'CLOUD', 'INTERNAL', 'SOCIAL_ENGINEERING', 'ATTACK_SURFACE_MONITORING')


class AssetConnectionState(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('PENDING_APPROVAL', 'COMPROMISED', 'DISCOVERED')


class AssetSource(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CUSTOMER_DEFINED', 'DISCOVERED')


class AssetType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('IP_ADDRESS', 'HOSTNAME', 'DOMAIN', 'URL', 'CIDR', 'ACCOUNT', 'EMAIL')


Boolean = sgqlc.types.Boolean

class CloudPlatform(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('AWS', 'AZURE', 'GCP')


class Confidence(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('INFO', 'LOW', 'MEDIUM', 'HIGH')


class CredentialLinkType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('DISCOVERED', 'ATTEMPTED_AUTHENTICATION', 'SUCCESSFUL_AUTHENTICATION')


class DateInterval(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('DAY', 'WEEK', 'MONTH', 'QUARTER', 'YEAR')


class DiscoveryMethod(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('PORTSCAN', 'ARPSCAN', 'DNS', 'NBT', 'SMB')


Float = sgqlc.types.Float

class HashType(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('LM', 'NTLM', 'SHA1', 'SHA256', 'SHA256CRYPT', 'SHA512', 'SHA512CRYPT')


ID = sgqlc.types.ID

Int = sgqlc.types.Int

class ModelAttributeTypes(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('binary', 'binarySet', 'bool', 'list', 'map', 'number', 'numberSet', 'string', 'stringSet', '_null')


class ModelSortDirection(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('ASC', 'DESC')


class ScheduleFrequency(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('HOURLY', 'DAILY', 'WEEKLY', 'MONTHLY', 'QUARTERLY', 'YEARLY')


class SearchableAssessmentRunSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'createdAt', 'updatedAt', 'assessmentId', 'writeKey', 'score', 'executionArn', 'stager', 'failReason', 'recon', 'lastRunId')


class SearchableAssessmentSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'createdAt', 'updatedAt', 'name', 'externallyAssessCloudAssets', 'reportRecipients')


class SearchableAssetGroupSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'name')


class SearchableAssetSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'createdAt', 'updatedAt', 'assetIdentifier', 'tags', 'criticality')


class SearchableClientSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'createdAt', 'updatedAt', 'name', 'verified', 'invoices', 'stripeCustomerId', 'stripeCustomer', 'stripeSubscriptionId', 'stripeLatestInvoiceStatus', 'stripeSubscriptionStatus', 'upcomingInvoice', 'users')


class SearchableCredentialSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'createdAt', 'updatedAt', 'name', 'username', 'password', 'domain')


class SearchableFindingSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'assessmentId', 'affectedAssetId', 'createdAt', 'updatedAt', 'title', 'description', 'evidence', 'references', 'recommendations', 'risk', 'fileLinks')


class SearchableLeadSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'assessmentRunId', 'createdAt', 'updatedAt', 'title', 'description', 'evidence', 'references', 'fileLinks')


class SearchableSortDirection(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('asc', 'desc')


class SearchableTTPSortableFields(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('id', 'assessmentRunId', 'assetId', 'createdAt', 'updatedAt', 'executedOn', 'technique', 'url', 'evidence', 'fileLinks')


class Severity(sgqlc.types.Enum):
    __schema__ = schema
    __choices__ = ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFORMATIONAL')


String = sgqlc.types.String


########################################################################
# Input Objects
########################################################################
class AssessmentRunMetadataInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('emails_processed', 'findings_created', 'external_assets_processed', 'cloud_accounts_processed', 'seeds_monitored', 'internal_assessments_executed')
    emails_processed = sgqlc.types.Field(Int, graphql_name='emailsProcessed')
    findings_created = sgqlc.types.Field(Int, graphql_name='findingsCreated')
    external_assets_processed = sgqlc.types.Field(Int, graphql_name='externalAssetsProcessed')
    cloud_accounts_processed = sgqlc.types.Field(Int, graphql_name='cloudAccountsProcessed')
    seeds_monitored = sgqlc.types.Field(Int, graphql_name='seedsMonitored')
    internal_assessments_executed = sgqlc.types.Field(Int, graphql_name='internalAssessmentsExecuted')


class CreateAssessmentAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'assessment_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')


class CreateAssessmentAssetGroupConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_group_id', 'assessment_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetGroupId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')


class CreateAssessmentInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'type', 'name', 'externally_assess_cloud_assets', 'schedule', 'phishing_configuration', 'report_recipients', 'assessment_client_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    type = sgqlc.types.Field(sgqlc.types.non_null(AssessmentType), graphql_name='type')
    name = sgqlc.types.Field(String, graphql_name='name')
    externally_assess_cloud_assets = sgqlc.types.Field(Boolean, graphql_name='externallyAssessCloudAssets')
    schedule = sgqlc.types.Field('ScheduleInput', graphql_name='schedule')
    phishing_configuration = sgqlc.types.Field('PhishingConfigurationInput', graphql_name='phishingConfiguration')
    report_recipients = sgqlc.types.Field(sgqlc.types.list_of(AWSEmail), graphql_name='reportRecipients')
    assessment_client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentClientId')


class CreateAssessmentRunAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'assessment_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')


class CreateAssessmentRunAssetInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_type', 'asset_identifier', 'asset_source', 'tags', 'asset_client_id', 'assessment_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_type = sgqlc.types.Field(sgqlc.types.non_null(AssetType), graphql_name='assetType')
    asset_identifier = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='assetIdentifier')
    asset_source = sgqlc.types.Field(sgqlc.types.non_null(AssetSource), graphql_name='assetSource')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    asset_client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetClientId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')


class CreateAssessmentRunCredentialConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'assessment_id', 'credential_id', 'link_type')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    credential_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='credentialId')
    link_type = sgqlc.types.Field(CredentialLinkType, graphql_name='linkType')


class CreateAssessmentRunCredentialInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'username', 'password', 'hashes', 'domain', 'credential_client_id', 'assessment_id', 'asset_id', 'link_type')
    id = sgqlc.types.Field(ID, graphql_name='id')
    username = sgqlc.types.Field(String, graphql_name='username')
    password = sgqlc.types.Field(String, graphql_name='password')
    hashes = sgqlc.types.Field(sgqlc.types.list_of('HashPairInput'), graphql_name='hashes')
    domain = sgqlc.types.Field(String, graphql_name='domain')
    credential_client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='credentialClientId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    link_type = sgqlc.types.Field(CredentialLinkType, graphql_name='linkType')


class CreateAssessmentRunInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'write_key', 'state', 'score', 'execution_arn', 'phishing_results', 'stager', 'metadata', 'fail_reason', 'recon', 'last_run_id', 'assessment_run_client_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    write_key = sgqlc.types.Field(String, graphql_name='writeKey')
    state = sgqlc.types.Field(AssessmentState, graphql_name='state')
    score = sgqlc.types.Field(Float, graphql_name='score')
    execution_arn = sgqlc.types.Field(String, graphql_name='executionArn')
    phishing_results = sgqlc.types.Field(sgqlc.types.list_of('PhishingResultInput'), graphql_name='phishingResults')
    stager = sgqlc.types.Field(String, graphql_name='stager')
    metadata = sgqlc.types.Field(AssessmentRunMetadataInput, graphql_name='metadata')
    fail_reason = sgqlc.types.Field(String, graphql_name='failReason')
    recon = sgqlc.types.Field(AWSJSON, graphql_name='recon')
    last_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='lastRunId')
    assessment_run_client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentRunClientId')


class CreateAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'discovery_method', 'state', 'assessment_run_id', 'asset_source_id', 'asset_destination_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    discovery_method = sgqlc.types.Field(sgqlc.types.non_null(DiscoveryMethod), graphql_name='discoveryMethod')
    state = sgqlc.types.Field(sgqlc.types.non_null(AssetConnectionState), graphql_name='state')
    assessment_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentRunId')
    asset_source_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetSourceId')
    asset_destination_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetDestinationId')


class CreateAssetGroupConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'group_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetID')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupID')


class CreateAssetGroupInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'asset_group_client_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    asset_group_client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetGroupClientId')


class CreateAssetInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_type', 'asset_identifier', 'asset_source', 'tags', 'criticality', 'asset_client_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_type = sgqlc.types.Field(sgqlc.types.non_null(AssetType), graphql_name='assetType')
    asset_identifier = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='assetIdentifier')
    asset_source = sgqlc.types.Field(sgqlc.types.non_null(AssetSource), graphql_name='assetSource')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    criticality = sgqlc.types.Field(Int, graphql_name='criticality')
    asset_client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetClientId')


class CreateClientConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'client_id', 'name', 'slack_configuration', 'splunk_configuration', 'jira_configuration', 'email_configuration')
    id = sgqlc.types.Field(ID, graphql_name='id')
    client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='clientId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    slack_configuration = sgqlc.types.Field('SlackConfigurationInput', graphql_name='slackConfiguration')
    splunk_configuration = sgqlc.types.Field('SplunkConfigurationInput', graphql_name='splunkConfiguration')
    jira_configuration = sgqlc.types.Field('JiraConfigurationInput', graphql_name='jiraConfiguration')
    email_configuration = sgqlc.types.Field('EmailConfigurationInput', graphql_name='emailConfiguration')


class CreateClientInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'verified', 'invoices', 'stripe_customer_id', 'stripe_customer', 'stripe_subscription_id', 'stripe_subscription_items', 'stripe_latest_invoice_status', 'stripe_subscription_status', 'upcoming_invoice', 'users')
    id = sgqlc.types.Field(ID, graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    verified = sgqlc.types.Field(Boolean, graphql_name='verified')
    invoices = sgqlc.types.Field(AWSJSON, graphql_name='invoices')
    stripe_customer_id = sgqlc.types.Field(String, graphql_name='stripeCustomerId')
    stripe_customer = sgqlc.types.Field(AWSJSON, graphql_name='stripeCustomer')
    stripe_subscription_id = sgqlc.types.Field(String, graphql_name='stripeSubscriptionId')
    stripe_subscription_items = sgqlc.types.Field(sgqlc.types.list_of('StripeSubscriptionItemInput'), graphql_name='stripeSubscriptionItems')
    stripe_latest_invoice_status = sgqlc.types.Field(String, graphql_name='stripeLatestInvoiceStatus')
    stripe_subscription_status = sgqlc.types.Field(String, graphql_name='stripeSubscriptionStatus')
    upcoming_invoice = sgqlc.types.Field(AWSJSON, graphql_name='upcomingInvoice')
    users = sgqlc.types.Field(AWSJSON, graphql_name='users')


class CreateCloudCredentialInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'client_id', 'name', 'access_key', 'secret_key', 'session_token', 'additional_data', 'cloud_platform')
    id = sgqlc.types.Field(ID, graphql_name='id')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='clientId')
    name = sgqlc.types.Field(String, graphql_name='name')
    access_key = sgqlc.types.Field(String, graphql_name='accessKey')
    secret_key = sgqlc.types.Field(String, graphql_name='secretKey')
    session_token = sgqlc.types.Field(String, graphql_name='sessionToken')
    additional_data = sgqlc.types.Field(AWSJSON, graphql_name='additionalData')
    cloud_platform = sgqlc.types.Field(CloudPlatform, graphql_name='cloudPlatform')


class CreateCredentialConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'credential_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    credential_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='credentialId')


class CreateCredentialInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'username', 'password', 'hashes', 'domain', 'credential_client_id')
    id = sgqlc.types.Field(ID, graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    username = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='username')
    password = sgqlc.types.Field(String, graphql_name='password')
    hashes = sgqlc.types.Field(sgqlc.types.list_of('HashPairInput'), graphql_name='hashes')
    domain = sgqlc.types.Field(String, graphql_name='domain')
    credential_client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='credentialClientId')


class CreateFindingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'affected_asset_id', 'severity', 'title', 'description', 'evidence', 'references', 'recommendations', 'files')
    id = sgqlc.types.Field(ID, graphql_name='id')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    affected_asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='affectedAssetId')
    severity = sgqlc.types.Field(sgqlc.types.non_null(Severity), graphql_name='severity')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    evidence = sgqlc.types.Field(AWSJSON, graphql_name='evidence')
    references = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='references')
    recommendations = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='recommendations')
    files = sgqlc.types.Field(sgqlc.types.list_of('S3ObjectInput'), graphql_name='files')


class CreateLeadInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'title', 'description', 'evidence', 'references', 'confidence', 'files')
    id = sgqlc.types.Field(ID, graphql_name='id')
    assessment_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentRunId')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    evidence = sgqlc.types.Field(AWSJSON, graphql_name='evidence')
    references = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='references')
    confidence = sgqlc.types.Field(Confidence, graphql_name='confidence')
    files = sgqlc.types.Field(sgqlc.types.list_of('S3ObjectInput'), graphql_name='files')


class CreateTTPInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'asset_id', 'executed_on', 'technique', 'url', 'evidence', 'files')
    id = sgqlc.types.Field(ID, graphql_name='id')
    assessment_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentRunId')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    executed_on = sgqlc.types.Field(AWSDateTime, graphql_name='executedOn')
    technique = sgqlc.types.Field(String, graphql_name='technique')
    url = sgqlc.types.Field(String, graphql_name='url')
    evidence = sgqlc.types.Field(String, graphql_name='evidence')
    files = sgqlc.types.Field(sgqlc.types.list_of('S3ObjectInput'), graphql_name='files')


class DeleteAssessmentAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssessmentAssetGroupConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssessmentInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssessmentRunAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssessmentRunCredentialConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssessmentRunInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssetGroupConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssetGroupInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteAssetInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteClientConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteClientInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteCloudCredentialInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteCredentialConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteCredentialInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteFindingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteLeadInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class DeleteTTPInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id',)
    id = sgqlc.types.Field(ID, graphql_name='id')


class EmailConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('enabled', 'enabled_events', 'emails')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')
    emails = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AWSEmail))), graphql_name='emails')


class HashPairInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('hash_type', 'hash')
    hash_type = sgqlc.types.Field(sgqlc.types.non_null(HashType), graphql_name='hashType')
    hash = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='hash')


class JiraConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('enabled', 'base_url', 'username', 'secret', 'enabled_events')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='baseUrl')
    username = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='username')
    secret = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='secret')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')


class ModelAssessmentAssetConnectionConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'asset_id', 'assessment_id', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetConnectionConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetConnectionConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentAssetConnectionConditionInput', graphql_name='not')


class ModelAssessmentAssetConnectionFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'assessment_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetConnectionFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetConnectionFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentAssetConnectionFilterInput', graphql_name='not')


class ModelAssessmentAssetGroupConnectionConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'asset_group_id', 'assessment_id', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_group_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetGroupId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetGroupConnectionConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetGroupConnectionConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentAssetGroupConnectionConditionInput', graphql_name='not')


class ModelAssessmentAssetGroupConnectionFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_group_id', 'assessment_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_group_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetGroupId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetGroupConnectionFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentAssetGroupConnectionFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentAssetGroupConnectionFilterInput', graphql_name='not')


class ModelAssessmentConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'type', 'name', 'externally_assess_cloud_assets', 'report_recipients', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    type = sgqlc.types.Field('ModelAssessmentTypeInput', graphql_name='type')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    externally_assess_cloud_assets = sgqlc.types.Field('ModelBooleanInput', graphql_name='externallyAssessCloudAssets')
    report_recipients = sgqlc.types.Field('ModelStringInput', graphql_name='reportRecipients')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentConditionInput', graphql_name='not')


class ModelAssessmentFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'type', 'name', 'externally_assess_cloud_assets', 'report_recipients', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    type = sgqlc.types.Field('ModelAssessmentTypeInput', graphql_name='type')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    externally_assess_cloud_assets = sgqlc.types.Field('ModelBooleanInput', graphql_name='externallyAssessCloudAssets')
    report_recipients = sgqlc.types.Field('ModelStringInput', graphql_name='reportRecipients')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentFilterInput', graphql_name='not')


class ModelAssessmentRunAssetConnectionConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'asset_id', 'assessment_id', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunAssetConnectionConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunAssetConnectionConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentRunAssetConnectionConditionInput', graphql_name='not')


class ModelAssessmentRunAssetConnectionFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'assessment_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunAssetConnectionFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunAssetConnectionFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentRunAssetConnectionFilterInput', graphql_name='not')


class ModelAssessmentRunConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'assessment_id', 'write_key', 'state', 'score', 'execution_arn', 'stager', 'fail_reason', 'recon', 'last_run_id', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    write_key = sgqlc.types.Field('ModelStringInput', graphql_name='writeKey')
    state = sgqlc.types.Field('ModelAssessmentStateInput', graphql_name='state')
    score = sgqlc.types.Field('ModelFloatInput', graphql_name='score')
    execution_arn = sgqlc.types.Field('ModelStringInput', graphql_name='executionArn')
    stager = sgqlc.types.Field('ModelStringInput', graphql_name='stager')
    fail_reason = sgqlc.types.Field('ModelStringInput', graphql_name='failReason')
    recon = sgqlc.types.Field('ModelStringInput', graphql_name='recon')
    last_run_id = sgqlc.types.Field('ModelIDInput', graphql_name='lastRunId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentRunConditionInput', graphql_name='not')


class ModelAssessmentRunCredentialConnectionConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'asset_id', 'assessment_id', 'credential_id', 'link_type', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    credential_id = sgqlc.types.Field('ModelIDInput', graphql_name='credentialId')
    link_type = sgqlc.types.Field('ModelCredentialLinkTypeInput', graphql_name='linkType')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunCredentialConnectionConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunCredentialConnectionConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentRunCredentialConnectionConditionInput', graphql_name='not')


class ModelAssessmentRunCredentialConnectionFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'assessment_id', 'credential_id', 'link_type', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    credential_id = sgqlc.types.Field('ModelIDInput', graphql_name='credentialId')
    link_type = sgqlc.types.Field('ModelCredentialLinkTypeInput', graphql_name='linkType')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunCredentialConnectionFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunCredentialConnectionFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentRunCredentialConnectionFilterInput', graphql_name='not')


class ModelAssessmentRunFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'assessment_id', 'write_key', 'state', 'score', 'execution_arn', 'stager', 'fail_reason', 'recon', 'last_run_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    write_key = sgqlc.types.Field('ModelStringInput', graphql_name='writeKey')
    state = sgqlc.types.Field('ModelAssessmentStateInput', graphql_name='state')
    score = sgqlc.types.Field('ModelFloatInput', graphql_name='score')
    execution_arn = sgqlc.types.Field('ModelStringInput', graphql_name='executionArn')
    stager = sgqlc.types.Field('ModelStringInput', graphql_name='stager')
    fail_reason = sgqlc.types.Field('ModelStringInput', graphql_name='failReason')
    recon = sgqlc.types.Field('ModelStringInput', graphql_name='recon')
    last_run_id = sgqlc.types.Field('ModelIDInput', graphql_name='lastRunId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssessmentRunFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssessmentRunFilterInput', graphql_name='not')


class ModelAssessmentStateInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(AssessmentState, graphql_name='eq')
    ne = sgqlc.types.Field(AssessmentState, graphql_name='ne')


class ModelAssessmentTypeInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(AssessmentType, graphql_name='eq')
    ne = sgqlc.types.Field(AssessmentType, graphql_name='ne')


class ModelAssetConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'asset_type', 'asset_identifier', 'asset_source', 'tags', 'criticality', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_type = sgqlc.types.Field('ModelAssetTypeInput', graphql_name='assetType')
    asset_identifier = sgqlc.types.Field('ModelStringInput', graphql_name='assetIdentifier')
    asset_source = sgqlc.types.Field('ModelAssetSourceInput', graphql_name='assetSource')
    tags = sgqlc.types.Field('ModelStringInput', graphql_name='tags')
    criticality = sgqlc.types.Field('ModelIntInput', graphql_name='criticality')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetConditionInput', graphql_name='not')


class ModelAssetConnectionConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'discovery_method', 'state', 'assessment_run_id', 'asset_source_id', 'asset_destination_id', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    discovery_method = sgqlc.types.Field('ModelDiscoveryMethodInput', graphql_name='discoveryMethod')
    state = sgqlc.types.Field('ModelAssetConnectionStateInput', graphql_name='state')
    assessment_run_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentRunId')
    asset_source_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetSourceId')
    asset_destination_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetDestinationId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetConnectionConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetConnectionConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetConnectionConditionInput', graphql_name='not')


class ModelAssetConnectionFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'discovery_method', 'state', 'assessment_run_id', 'asset_source_id', 'asset_destination_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    discovery_method = sgqlc.types.Field('ModelDiscoveryMethodInput', graphql_name='discoveryMethod')
    state = sgqlc.types.Field('ModelAssetConnectionStateInput', graphql_name='state')
    assessment_run_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentRunId')
    asset_source_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetSourceId')
    asset_destination_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetDestinationId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetConnectionFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetConnectionFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetConnectionFilterInput', graphql_name='not')


class ModelAssetConnectionStateInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(AssetConnectionState, graphql_name='eq')
    ne = sgqlc.types.Field(AssetConnectionState, graphql_name='ne')


class ModelAssetFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_type', 'asset_identifier', 'asset_source', 'tags', 'criticality', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_type = sgqlc.types.Field('ModelAssetTypeInput', graphql_name='assetType')
    asset_identifier = sgqlc.types.Field('ModelStringInput', graphql_name='assetIdentifier')
    asset_source = sgqlc.types.Field('ModelAssetSourceInput', graphql_name='assetSource')
    tags = sgqlc.types.Field('ModelStringInput', graphql_name='tags')
    criticality = sgqlc.types.Field('ModelIntInput', graphql_name='criticality')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetFilterInput', graphql_name='not')


class ModelAssetGroupConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('name', 'and_', 'or_', 'not_')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetGroupConditionInput', graphql_name='not')


class ModelAssetGroupConnectionConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('asset_id', 'group_id', 'and_', 'or_', 'not_')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetID')
    group_id = sgqlc.types.Field('ModelIDInput', graphql_name='groupID')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupConnectionConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupConnectionConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetGroupConnectionConditionInput', graphql_name='not')


class ModelAssetGroupConnectionFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'group_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetID')
    group_id = sgqlc.types.Field('ModelIDInput', graphql_name='groupID')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupConnectionFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupConnectionFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetGroupConnectionFilterInput', graphql_name='not')


class ModelAssetGroupFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelAssetGroupFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelAssetGroupFilterInput', graphql_name='not')


class ModelAssetSourceInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(AssetSource, graphql_name='eq')
    ne = sgqlc.types.Field(AssetSource, graphql_name='ne')


class ModelAssetTypeInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(AssetType, graphql_name='eq')
    ne = sgqlc.types.Field(AssetType, graphql_name='ne')


class ModelBooleanInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'eq', 'attribute_exists', 'attribute_type')
    ne = sgqlc.types.Field(Boolean, graphql_name='ne')
    eq = sgqlc.types.Field(Boolean, graphql_name='eq')
    attribute_exists = sgqlc.types.Field(Boolean, graphql_name='attributeExists')
    attribute_type = sgqlc.types.Field(ModelAttributeTypes, graphql_name='attributeType')


class ModelClientConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'name', 'verified', 'invoices', 'stripe_customer_id', 'stripe_customer', 'stripe_subscription_id', 'stripe_latest_invoice_status', 'stripe_subscription_status', 'upcoming_invoice', 'users', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    verified = sgqlc.types.Field(ModelBooleanInput, graphql_name='verified')
    invoices = sgqlc.types.Field('ModelStringInput', graphql_name='invoices')
    stripe_customer_id = sgqlc.types.Field('ModelStringInput', graphql_name='stripeCustomerId')
    stripe_customer = sgqlc.types.Field('ModelStringInput', graphql_name='stripeCustomer')
    stripe_subscription_id = sgqlc.types.Field('ModelStringInput', graphql_name='stripeSubscriptionId')
    stripe_latest_invoice_status = sgqlc.types.Field('ModelStringInput', graphql_name='stripeLatestInvoiceStatus')
    stripe_subscription_status = sgqlc.types.Field('ModelStringInput', graphql_name='stripeSubscriptionStatus')
    upcoming_invoice = sgqlc.types.Field('ModelStringInput', graphql_name='upcomingInvoice')
    users = sgqlc.types.Field('ModelStringInput', graphql_name='users')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelClientConditionInput', graphql_name='not')


class ModelClientConfigurationConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'name', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientConfigurationConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientConfigurationConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelClientConfigurationConditionInput', graphql_name='not')


class ModelClientConfigurationFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'client_id', 'name', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    client_id = sgqlc.types.Field('ModelIDInput', graphql_name='clientId')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientConfigurationFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientConfigurationFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelClientConfigurationFilterInput', graphql_name='not')


class ModelClientFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'name', 'verified', 'invoices', 'stripe_customer_id', 'stripe_customer', 'stripe_subscription_id', 'stripe_latest_invoice_status', 'stripe_subscription_status', 'upcoming_invoice', 'users', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    verified = sgqlc.types.Field(ModelBooleanInput, graphql_name='verified')
    invoices = sgqlc.types.Field('ModelStringInput', graphql_name='invoices')
    stripe_customer_id = sgqlc.types.Field('ModelStringInput', graphql_name='stripeCustomerId')
    stripe_customer = sgqlc.types.Field('ModelStringInput', graphql_name='stripeCustomer')
    stripe_subscription_id = sgqlc.types.Field('ModelStringInput', graphql_name='stripeSubscriptionId')
    stripe_latest_invoice_status = sgqlc.types.Field('ModelStringInput', graphql_name='stripeLatestInvoiceStatus')
    stripe_subscription_status = sgqlc.types.Field('ModelStringInput', graphql_name='stripeSubscriptionStatus')
    upcoming_invoice = sgqlc.types.Field('ModelStringInput', graphql_name='upcomingInvoice')
    users = sgqlc.types.Field('ModelStringInput', graphql_name='users')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelClientFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelClientFilterInput', graphql_name='not')


class ModelCloudCredentialConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('assessment_id', 'created_at', 'updated_at', 'name', 'access_key', 'secret_key', 'session_token', 'additional_data', 'cloud_platform', 'and_', 'or_', 'not_')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    access_key = sgqlc.types.Field('ModelStringInput', graphql_name='accessKey')
    secret_key = sgqlc.types.Field('ModelStringInput', graphql_name='secretKey')
    session_token = sgqlc.types.Field('ModelStringInput', graphql_name='sessionToken')
    additional_data = sgqlc.types.Field('ModelStringInput', graphql_name='additionalData')
    cloud_platform = sgqlc.types.Field('ModelCloudPlatformInput', graphql_name='cloudPlatform')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCloudCredentialConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCloudCredentialConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelCloudCredentialConditionInput', graphql_name='not')


class ModelCloudCredentialFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'client_id', 'created_at', 'updated_at', 'name', 'access_key', 'secret_key', 'session_token', 'additional_data', 'cloud_platform', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    client_id = sgqlc.types.Field('ModelIDInput', graphql_name='clientId')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    access_key = sgqlc.types.Field('ModelStringInput', graphql_name='accessKey')
    secret_key = sgqlc.types.Field('ModelStringInput', graphql_name='secretKey')
    session_token = sgqlc.types.Field('ModelStringInput', graphql_name='sessionToken')
    additional_data = sgqlc.types.Field('ModelStringInput', graphql_name='additionalData')
    cloud_platform = sgqlc.types.Field('ModelCloudPlatformInput', graphql_name='cloudPlatform')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCloudCredentialFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCloudCredentialFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelCloudCredentialFilterInput', graphql_name='not')


class ModelCloudPlatformInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(CloudPlatform, graphql_name='eq')
    ne = sgqlc.types.Field(CloudPlatform, graphql_name='ne')


class ModelConfidenceInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(Confidence, graphql_name='eq')
    ne = sgqlc.types.Field(Confidence, graphql_name='ne')


class ModelCredentialConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'name', 'username', 'password', 'domain', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    username = sgqlc.types.Field('ModelStringInput', graphql_name='username')
    password = sgqlc.types.Field('ModelStringInput', graphql_name='password')
    domain = sgqlc.types.Field('ModelStringInput', graphql_name='domain')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelCredentialConditionInput', graphql_name='not')


class ModelCredentialConnectionConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('created_at', 'updated_at', 'asset_id', 'credential_id', 'and_', 'or_', 'not_')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    credential_id = sgqlc.types.Field('ModelIDInput', graphql_name='credentialId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialConnectionConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialConnectionConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelCredentialConnectionConditionInput', graphql_name='not')


class ModelCredentialConnectionFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'credential_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='assetId')
    credential_id = sgqlc.types.Field('ModelIDInput', graphql_name='credentialId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialConnectionFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialConnectionFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelCredentialConnectionFilterInput', graphql_name='not')


class ModelCredentialFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'name', 'username', 'password', 'domain', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('ModelStringInput', graphql_name='name')
    username = sgqlc.types.Field('ModelStringInput', graphql_name='username')
    password = sgqlc.types.Field('ModelStringInput', graphql_name='password')
    domain = sgqlc.types.Field('ModelStringInput', graphql_name='domain')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelCredentialFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelCredentialFilterInput', graphql_name='not')


class ModelCredentialLinkTypeInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(CredentialLinkType, graphql_name='eq')
    ne = sgqlc.types.Field(CredentialLinkType, graphql_name='ne')


class ModelDiscoveryMethodInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(DiscoveryMethod, graphql_name='eq')
    ne = sgqlc.types.Field(DiscoveryMethod, graphql_name='ne')


class ModelFindingConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('assessment_id', 'affected_asset_id', 'created_at', 'updated_at', 'severity', 'title', 'description', 'evidence', 'references', 'recommendations', 'risk', 'file_links', 'and_', 'or_', 'not_')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    affected_asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='affectedAssetId')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    severity = sgqlc.types.Field('ModelSeverityInput', graphql_name='severity')
    title = sgqlc.types.Field('ModelStringInput', graphql_name='title')
    description = sgqlc.types.Field('ModelStringInput', graphql_name='description')
    evidence = sgqlc.types.Field('ModelStringInput', graphql_name='evidence')
    references = sgqlc.types.Field('ModelStringInput', graphql_name='references')
    recommendations = sgqlc.types.Field('ModelStringInput', graphql_name='recommendations')
    risk = sgqlc.types.Field('ModelFloatInput', graphql_name='risk')
    file_links = sgqlc.types.Field('ModelStringInput', graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelFindingConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelFindingConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelFindingConditionInput', graphql_name='not')


class ModelFindingFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'affected_asset_id', 'created_at', 'updated_at', 'severity', 'title', 'description', 'evidence', 'references', 'recommendations', 'risk', 'file_links', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('ModelIDInput', graphql_name='id')
    assessment_id = sgqlc.types.Field('ModelIDInput', graphql_name='assessmentId')
    affected_asset_id = sgqlc.types.Field('ModelIDInput', graphql_name='affectedAssetId')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    severity = sgqlc.types.Field('ModelSeverityInput', graphql_name='severity')
    title = sgqlc.types.Field('ModelStringInput', graphql_name='title')
    description = sgqlc.types.Field('ModelStringInput', graphql_name='description')
    evidence = sgqlc.types.Field('ModelStringInput', graphql_name='evidence')
    references = sgqlc.types.Field('ModelStringInput', graphql_name='references')
    recommendations = sgqlc.types.Field('ModelStringInput', graphql_name='recommendations')
    risk = sgqlc.types.Field('ModelFloatInput', graphql_name='risk')
    file_links = sgqlc.types.Field('ModelStringInput', graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelFindingFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelFindingFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelFindingFilterInput', graphql_name='not')


class ModelFloatInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'eq', 'le', 'lt', 'ge', 'gt', 'between', 'attribute_exists', 'attribute_type')
    ne = sgqlc.types.Field(Float, graphql_name='ne')
    eq = sgqlc.types.Field(Float, graphql_name='eq')
    le = sgqlc.types.Field(Float, graphql_name='le')
    lt = sgqlc.types.Field(Float, graphql_name='lt')
    ge = sgqlc.types.Field(Float, graphql_name='ge')
    gt = sgqlc.types.Field(Float, graphql_name='gt')
    between = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='between')
    attribute_exists = sgqlc.types.Field(Boolean, graphql_name='attributeExists')
    attribute_type = sgqlc.types.Field(ModelAttributeTypes, graphql_name='attributeType')


class ModelIDInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'eq', 'le', 'lt', 'ge', 'gt', 'contains', 'not_contains', 'between', 'begins_with', 'attribute_exists', 'attribute_type', 'size')
    ne = sgqlc.types.Field(ID, graphql_name='ne')
    eq = sgqlc.types.Field(ID, graphql_name='eq')
    le = sgqlc.types.Field(ID, graphql_name='le')
    lt = sgqlc.types.Field(ID, graphql_name='lt')
    ge = sgqlc.types.Field(ID, graphql_name='ge')
    gt = sgqlc.types.Field(ID, graphql_name='gt')
    contains = sgqlc.types.Field(ID, graphql_name='contains')
    not_contains = sgqlc.types.Field(ID, graphql_name='notContains')
    between = sgqlc.types.Field(sgqlc.types.list_of(ID), graphql_name='between')
    begins_with = sgqlc.types.Field(ID, graphql_name='beginsWith')
    attribute_exists = sgqlc.types.Field(Boolean, graphql_name='attributeExists')
    attribute_type = sgqlc.types.Field(ModelAttributeTypes, graphql_name='attributeType')
    size = sgqlc.types.Field('ModelSizeInput', graphql_name='size')


class ModelIDKeyConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'le', 'lt', 'ge', 'gt', 'between', 'begins_with')
    eq = sgqlc.types.Field(ID, graphql_name='eq')
    le = sgqlc.types.Field(ID, graphql_name='le')
    lt = sgqlc.types.Field(ID, graphql_name='lt')
    ge = sgqlc.types.Field(ID, graphql_name='ge')
    gt = sgqlc.types.Field(ID, graphql_name='gt')
    between = sgqlc.types.Field(sgqlc.types.list_of(ID), graphql_name='between')
    begins_with = sgqlc.types.Field(ID, graphql_name='beginsWith')


class ModelIntInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'eq', 'le', 'lt', 'ge', 'gt', 'between', 'attribute_exists', 'attribute_type')
    ne = sgqlc.types.Field(Int, graphql_name='ne')
    eq = sgqlc.types.Field(Int, graphql_name='eq')
    le = sgqlc.types.Field(Int, graphql_name='le')
    lt = sgqlc.types.Field(Int, graphql_name='lt')
    ge = sgqlc.types.Field(Int, graphql_name='ge')
    gt = sgqlc.types.Field(Int, graphql_name='gt')
    between = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='between')
    attribute_exists = sgqlc.types.Field(Boolean, graphql_name='attributeExists')
    attribute_type = sgqlc.types.Field(ModelAttributeTypes, graphql_name='attributeType')


class ModelLeadConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('assessment_run_id', 'created_at', 'updated_at', 'title', 'description', 'evidence', 'references', 'confidence', 'file_links', 'and_', 'or_', 'not_')
    assessment_run_id = sgqlc.types.Field(ModelIDInput, graphql_name='assessmentRunId')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    title = sgqlc.types.Field('ModelStringInput', graphql_name='title')
    description = sgqlc.types.Field('ModelStringInput', graphql_name='description')
    evidence = sgqlc.types.Field('ModelStringInput', graphql_name='evidence')
    references = sgqlc.types.Field('ModelStringInput', graphql_name='references')
    confidence = sgqlc.types.Field(ModelConfidenceInput, graphql_name='confidence')
    file_links = sgqlc.types.Field('ModelStringInput', graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelLeadConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelLeadConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelLeadConditionInput', graphql_name='not')


class ModelLeadFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'created_at', 'updated_at', 'title', 'description', 'evidence', 'references', 'confidence', 'file_links', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field(ModelIDInput, graphql_name='id')
    assessment_run_id = sgqlc.types.Field(ModelIDInput, graphql_name='assessmentRunId')
    created_at = sgqlc.types.Field('ModelStringInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('ModelStringInput', graphql_name='updatedAt')
    title = sgqlc.types.Field('ModelStringInput', graphql_name='title')
    description = sgqlc.types.Field('ModelStringInput', graphql_name='description')
    evidence = sgqlc.types.Field('ModelStringInput', graphql_name='evidence')
    references = sgqlc.types.Field('ModelStringInput', graphql_name='references')
    confidence = sgqlc.types.Field(ModelConfidenceInput, graphql_name='confidence')
    file_links = sgqlc.types.Field('ModelStringInput', graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelLeadFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelLeadFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelLeadFilterInput', graphql_name='not')


class ModelSeverityInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(Severity, graphql_name='eq')
    ne = sgqlc.types.Field(Severity, graphql_name='ne')


class ModelSizeInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'eq', 'le', 'lt', 'ge', 'gt', 'between')
    ne = sgqlc.types.Field(Int, graphql_name='ne')
    eq = sgqlc.types.Field(Int, graphql_name='eq')
    le = sgqlc.types.Field(Int, graphql_name='le')
    lt = sgqlc.types.Field(Int, graphql_name='lt')
    ge = sgqlc.types.Field(Int, graphql_name='ge')
    gt = sgqlc.types.Field(Int, graphql_name='gt')
    between = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='between')


class ModelStringInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'eq', 'le', 'lt', 'ge', 'gt', 'contains', 'not_contains', 'between', 'begins_with', 'attribute_exists', 'attribute_type', 'size')
    ne = sgqlc.types.Field(String, graphql_name='ne')
    eq = sgqlc.types.Field(String, graphql_name='eq')
    le = sgqlc.types.Field(String, graphql_name='le')
    lt = sgqlc.types.Field(String, graphql_name='lt')
    ge = sgqlc.types.Field(String, graphql_name='ge')
    gt = sgqlc.types.Field(String, graphql_name='gt')
    contains = sgqlc.types.Field(String, graphql_name='contains')
    not_contains = sgqlc.types.Field(String, graphql_name='notContains')
    between = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='between')
    begins_with = sgqlc.types.Field(String, graphql_name='beginsWith')
    attribute_exists = sgqlc.types.Field(Boolean, graphql_name='attributeExists')
    attribute_type = sgqlc.types.Field(ModelAttributeTypes, graphql_name='attributeType')
    size = sgqlc.types.Field(ModelSizeInput, graphql_name='size')


class ModelStringKeyConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'le', 'lt', 'ge', 'gt', 'between', 'begins_with')
    eq = sgqlc.types.Field(String, graphql_name='eq')
    le = sgqlc.types.Field(String, graphql_name='le')
    lt = sgqlc.types.Field(String, graphql_name='lt')
    ge = sgqlc.types.Field(String, graphql_name='ge')
    gt = sgqlc.types.Field(String, graphql_name='gt')
    between = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='between')
    begins_with = sgqlc.types.Field(String, graphql_name='beginsWith')


class ModelTTPConditionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('assessment_run_id', 'asset_id', 'created_at', 'updated_at', 'executed_on', 'technique', 'url', 'evidence', 'file_links', 'and_', 'or_', 'not_')
    assessment_run_id = sgqlc.types.Field(ModelIDInput, graphql_name='assessmentRunId')
    asset_id = sgqlc.types.Field(ModelIDInput, graphql_name='assetId')
    created_at = sgqlc.types.Field(ModelStringInput, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(ModelStringInput, graphql_name='updatedAt')
    executed_on = sgqlc.types.Field(ModelStringInput, graphql_name='executedOn')
    technique = sgqlc.types.Field(ModelStringInput, graphql_name='technique')
    url = sgqlc.types.Field(ModelStringInput, graphql_name='url')
    evidence = sgqlc.types.Field(ModelStringInput, graphql_name='evidence')
    file_links = sgqlc.types.Field(ModelStringInput, graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelTTPConditionInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelTTPConditionInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelTTPConditionInput', graphql_name='not')


class ModelTTPFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'asset_id', 'created_at', 'updated_at', 'executed_on', 'technique', 'url', 'evidence', 'file_links', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field(ModelIDInput, graphql_name='id')
    assessment_run_id = sgqlc.types.Field(ModelIDInput, graphql_name='assessmentRunId')
    asset_id = sgqlc.types.Field(ModelIDInput, graphql_name='assetId')
    created_at = sgqlc.types.Field(ModelStringInput, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(ModelStringInput, graphql_name='updatedAt')
    executed_on = sgqlc.types.Field(ModelStringInput, graphql_name='executedOn')
    technique = sgqlc.types.Field(ModelStringInput, graphql_name='technique')
    url = sgqlc.types.Field(ModelStringInput, graphql_name='url')
    evidence = sgqlc.types.Field(ModelStringInput, graphql_name='evidence')
    file_links = sgqlc.types.Field(ModelStringInput, graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('ModelTTPFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('ModelTTPFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('ModelTTPFilterInput', graphql_name='not')


class PhishingConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('template', 'subject', 'landing_page', 'send_from', 'redirect_url', 'hours')
    template = sgqlc.types.Field(String, graphql_name='template')
    subject = sgqlc.types.Field(String, graphql_name='subject')
    landing_page = sgqlc.types.Field(String, graphql_name='landingPage')
    send_from = sgqlc.types.Field(String, graphql_name='sendFrom')
    redirect_url = sgqlc.types.Field(String, graphql_name='redirectUrl')
    hours = sgqlc.types.Field(Int, graphql_name='hours')


class PhishingResultInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('email', 'status', 'ip', 'latitude', 'longitude')
    email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='email')
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='status')
    ip = sgqlc.types.Field(String, graphql_name='ip')
    latitude = sgqlc.types.Field(Float, graphql_name='latitude')
    longitude = sgqlc.types.Field(Float, graphql_name='longitude')


class S3ObjectInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('bucket', 'key', 'region', 'local_uri', 'mime_type')
    bucket = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='bucket')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    region = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='region')
    local_uri = sgqlc.types.Field(String, graphql_name='localUri')
    mime_type = sgqlc.types.Field(String, graphql_name='mimeType')


class ScheduleInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('assessment_id', 'frequency', 'time_expression')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    frequency = sgqlc.types.Field(sgqlc.types.non_null(ScheduleFrequency), graphql_name='frequency')
    time_expression = sgqlc.types.Field(sgqlc.types.non_null('TimeExpressionInput'), graphql_name='timeExpression')


class SearchableAssessmentFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'name', 'externally_assess_cloud_assets', 'report_recipients', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='id')
    created_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='name')
    externally_assess_cloud_assets = sgqlc.types.Field('SearchableBooleanFilterInput', graphql_name='externallyAssessCloudAssets')
    report_recipients = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='reportRecipients')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssessmentFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssessmentFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableAssessmentFilterInput', graphql_name='not')


class SearchableAssessmentRunFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'assessment_id', 'write_key', 'score', 'execution_arn', 'stager', 'fail_reason', 'recon', 'last_run_id', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='id')
    created_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='updatedAt')
    assessment_id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='assessmentId')
    write_key = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='writeKey')
    score = sgqlc.types.Field('SearchableFloatFilterInput', graphql_name='score')
    execution_arn = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='executionArn')
    stager = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='stager')
    fail_reason = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='failReason')
    recon = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='recon')
    last_run_id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='lastRunId')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssessmentRunFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssessmentRunFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableAssessmentRunFilterInput', graphql_name='not')


class SearchableAssessmentRunSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableAssessmentRunSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableAssessmentSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableAssessmentSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableAssetFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_identifier', 'tags', 'criticality', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='id')
    created_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='updatedAt')
    asset_identifier = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='assetIdentifier')
    tags = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='tags')
    criticality = sgqlc.types.Field('SearchableIntFilterInput', graphql_name='criticality')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssetFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssetFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableAssetFilterInput', graphql_name='not')


class SearchableAssetGroupFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='id')
    name = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='name')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssetGroupFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableAssetGroupFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableAssetGroupFilterInput', graphql_name='not')


class SearchableAssetGroupSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableAssetGroupSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableAssetSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableAssetSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableBooleanFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('eq', 'ne')
    eq = sgqlc.types.Field(Boolean, graphql_name='eq')
    ne = sgqlc.types.Field(Boolean, graphql_name='ne')


class SearchableClientFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'name', 'verified', 'invoices', 'stripe_customer_id', 'stripe_customer', 'stripe_subscription_id', 'stripe_latest_invoice_status', 'stripe_subscription_status', 'upcoming_invoice', 'users', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='id')
    created_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='name')
    verified = sgqlc.types.Field(SearchableBooleanFilterInput, graphql_name='verified')
    invoices = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='invoices')
    stripe_customer_id = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='stripeCustomerId')
    stripe_customer = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='stripeCustomer')
    stripe_subscription_id = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='stripeSubscriptionId')
    stripe_latest_invoice_status = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='stripeLatestInvoiceStatus')
    stripe_subscription_status = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='stripeSubscriptionStatus')
    upcoming_invoice = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='upcomingInvoice')
    users = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='users')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableClientFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableClientFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableClientFilterInput', graphql_name='not')


class SearchableClientSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableClientSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableCredentialFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'name', 'username', 'password', 'domain', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='id')
    created_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='updatedAt')
    name = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='name')
    username = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='username')
    password = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='password')
    domain = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='domain')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableCredentialFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableCredentialFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableCredentialFilterInput', graphql_name='not')


class SearchableCredentialSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableCredentialSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableFindingFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'affected_asset_id', 'created_at', 'updated_at', 'title', 'description', 'evidence', 'references', 'recommendations', 'risk', 'file_links', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='id')
    assessment_id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='assessmentId')
    affected_asset_id = sgqlc.types.Field('SearchableIDFilterInput', graphql_name='affectedAssetId')
    created_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='updatedAt')
    title = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='title')
    description = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='description')
    evidence = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='evidence')
    references = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='references')
    recommendations = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='recommendations')
    risk = sgqlc.types.Field('SearchableFloatFilterInput', graphql_name='risk')
    file_links = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableFindingFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableFindingFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableFindingFilterInput', graphql_name='not')


class SearchableFindingSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableFindingSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableFloatFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'gt', 'lt', 'gte', 'lte', 'eq', 'range')
    ne = sgqlc.types.Field(Float, graphql_name='ne')
    gt = sgqlc.types.Field(Float, graphql_name='gt')
    lt = sgqlc.types.Field(Float, graphql_name='lt')
    gte = sgqlc.types.Field(Float, graphql_name='gte')
    lte = sgqlc.types.Field(Float, graphql_name='lte')
    eq = sgqlc.types.Field(Float, graphql_name='eq')
    range = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='range')


class SearchableIDFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'gt', 'lt', 'gte', 'lte', 'eq', 'match', 'match_phrase', 'match_phrase_prefix', 'multi_match', 'exists', 'wildcard', 'regexp')
    ne = sgqlc.types.Field(ID, graphql_name='ne')
    gt = sgqlc.types.Field(ID, graphql_name='gt')
    lt = sgqlc.types.Field(ID, graphql_name='lt')
    gte = sgqlc.types.Field(ID, graphql_name='gte')
    lte = sgqlc.types.Field(ID, graphql_name='lte')
    eq = sgqlc.types.Field(ID, graphql_name='eq')
    match = sgqlc.types.Field(ID, graphql_name='match')
    match_phrase = sgqlc.types.Field(ID, graphql_name='matchPhrase')
    match_phrase_prefix = sgqlc.types.Field(ID, graphql_name='matchPhrasePrefix')
    multi_match = sgqlc.types.Field(ID, graphql_name='multiMatch')
    exists = sgqlc.types.Field(Boolean, graphql_name='exists')
    wildcard = sgqlc.types.Field(ID, graphql_name='wildcard')
    regexp = sgqlc.types.Field(ID, graphql_name='regexp')


class SearchableIntFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'gt', 'lt', 'gte', 'lte', 'eq', 'range')
    ne = sgqlc.types.Field(Int, graphql_name='ne')
    gt = sgqlc.types.Field(Int, graphql_name='gt')
    lt = sgqlc.types.Field(Int, graphql_name='lt')
    gte = sgqlc.types.Field(Int, graphql_name='gte')
    lte = sgqlc.types.Field(Int, graphql_name='lte')
    eq = sgqlc.types.Field(Int, graphql_name='eq')
    range = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='range')


class SearchableLeadFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'created_at', 'updated_at', 'title', 'description', 'evidence', 'references', 'file_links', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field(SearchableIDFilterInput, graphql_name='id')
    assessment_run_id = sgqlc.types.Field(SearchableIDFilterInput, graphql_name='assessmentRunId')
    created_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='createdAt')
    updated_at = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='updatedAt')
    title = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='title')
    description = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='description')
    evidence = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='evidence')
    references = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='references')
    file_links = sgqlc.types.Field('SearchableStringFilterInput', graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableLeadFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableLeadFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableLeadFilterInput', graphql_name='not')


class SearchableLeadSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableLeadSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SearchableStringFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('ne', 'gt', 'lt', 'gte', 'lte', 'eq', 'match', 'match_phrase', 'match_phrase_prefix', 'multi_match', 'exists', 'wildcard', 'regexp')
    ne = sgqlc.types.Field(String, graphql_name='ne')
    gt = sgqlc.types.Field(String, graphql_name='gt')
    lt = sgqlc.types.Field(String, graphql_name='lt')
    gte = sgqlc.types.Field(String, graphql_name='gte')
    lte = sgqlc.types.Field(String, graphql_name='lte')
    eq = sgqlc.types.Field(String, graphql_name='eq')
    match = sgqlc.types.Field(String, graphql_name='match')
    match_phrase = sgqlc.types.Field(String, graphql_name='matchPhrase')
    match_phrase_prefix = sgqlc.types.Field(String, graphql_name='matchPhrasePrefix')
    multi_match = sgqlc.types.Field(String, graphql_name='multiMatch')
    exists = sgqlc.types.Field(Boolean, graphql_name='exists')
    wildcard = sgqlc.types.Field(String, graphql_name='wildcard')
    regexp = sgqlc.types.Field(String, graphql_name='regexp')


class SearchableTTPFilterInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'asset_id', 'created_at', 'updated_at', 'executed_on', 'technique', 'url', 'evidence', 'file_links', 'and_', 'or_', 'not_')
    id = sgqlc.types.Field(SearchableIDFilterInput, graphql_name='id')
    assessment_run_id = sgqlc.types.Field(SearchableIDFilterInput, graphql_name='assessmentRunId')
    asset_id = sgqlc.types.Field(SearchableIDFilterInput, graphql_name='assetId')
    created_at = sgqlc.types.Field(SearchableStringFilterInput, graphql_name='createdAt')
    updated_at = sgqlc.types.Field(SearchableStringFilterInput, graphql_name='updatedAt')
    executed_on = sgqlc.types.Field(SearchableStringFilterInput, graphql_name='executedOn')
    technique = sgqlc.types.Field(SearchableStringFilterInput, graphql_name='technique')
    url = sgqlc.types.Field(SearchableStringFilterInput, graphql_name='url')
    evidence = sgqlc.types.Field(SearchableStringFilterInput, graphql_name='evidence')
    file_links = sgqlc.types.Field(SearchableStringFilterInput, graphql_name='fileLinks')
    and_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableTTPFilterInput'), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of('SearchableTTPFilterInput'), graphql_name='or')
    not_ = sgqlc.types.Field('SearchableTTPFilterInput', graphql_name='not')


class SearchableTTPSortInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('field', 'direction')
    field = sgqlc.types.Field(SearchableTTPSortableFields, graphql_name='field')
    direction = sgqlc.types.Field(SearchableSortDirection, graphql_name='direction')


class SlackConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('enabled', 'webhook_url', 'enabled_events')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    webhook_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='webhookUrl')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')


class SplunkConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('enabled', 'hec_url', 'hec_token', 'enabled_events')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    hec_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='hecUrl')
    hec_token = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='hecToken')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')


class StripeSubscriptionItemInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('subscription_item_id', 'nickname', 'product_id')
    subscription_item_id = sgqlc.types.Field(String, graphql_name='subscriptionItemId')
    nickname = sgqlc.types.Field(String, graphql_name='nickname')
    product_id = sgqlc.types.Field(String, graphql_name='productId')


class TimeExpressionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('minute', 'hour', 'day_of_month', 'month', 'day_of_week', 'year')
    minute = sgqlc.types.Field(String, graphql_name='minute')
    hour = sgqlc.types.Field(String, graphql_name='hour')
    day_of_month = sgqlc.types.Field(String, graphql_name='dayOfMonth')
    month = sgqlc.types.Field(String, graphql_name='month')
    day_of_week = sgqlc.types.Field(String, graphql_name='dayOfWeek')
    year = sgqlc.types.Field(String, graphql_name='year')


class UpdateAssessmentAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'assessment_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_id = sgqlc.types.Field(ID, graphql_name='assetId')
    assessment_id = sgqlc.types.Field(ID, graphql_name='assessmentId')


class UpdateAssessmentAssetGroupConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_group_id', 'assessment_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_group_id = sgqlc.types.Field(ID, graphql_name='assetGroupId')
    assessment_id = sgqlc.types.Field(ID, graphql_name='assessmentId')


class UpdateAssessmentInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'type', 'name', 'externally_assess_cloud_assets', 'schedule', 'phishing_configuration', 'report_recipients', 'assessment_client_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    type = sgqlc.types.Field(AssessmentType, graphql_name='type')
    name = sgqlc.types.Field(String, graphql_name='name')
    externally_assess_cloud_assets = sgqlc.types.Field(Boolean, graphql_name='externallyAssessCloudAssets')
    schedule = sgqlc.types.Field(ScheduleInput, graphql_name='schedule')
    phishing_configuration = sgqlc.types.Field(PhishingConfigurationInput, graphql_name='phishingConfiguration')
    report_recipients = sgqlc.types.Field(sgqlc.types.list_of(AWSEmail), graphql_name='reportRecipients')
    assessment_client_id = sgqlc.types.Field(ID, graphql_name='assessmentClientId')


class UpdateAssessmentRunAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'assessment_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_id = sgqlc.types.Field(ID, graphql_name='assetId')
    assessment_id = sgqlc.types.Field(ID, graphql_name='assessmentId')


class UpdateAssessmentRunCredentialConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'assessment_id', 'credential_id', 'link_type')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_id = sgqlc.types.Field(ID, graphql_name='assetId')
    assessment_id = sgqlc.types.Field(ID, graphql_name='assessmentId')
    credential_id = sgqlc.types.Field(ID, graphql_name='credentialId')
    link_type = sgqlc.types.Field(CredentialLinkType, graphql_name='linkType')


class UpdateAssessmentRunInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'write_key', 'state', 'score', 'execution_arn', 'phishing_results', 'stager', 'metadata', 'fail_reason', 'recon', 'last_run_id', 'assessment_run_client_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_id = sgqlc.types.Field(ID, graphql_name='assessmentId')
    write_key = sgqlc.types.Field(String, graphql_name='writeKey')
    state = sgqlc.types.Field(AssessmentState, graphql_name='state')
    score = sgqlc.types.Field(Float, graphql_name='score')
    execution_arn = sgqlc.types.Field(String, graphql_name='executionArn')
    phishing_results = sgqlc.types.Field(sgqlc.types.list_of(PhishingResultInput), graphql_name='phishingResults')
    stager = sgqlc.types.Field(String, graphql_name='stager')
    metadata = sgqlc.types.Field(AssessmentRunMetadataInput, graphql_name='metadata')
    fail_reason = sgqlc.types.Field(String, graphql_name='failReason')
    recon = sgqlc.types.Field(AWSJSON, graphql_name='recon')
    last_run_id = sgqlc.types.Field(ID, graphql_name='lastRunId')
    assessment_run_client_id = sgqlc.types.Field(ID, graphql_name='assessmentRunClientId')


class UpdateAssetConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'discovery_method', 'state', 'assessment_run_id', 'asset_source_id', 'asset_destination_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    discovery_method = sgqlc.types.Field(DiscoveryMethod, graphql_name='discoveryMethod')
    state = sgqlc.types.Field(AssetConnectionState, graphql_name='state')
    assessment_run_id = sgqlc.types.Field(ID, graphql_name='assessmentRunId')
    asset_source_id = sgqlc.types.Field(ID, graphql_name='assetSourceId')
    asset_destination_id = sgqlc.types.Field(ID, graphql_name='assetDestinationId')


class UpdateAssetGroupConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'group_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_id = sgqlc.types.Field(ID, graphql_name='assetID')
    group_id = sgqlc.types.Field(ID, graphql_name='groupID')


class UpdateAssetGroupInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'asset_group_client_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    asset_group_client_id = sgqlc.types.Field(ID, graphql_name='assetGroupClientId')


class UpdateAssetInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_type', 'asset_identifier', 'asset_source', 'tags', 'criticality', 'asset_client_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_type = sgqlc.types.Field(AssetType, graphql_name='assetType')
    asset_identifier = sgqlc.types.Field(String, graphql_name='assetIdentifier')
    asset_source = sgqlc.types.Field(AssetSource, graphql_name='assetSource')
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    criticality = sgqlc.types.Field(Int, graphql_name='criticality')
    asset_client_id = sgqlc.types.Field(ID, graphql_name='assetClientId')


class UpdateClientConfigurationInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'client_id', 'name', 'slack_configuration', 'splunk_configuration', 'jira_configuration', 'email_configuration')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    client_id = sgqlc.types.Field(ID, graphql_name='clientId')
    name = sgqlc.types.Field(String, graphql_name='name')
    slack_configuration = sgqlc.types.Field(SlackConfigurationInput, graphql_name='slackConfiguration')
    splunk_configuration = sgqlc.types.Field(SplunkConfigurationInput, graphql_name='splunkConfiguration')
    jira_configuration = sgqlc.types.Field(JiraConfigurationInput, graphql_name='jiraConfiguration')
    email_configuration = sgqlc.types.Field(EmailConfigurationInput, graphql_name='emailConfiguration')


class UpdateClientInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'verified', 'invoices', 'stripe_customer_id', 'stripe_customer', 'stripe_subscription_id', 'stripe_subscription_items', 'stripe_latest_invoice_status', 'stripe_subscription_status', 'upcoming_invoice', 'users')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    verified = sgqlc.types.Field(Boolean, graphql_name='verified')
    invoices = sgqlc.types.Field(AWSJSON, graphql_name='invoices')
    stripe_customer_id = sgqlc.types.Field(String, graphql_name='stripeCustomerId')
    stripe_customer = sgqlc.types.Field(AWSJSON, graphql_name='stripeCustomer')
    stripe_subscription_id = sgqlc.types.Field(String, graphql_name='stripeSubscriptionId')
    stripe_subscription_items = sgqlc.types.Field(sgqlc.types.list_of(StripeSubscriptionItemInput), graphql_name='stripeSubscriptionItems')
    stripe_latest_invoice_status = sgqlc.types.Field(String, graphql_name='stripeLatestInvoiceStatus')
    stripe_subscription_status = sgqlc.types.Field(String, graphql_name='stripeSubscriptionStatus')
    upcoming_invoice = sgqlc.types.Field(AWSJSON, graphql_name='upcomingInvoice')
    users = sgqlc.types.Field(AWSJSON, graphql_name='users')


class UpdateCloudCredentialInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'client_id', 'name', 'access_key', 'secret_key', 'session_token', 'additional_data', 'cloud_platform')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_id = sgqlc.types.Field(ID, graphql_name='assessmentId')
    client_id = sgqlc.types.Field(ID, graphql_name='clientId')
    name = sgqlc.types.Field(String, graphql_name='name')
    access_key = sgqlc.types.Field(String, graphql_name='accessKey')
    secret_key = sgqlc.types.Field(String, graphql_name='secretKey')
    session_token = sgqlc.types.Field(String, graphql_name='sessionToken')
    additional_data = sgqlc.types.Field(AWSJSON, graphql_name='additionalData')
    cloud_platform = sgqlc.types.Field(CloudPlatform, graphql_name='cloudPlatform')


class UpdateCredentialConnectionInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'credential_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_id = sgqlc.types.Field(ID, graphql_name='assetId')
    credential_id = sgqlc.types.Field(ID, graphql_name='credentialId')


class UpdateCredentialInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'username', 'password', 'hashes', 'domain', 'credential_client_id')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(String, graphql_name='name')
    username = sgqlc.types.Field(String, graphql_name='username')
    password = sgqlc.types.Field(String, graphql_name='password')
    hashes = sgqlc.types.Field(sgqlc.types.list_of(HashPairInput), graphql_name='hashes')
    domain = sgqlc.types.Field(String, graphql_name='domain')
    credential_client_id = sgqlc.types.Field(ID, graphql_name='credentialClientId')


class UpdateFindingInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'affected_asset_id', 'severity', 'title', 'description', 'evidence', 'references', 'recommendations', 'risk', 'files', 'file_links')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_id = sgqlc.types.Field(ID, graphql_name='assessmentId')
    affected_asset_id = sgqlc.types.Field(ID, graphql_name='affectedAssetId')
    severity = sgqlc.types.Field(Severity, graphql_name='severity')
    title = sgqlc.types.Field(String, graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    evidence = sgqlc.types.Field(AWSJSON, graphql_name='evidence')
    references = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='references')
    recommendations = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='recommendations')
    risk = sgqlc.types.Field(Float, graphql_name='risk')
    files = sgqlc.types.Field(sgqlc.types.list_of(S3ObjectInput), graphql_name='files')
    file_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fileLinks')


class UpdateLeadInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'title', 'description', 'evidence', 'references', 'confidence', 'files', 'file_links')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_run_id = sgqlc.types.Field(ID, graphql_name='assessmentRunId')
    title = sgqlc.types.Field(String, graphql_name='title')
    description = sgqlc.types.Field(String, graphql_name='description')
    evidence = sgqlc.types.Field(AWSJSON, graphql_name='evidence')
    references = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='references')
    confidence = sgqlc.types.Field(Confidence, graphql_name='confidence')
    files = sgqlc.types.Field(sgqlc.types.list_of(S3ObjectInput), graphql_name='files')
    file_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fileLinks')


class UpdateTTPInput(sgqlc.types.Input):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'asset_id', 'executed_on', 'technique', 'url', 'evidence', 'files', 'file_links')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_run_id = sgqlc.types.Field(ID, graphql_name='assessmentRunId')
    asset_id = sgqlc.types.Field(ID, graphql_name='assetId')
    executed_on = sgqlc.types.Field(AWSDateTime, graphql_name='executedOn')
    technique = sgqlc.types.Field(String, graphql_name='technique')
    url = sgqlc.types.Field(String, graphql_name='url')
    evidence = sgqlc.types.Field(String, graphql_name='evidence')
    files = sgqlc.types.Field(sgqlc.types.list_of(S3ObjectInput), graphql_name='files')
    file_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fileLinks')



########################################################################
# Output Objects and Interfaces
########################################################################
class Assessment(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'type', 'name', 'externally_assess_cloud_assets', 'phishing_configuration', 'report_recipients', 'schedule', 'assets', 'asset_groups', 'runs', 'client', 'cloud_credentials')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    type = sgqlc.types.Field(sgqlc.types.non_null(AssessmentType), graphql_name='type')
    name = sgqlc.types.Field(String, graphql_name='name')
    externally_assess_cloud_assets = sgqlc.types.Field(Boolean, graphql_name='externallyAssessCloudAssets')
    phishing_configuration = sgqlc.types.Field('PhishingConfiguration', graphql_name='phishingConfiguration')
    report_recipients = sgqlc.types.Field(sgqlc.types.list_of(AWSEmail), graphql_name='reportRecipients')
    schedule = sgqlc.types.Field('Schedule', graphql_name='schedule')
    assets = sgqlc.types.Field('ModelAssessmentAssetConnectionConnection', graphql_name='assets', args=sgqlc.types.ArgDict((
        ('asset_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='assetId', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentAssetConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    asset_groups = sgqlc.types.Field('ModelAssessmentAssetGroupConnectionConnection', graphql_name='assetGroups', args=sgqlc.types.ArgDict((
        ('asset_group_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='assetGroupId', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentAssetGroupConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    runs = sgqlc.types.Field('ModelAssessmentRunConnection', graphql_name='runs', args=sgqlc.types.ArgDict((
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentRunFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    client = sgqlc.types.Field(sgqlc.types.non_null('Client'), graphql_name='client')
    cloud_credentials = sgqlc.types.Field('ModelCloudCredentialConnection', graphql_name='cloudCredentials', args=sgqlc.types.ArgDict((
        ('access_key', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='accessKey', default=None)),
        ('filter', sgqlc.types.Arg(ModelCloudCredentialFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )


class AssessmentAssetConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'assessment_id', 'assessment', 'asset')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    assessment = sgqlc.types.Field(Assessment, graphql_name='assessment')
    asset = sgqlc.types.Field('Asset', graphql_name='asset')


class AssessmentAssetGroupConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_group_id', 'assessment_id', 'assessment', 'asset_group')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    asset_group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetGroupId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    assessment = sgqlc.types.Field(Assessment, graphql_name='assessment')
    asset_group = sgqlc.types.Field('AssetGroup', graphql_name='assetGroup')


class AssessmentRun(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'assessment_id', 'state', 'phishing_results', 'stager', 'metadata', 'fail_reason', 'recon', 'last_run_id', 'assessment', 'last_run', 'write_key', 'score', 'execution_arn', 'discovered_assets', 'credentials', 'connections', 'client', 'findings', 'leads', 'ttps')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    state = sgqlc.types.Field(AssessmentState, graphql_name='state', args=sgqlc.types.ArgDict((
        ('state', sgqlc.types.Arg(AssessmentState, graphql_name='state', default=None)),
))
    )
    phishing_results = sgqlc.types.Field(sgqlc.types.list_of('PhishingResult'), graphql_name='phishingResults')
    stager = sgqlc.types.Field(String, graphql_name='stager')
    metadata = sgqlc.types.Field('AssessmentRunMetadata', graphql_name='metadata')
    fail_reason = sgqlc.types.Field(String, graphql_name='failReason')
    recon = sgqlc.types.Field(AWSJSON, graphql_name='recon')
    last_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='lastRunId')
    assessment = sgqlc.types.Field(Assessment, graphql_name='assessment')
    last_run = sgqlc.types.Field('AssessmentRun', graphql_name='lastRun')
    write_key = sgqlc.types.Field(String, graphql_name='writeKey')
    score = sgqlc.types.Field(Float, graphql_name='score')
    execution_arn = sgqlc.types.Field(String, graphql_name='executionArn')
    discovered_assets = sgqlc.types.Field('ModelAssessmentRunAssetConnectionConnection', graphql_name='discoveredAssets', args=sgqlc.types.ArgDict((
        ('asset_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='assetId', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentRunAssetConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    credentials = sgqlc.types.Field('ModelAssessmentRunCredentialConnectionConnection', graphql_name='credentials', args=sgqlc.types.ArgDict((
        ('credential_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='credentialId', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentRunCredentialConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    connections = sgqlc.types.Field('ModelAssetConnectionConnection', graphql_name='connections', args=sgqlc.types.ArgDict((
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    client = sgqlc.types.Field(sgqlc.types.non_null('Client'), graphql_name='client')
    findings = sgqlc.types.Field('ModelFindingConnection', graphql_name='findings', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelFindingFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    leads = sgqlc.types.Field('ModelLeadConnection', graphql_name='leads', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelLeadFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    ttps = sgqlc.types.Field('ModelTTPConnection', graphql_name='ttps', args=sgqlc.types.ArgDict((
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('filter', sgqlc.types.Arg(ModelTTPFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )


class AssessmentRunAssetConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'assessment_id', 'assessment', 'asset')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    assessment = sgqlc.types.Field(AssessmentRun, graphql_name='assessment')
    asset = sgqlc.types.Field('Asset', graphql_name='asset')


class AssessmentRunCredentialConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'assessment_id', 'credential_id', 'link_type', 'assessment', 'asset', 'credential')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    credential_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='credentialId')
    link_type = sgqlc.types.Field(CredentialLinkType, graphql_name='linkType', args=sgqlc.types.ArgDict((
        ('link_type', sgqlc.types.Arg(CredentialLinkType, graphql_name='linkType', default=None)),
))
    )
    assessment = sgqlc.types.Field(AssessmentRun, graphql_name='assessment')
    asset = sgqlc.types.Field('Asset', graphql_name='asset')
    credential = sgqlc.types.Field('Credential', graphql_name='credential')


class AssessmentRunMetadata(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('emails_processed', 'findings_created', 'external_assets_processed', 'cloud_accounts_processed', 'seeds_monitored', 'internal_assessments_executed')
    emails_processed = sgqlc.types.Field(Int, graphql_name='emailsProcessed')
    findings_created = sgqlc.types.Field(Int, graphql_name='findingsCreated')
    external_assets_processed = sgqlc.types.Field(Int, graphql_name='externalAssetsProcessed')
    cloud_accounts_processed = sgqlc.types.Field(Int, graphql_name='cloudAccountsProcessed')
    seeds_monitored = sgqlc.types.Field(Int, graphql_name='seedsMonitored')
    internal_assessments_executed = sgqlc.types.Field(Int, graphql_name='internalAssessmentsExecuted')


class Asset(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_type', 'asset_identifier', 'asset_source', 'tags', 'criticality', 'assessments', 'connections', 'asset_groups', 'client', 'credentials', 'findings')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    asset_type = sgqlc.types.Field(sgqlc.types.non_null(AssetType), graphql_name='assetType')
    asset_identifier = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='assetIdentifier')
    asset_source = sgqlc.types.Field(sgqlc.types.non_null(AssetSource), graphql_name='assetSource', args=sgqlc.types.ArgDict((
        ('asset_source', sgqlc.types.Arg(AssetSource, graphql_name='assetSource', default=None)),
))
    )
    tags = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(String)), graphql_name='tags')
    criticality = sgqlc.types.Field(Int, graphql_name='criticality')
    assessments = sgqlc.types.Field('ModelAssessmentAssetConnectionConnection', graphql_name='assessments', args=sgqlc.types.ArgDict((
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentAssetConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    connections = sgqlc.types.Field('ModelAssetConnectionConnection', graphql_name='connections', args=sgqlc.types.ArgDict((
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    asset_groups = sgqlc.types.Field('ModelAssetGroupConnectionConnection', graphql_name='assetGroups', args=sgqlc.types.ArgDict((
        ('group_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='groupID', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetGroupConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    client = sgqlc.types.Field(sgqlc.types.non_null('Client'), graphql_name='client')
    credentials = sgqlc.types.Field('ModelCredentialConnectionConnection', graphql_name='credentials', args=sgqlc.types.ArgDict((
        ('credential_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='credentialId', default=None)),
        ('filter', sgqlc.types.Arg(ModelCredentialConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    findings = sgqlc.types.Field('ModelFindingConnection', graphql_name='findings', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelFindingFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )


class AssetConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'discovery_method', 'state', 'assessment_run_id', 'asset_source_id', 'asset_destination_id', 'assessment', 'asset_source', 'asset_destination')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    discovery_method = sgqlc.types.Field(sgqlc.types.non_null(DiscoveryMethod), graphql_name='discoveryMethod', args=sgqlc.types.ArgDict((
        ('discovery_method', sgqlc.types.Arg(DiscoveryMethod, graphql_name='discoveryMethod', default=None)),
))
    )
    state = sgqlc.types.Field(sgqlc.types.non_null(AssetConnectionState), graphql_name='state', args=sgqlc.types.ArgDict((
        ('state', sgqlc.types.Arg(AssetConnectionState, graphql_name='state', default=None)),
))
    )
    assessment_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentRunId')
    asset_source_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetSourceId')
    asset_destination_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetDestinationId')
    assessment = sgqlc.types.Field(AssessmentRun, graphql_name='assessment')
    asset_source = sgqlc.types.Field(Asset, graphql_name='assetSource')
    asset_destination = sgqlc.types.Field(Asset, graphql_name='assetDestination')


class AssetGroup(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'name', 'created_at', 'updated_at', 'assessments', 'assets', 'client')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    assessments = sgqlc.types.Field('ModelAssessmentAssetGroupConnectionConnection', graphql_name='assessments', args=sgqlc.types.ArgDict((
        ('assessment_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='assessmentId', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentAssetGroupConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    assets = sgqlc.types.Field('ModelAssetGroupConnectionConnection', graphql_name='assets', args=sgqlc.types.ArgDict((
        ('asset_id', sgqlc.types.Arg(ModelIDKeyConditionInput, graphql_name='assetID', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetGroupConnectionFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    client = sgqlc.types.Field(sgqlc.types.non_null('Client'), graphql_name='client')


class AssetGroupConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'asset_id', 'group_id', 'created_at', 'updated_at', 'asset', 'group')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetID')
    group_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='groupID')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    asset = sgqlc.types.Field(Asset, graphql_name='asset')
    group = sgqlc.types.Field(AssetGroup, graphql_name='group')


class Client(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'verified', 'invoices', 'stripe_customer_id', 'stripe_customer', 'stripe_subscription_status', 'upcoming_invoice', 'users', 'assessments', 'runs', 'assets', 'asset_groups', 'name', 'stripe_subscription_id', 'stripe_subscription_items', 'stripe_latest_invoice_status', 'configurations', 'credentials')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    verified = sgqlc.types.Field(Boolean, graphql_name='verified')
    invoices = sgqlc.types.Field(AWSJSON, graphql_name='invoices')
    stripe_customer_id = sgqlc.types.Field(String, graphql_name='stripeCustomerId')
    stripe_customer = sgqlc.types.Field(AWSJSON, graphql_name='stripeCustomer')
    stripe_subscription_status = sgqlc.types.Field(String, graphql_name='stripeSubscriptionStatus')
    upcoming_invoice = sgqlc.types.Field(AWSJSON, graphql_name='upcomingInvoice')
    users = sgqlc.types.Field(AWSJSON, graphql_name='users')
    assessments = sgqlc.types.Field('ModelAssessmentConnection', graphql_name='assessments', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssessmentFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    runs = sgqlc.types.Field('ModelAssessmentRunConnection', graphql_name='runs', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssessmentRunFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    assets = sgqlc.types.Field('ModelAssetConnection', graphql_name='assets', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssetFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    asset_groups = sgqlc.types.Field('ModelAssetGroupConnection', graphql_name='assetGroups', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssetGroupFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    stripe_subscription_id = sgqlc.types.Field(String, graphql_name='stripeSubscriptionId')
    stripe_subscription_items = sgqlc.types.Field(sgqlc.types.list_of('StripeSubscriptionItem'), graphql_name='stripeSubscriptionItems')
    stripe_latest_invoice_status = sgqlc.types.Field(String, graphql_name='stripeLatestInvoiceStatus')
    configurations = sgqlc.types.Field('ModelClientConfigurationConnection', graphql_name='configurations', args=sgqlc.types.ArgDict((
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('filter', sgqlc.types.Arg(ModelClientConfigurationFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    credentials = sgqlc.types.Field('ModelCredentialConnection', graphql_name='credentials', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelCredentialFilterInput, graphql_name='filter', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )


class ClientConfiguration(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'client_id', 'name', 'slack_configuration', 'splunk_configuration', 'jira_configuration', 'email_configuration', 'client')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='clientId')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')
    slack_configuration = sgqlc.types.Field('SlackConfiguration', graphql_name='slackConfiguration')
    splunk_configuration = sgqlc.types.Field('SplunkConfiguration', graphql_name='splunkConfiguration')
    jira_configuration = sgqlc.types.Field('JiraConfiguration', graphql_name='jiraConfiguration')
    email_configuration = sgqlc.types.Field('EmailConfiguration', graphql_name='emailConfiguration')
    client = sgqlc.types.Field(Client, graphql_name='client')


class CloudCredential(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'client_id', 'created_at', 'updated_at', 'name', 'access_key', 'cloud_platform', 'client', 'secret_key', 'session_token', 'additional_data')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    client_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='clientId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    name = sgqlc.types.Field(String, graphql_name='name')
    access_key = sgqlc.types.Field(String, graphql_name='accessKey')
    cloud_platform = sgqlc.types.Field(CloudPlatform, graphql_name='cloudPlatform', args=sgqlc.types.ArgDict((
        ('cloud_platform', sgqlc.types.Arg(CloudPlatform, graphql_name='cloudPlatform', default=None)),
))
    )
    client = sgqlc.types.Field(Client, graphql_name='client')
    secret_key = sgqlc.types.Field(String, graphql_name='secretKey')
    session_token = sgqlc.types.Field(String, graphql_name='sessionToken')
    additional_data = sgqlc.types.Field(AWSJSON, graphql_name='additionalData')


class Credential(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'name', 'username', 'password', 'hashes', 'domain', 'client')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    name = sgqlc.types.Field(String, graphql_name='name')
    username = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='username')
    password = sgqlc.types.Field(String, graphql_name='password')
    hashes = sgqlc.types.Field(sgqlc.types.list_of('HashPair'), graphql_name='hashes')
    domain = sgqlc.types.Field(String, graphql_name='domain')
    client = sgqlc.types.Field(sgqlc.types.non_null(Client), graphql_name='client')


class CredentialConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'created_at', 'updated_at', 'asset_id', 'credential_id', 'asset', 'credential')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    credential_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='credentialId')
    asset = sgqlc.types.Field(Asset, graphql_name='asset')
    credential = sgqlc.types.Field(Credential, graphql_name='credential')


class EmailConfiguration(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('enabled', 'enabled_events', 'emails')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')
    emails = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(AWSEmail))), graphql_name='emails')


class Finding(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_id', 'affected_asset_id', 'created_at', 'updated_at', 'severity', 'title', 'description', 'evidence', 'references', 'recommendations', 'risk', 'files', 'file_links', 'assessment', 'affected_asset')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentId')
    affected_asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='affectedAssetId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    severity = sgqlc.types.Field(sgqlc.types.non_null(Severity), graphql_name='severity')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    evidence = sgqlc.types.Field(AWSJSON, graphql_name='evidence')
    references = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='references')
    recommendations = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='recommendations')
    risk = sgqlc.types.Field(Float, graphql_name='risk')
    files = sgqlc.types.Field(sgqlc.types.list_of('S3Object'), graphql_name='files')
    file_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fileLinks')
    assessment = sgqlc.types.Field(AssessmentRun, graphql_name='assessment')
    affected_asset = sgqlc.types.Field(Asset, graphql_name='affectedAsset')


class HashPair(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('hash_type', 'hash')
    hash_type = sgqlc.types.Field(sgqlc.types.non_null(HashType), graphql_name='hashType')
    hash = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='hash')


class JiraConfiguration(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('enabled', 'base_url', 'username', 'secret', 'enabled_events')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    base_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='baseUrl')
    username = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='username')
    secret = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='secret')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')


class Lead(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'created_at', 'updated_at', 'title', 'description', 'evidence', 'references', 'confidence', 'files', 'file_links', 'assessment')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentRunId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    description = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='description')
    evidence = sgqlc.types.Field(AWSJSON, graphql_name='evidence')
    references = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='references')
    confidence = sgqlc.types.Field(Confidence, graphql_name='confidence')
    files = sgqlc.types.Field(sgqlc.types.list_of('S3Object'), graphql_name='files')
    file_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fileLinks')
    assessment = sgqlc.types.Field(AssessmentRun, graphql_name='assessment')


class ModelAssessmentAssetConnectionConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssessmentAssetConnection), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssessmentAssetGroupConnectionConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssessmentAssetGroupConnection), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssessmentConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(Assessment), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssessmentRunAssetConnectionConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssessmentRunAssetConnection), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssessmentRunConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssessmentRun), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssessmentRunCredentialConnectionConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssessmentRunCredentialConnection), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssetConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(Asset), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssetConnectionConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssetConnection), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssetGroupConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssetGroup), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelAssetGroupConnectionConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssetGroupConnection), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelClientConfigurationConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(ClientConfiguration), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelClientConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(Client), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelCloudCredentialConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(CloudCredential), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelCredentialConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(Credential), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelCredentialConnectionConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(CredentialConnection), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelFindingConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(Finding), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelLeadConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of(Lead), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class ModelTTPConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token')
    items = sgqlc.types.Field(sgqlc.types.list_of('TTP'), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')


class Mutation(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('start_assessment', 'stop_assessment', 'generate_run_report', 'create_subscription', 'update_payment_method', 'invite_user', 'send_test_phish', 'zip_assessment_run', 'batch_create_assets', 'batch_create_findings', 'batch_create_asset_connections', 'batch_create_credentials', 'batch_link_credentials', 'schedule_assessment', 'unschedule_assessment', 'batch_create_ttps', 'batch_create_leads', 'delete_assessment_asset_connection', 'create_assessment_asset_group_connection', 'update_assessment_asset_group_connection', 'delete_assessment_asset_group_connection', 'delete_assessment_run', 'delete_assessment_run_asset_connection', 'delete_assessment_run_credential_connection', 'delete_asset_connection', 'update_asset', 'delete_asset', 'create_asset_group_connection', 'update_asset_group_connection', 'delete_asset_group_connection', 'delete_asset_group', 'delete_client', 'create_client_configuration', 'update_client_configuration', 'delete_client_configuration', 'delete_cloud_credential', 'delete_credential', 'delete_credential_connection', 'delete_finding', 'delete_lead', 'delete_ttp', 'create_assessment', 'update_assessment', 'delete_assessment', 'create_assessment_asset_connection', 'update_assessment_asset_connection', 'create_assessment_run', 'update_assessment_run', 'create_assessment_run_asset_connection', 'update_assessment_run_asset_connection', 'create_assessment_run_credential_connection', 'update_assessment_run_credential_connection', 'create_asset_connection', 'update_asset_connection', 'create_asset', 'create_asset_group', 'update_asset_group', 'create_client', 'update_client', 'create_cloud_credential', 'update_cloud_credential', 'create_credential', 'update_credential', 'create_credential_connection', 'update_credential_connection', 'create_finding', 'update_finding', 'create_lead', 'update_lead', 'create_ttp', 'update_ttp')
    start_assessment = sgqlc.types.Field(AWSJSON, graphql_name='startAssessment', args=sgqlc.types.ArgDict((
        ('assessment_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentId', default=None)),
        ('client_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='clientId', default=None)),
))
    )
    stop_assessment = sgqlc.types.Field(String, graphql_name='stopAssessment', args=sgqlc.types.ArgDict((
        ('assessment_run_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentRunId', default=None)),
))
    )
    generate_run_report = sgqlc.types.Field(AWSJSON, graphql_name='generateRunReport', args=sgqlc.types.ArgDict((
        ('assessment_run_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentRunId', default=None)),
        ('client_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='clientId', default=None)),
))
    )
    create_subscription = sgqlc.types.Field(String, graphql_name='createSubscription', args=sgqlc.types.ArgDict((
        ('client_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='clientId', default=None)),
        ('payment_method_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='paymentMethodId', default=None)),
))
    )
    update_payment_method = sgqlc.types.Field(String, graphql_name='updatePaymentMethod', args=sgqlc.types.ArgDict((
        ('client_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='clientId', default=None)),
        ('payment_method_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='paymentMethodId', default=None)),
))
    )
    invite_user = sgqlc.types.Field(String, graphql_name='inviteUser', args=sgqlc.types.ArgDict((
        ('client_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='clientId', default=None)),
        ('emails', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(String)), graphql_name='emails', default=None)),
))
    )
    send_test_phish = sgqlc.types.Field(String, graphql_name='sendTestPhish', args=sgqlc.types.ArgDict((
        ('assessment_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='assessmentId', default=None)),
))
    )
    zip_assessment_run = sgqlc.types.Field(AWSJSON, graphql_name='zipAssessmentRun', args=sgqlc.types.ArgDict((
        ('assessment_run_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentRunId', default=None)),
))
    )
    batch_create_assets = sgqlc.types.Field(sgqlc.types.list_of(AssessmentRunAssetConnection), graphql_name='batchCreateAssets', args=sgqlc.types.ArgDict((
        ('assessment_run_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentRunId', default=None)),
        ('assets', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CreateAssessmentRunAssetInput))), graphql_name='assets', default=None)),
))
    )
    batch_create_findings = sgqlc.types.Field(sgqlc.types.list_of(Finding), graphql_name='batchCreateFindings', args=sgqlc.types.ArgDict((
        ('assessment_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentId', default=None)),
        ('findings', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CreateFindingInput))), graphql_name='findings', default=None)),
))
    )
    batch_create_asset_connections = sgqlc.types.Field(sgqlc.types.list_of(AssetConnection), graphql_name='batchCreateAssetConnections', args=sgqlc.types.ArgDict((
        ('assessment_run_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentRunId', default=None)),
        ('connections', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CreateAssetConnectionInput))), graphql_name='connections', default=None)),
))
    )
    batch_create_credentials = sgqlc.types.Field(sgqlc.types.list_of(AssessmentRunCredentialConnection), graphql_name='batchCreateCredentials', args=sgqlc.types.ArgDict((
        ('credentials', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CreateAssessmentRunCredentialInput))), graphql_name='credentials', default=None)),
))
    )
    batch_link_credentials = sgqlc.types.Field(sgqlc.types.list_of(AssessmentRunCredentialConnection), graphql_name='batchLinkCredentials', args=sgqlc.types.ArgDict((
        ('credentials', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CreateAssessmentRunCredentialConnectionInput))), graphql_name='credentials', default=None)),
))
    )
    schedule_assessment = sgqlc.types.Field(String, graphql_name='scheduleAssessment', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(ScheduleInput), graphql_name='input', default=None)),
))
    )
    unschedule_assessment = sgqlc.types.Field(String, graphql_name='unscheduleAssessment', args=sgqlc.types.ArgDict((
        ('assessment_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='assessmentId', default=None)),
))
    )
    batch_create_ttps = sgqlc.types.Field(sgqlc.types.list_of('TTP'), graphql_name='batchCreateTTPs', args=sgqlc.types.ArgDict((
        ('ttps', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CreateTTPInput))), graphql_name='ttps', default=None)),
))
    )
    batch_create_leads = sgqlc.types.Field(sgqlc.types.list_of(Lead), graphql_name='batchCreateLeads', args=sgqlc.types.ArgDict((
        ('leads', sgqlc.types.Arg(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CreateLeadInput))), graphql_name='leads', default=None)),
))
    )
    delete_assessment_asset_connection = sgqlc.types.Field(AssessmentAssetConnection, graphql_name='deleteAssessmentAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssessmentAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    create_assessment_asset_group_connection = sgqlc.types.Field(AssessmentAssetGroupConnection, graphql_name='createAssessmentAssetGroupConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssessmentAssetGroupConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentAssetGroupConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_assessment_asset_group_connection = sgqlc.types.Field(AssessmentAssetGroupConnection, graphql_name='updateAssessmentAssetGroupConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssessmentAssetGroupConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentAssetGroupConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_assessment_asset_group_connection = sgqlc.types.Field(AssessmentAssetGroupConnection, graphql_name='deleteAssessmentAssetGroupConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssessmentAssetGroupConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentAssetGroupConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_assessment_run = sgqlc.types.Field(AssessmentRun, graphql_name='deleteAssessmentRun', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssessmentRunInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_assessment_run_asset_connection = sgqlc.types.Field(AssessmentRunAssetConnection, graphql_name='deleteAssessmentRunAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssessmentRunAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_assessment_run_credential_connection = sgqlc.types.Field(AssessmentRunCredentialConnection, graphql_name='deleteAssessmentRunCredentialConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssessmentRunCredentialConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunCredentialConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_asset_connection = sgqlc.types.Field(AssetConnection, graphql_name='deleteAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_asset = sgqlc.types.Field(Asset, graphql_name='updateAsset', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssetInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_asset = sgqlc.types.Field(Asset, graphql_name='deleteAsset', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssetInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetConditionInput, graphql_name='condition', default=None)),
))
    )
    create_asset_group_connection = sgqlc.types.Field(AssetGroupConnection, graphql_name='createAssetGroupConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssetGroupConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetGroupConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_asset_group_connection = sgqlc.types.Field(AssetGroupConnection, graphql_name='updateAssetGroupConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssetGroupConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetGroupConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_asset_group_connection = sgqlc.types.Field(AssetGroupConnection, graphql_name='deleteAssetGroupConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssetGroupConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetGroupConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_asset_group = sgqlc.types.Field(AssetGroup, graphql_name='deleteAssetGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssetGroupInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetGroupConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_client = sgqlc.types.Field(Client, graphql_name='deleteClient', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteClientInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelClientConditionInput, graphql_name='condition', default=None)),
))
    )
    create_client_configuration = sgqlc.types.Field(ClientConfiguration, graphql_name='createClientConfiguration', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateClientConfigurationInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelClientConfigurationConditionInput, graphql_name='condition', default=None)),
))
    )
    update_client_configuration = sgqlc.types.Field(ClientConfiguration, graphql_name='updateClientConfiguration', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateClientConfigurationInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelClientConfigurationConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_client_configuration = sgqlc.types.Field(ClientConfiguration, graphql_name='deleteClientConfiguration', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteClientConfigurationInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelClientConfigurationConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_cloud_credential = sgqlc.types.Field(CloudCredential, graphql_name='deleteCloudCredential', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCloudCredentialInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCloudCredentialConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_credential = sgqlc.types.Field(Credential, graphql_name='deleteCredential', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCredentialInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCredentialConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_credential_connection = sgqlc.types.Field(CredentialConnection, graphql_name='deleteCredentialConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteCredentialConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCredentialConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_finding = sgqlc.types.Field(Finding, graphql_name='deleteFinding', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteFindingInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelFindingConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_lead = sgqlc.types.Field(Lead, graphql_name='deleteLead', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteLeadInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelLeadConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_ttp = sgqlc.types.Field('TTP', graphql_name='deleteTTP', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteTTPInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelTTPConditionInput, graphql_name='condition', default=None)),
))
    )
    create_assessment = sgqlc.types.Field(Assessment, graphql_name='createAssessment', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssessmentInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentConditionInput, graphql_name='condition', default=None)),
))
    )
    update_assessment = sgqlc.types.Field(Assessment, graphql_name='updateAssessment', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssessmentInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentConditionInput, graphql_name='condition', default=None)),
))
    )
    delete_assessment = sgqlc.types.Field(Assessment, graphql_name='deleteAssessment', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(DeleteAssessmentInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentConditionInput, graphql_name='condition', default=None)),
))
    )
    create_assessment_asset_connection = sgqlc.types.Field(AssessmentAssetConnection, graphql_name='createAssessmentAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssessmentAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_assessment_asset_connection = sgqlc.types.Field(AssessmentAssetConnection, graphql_name='updateAssessmentAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssessmentAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    create_assessment_run = sgqlc.types.Field(AssessmentRun, graphql_name='createAssessmentRun', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssessmentRunInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunConditionInput, graphql_name='condition', default=None)),
))
    )
    update_assessment_run = sgqlc.types.Field(AssessmentRun, graphql_name='updateAssessmentRun', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssessmentRunInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunConditionInput, graphql_name='condition', default=None)),
))
    )
    create_assessment_run_asset_connection = sgqlc.types.Field(AssessmentRunAssetConnection, graphql_name='createAssessmentRunAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssessmentRunAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_assessment_run_asset_connection = sgqlc.types.Field(AssessmentRunAssetConnection, graphql_name='updateAssessmentRunAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssessmentRunAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    create_assessment_run_credential_connection = sgqlc.types.Field(AssessmentRunCredentialConnection, graphql_name='createAssessmentRunCredentialConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssessmentRunCredentialConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunCredentialConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_assessment_run_credential_connection = sgqlc.types.Field(AssessmentRunCredentialConnection, graphql_name='updateAssessmentRunCredentialConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssessmentRunCredentialConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssessmentRunCredentialConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    create_asset_connection = sgqlc.types.Field(AssetConnection, graphql_name='createAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_asset_connection = sgqlc.types.Field(AssetConnection, graphql_name='updateAssetConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssetConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    create_asset = sgqlc.types.Field(Asset, graphql_name='createAsset', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssetInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetConditionInput, graphql_name='condition', default=None)),
))
    )
    create_asset_group = sgqlc.types.Field(AssetGroup, graphql_name='createAssetGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateAssetGroupInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetGroupConditionInput, graphql_name='condition', default=None)),
))
    )
    update_asset_group = sgqlc.types.Field(AssetGroup, graphql_name='updateAssetGroup', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateAssetGroupInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelAssetGroupConditionInput, graphql_name='condition', default=None)),
))
    )
    create_client = sgqlc.types.Field(Client, graphql_name='createClient', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateClientInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelClientConditionInput, graphql_name='condition', default=None)),
))
    )
    update_client = sgqlc.types.Field(Client, graphql_name='updateClient', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateClientInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelClientConditionInput, graphql_name='condition', default=None)),
))
    )
    create_cloud_credential = sgqlc.types.Field(CloudCredential, graphql_name='createCloudCredential', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCloudCredentialInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCloudCredentialConditionInput, graphql_name='condition', default=None)),
))
    )
    update_cloud_credential = sgqlc.types.Field(CloudCredential, graphql_name='updateCloudCredential', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateCloudCredentialInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCloudCredentialConditionInput, graphql_name='condition', default=None)),
))
    )
    create_credential = sgqlc.types.Field(Credential, graphql_name='createCredential', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCredentialInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCredentialConditionInput, graphql_name='condition', default=None)),
))
    )
    update_credential = sgqlc.types.Field(Credential, graphql_name='updateCredential', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateCredentialInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCredentialConditionInput, graphql_name='condition', default=None)),
))
    )
    create_credential_connection = sgqlc.types.Field(CredentialConnection, graphql_name='createCredentialConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateCredentialConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCredentialConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    update_credential_connection = sgqlc.types.Field(CredentialConnection, graphql_name='updateCredentialConnection', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateCredentialConnectionInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelCredentialConnectionConditionInput, graphql_name='condition', default=None)),
))
    )
    create_finding = sgqlc.types.Field(Finding, graphql_name='createFinding', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateFindingInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelFindingConditionInput, graphql_name='condition', default=None)),
))
    )
    update_finding = sgqlc.types.Field(Finding, graphql_name='updateFinding', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateFindingInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelFindingConditionInput, graphql_name='condition', default=None)),
))
    )
    create_lead = sgqlc.types.Field(Lead, graphql_name='createLead', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateLeadInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelLeadConditionInput, graphql_name='condition', default=None)),
))
    )
    update_lead = sgqlc.types.Field(Lead, graphql_name='updateLead', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateLeadInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelLeadConditionInput, graphql_name='condition', default=None)),
))
    )
    create_ttp = sgqlc.types.Field('TTP', graphql_name='createTTP', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(CreateTTPInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelTTPConditionInput, graphql_name='condition', default=None)),
))
    )
    update_ttp = sgqlc.types.Field('TTP', graphql_name='updateTTP', args=sgqlc.types.ArgDict((
        ('input', sgqlc.types.Arg(sgqlc.types.non_null(UpdateTTPInput), graphql_name='input', default=None)),
        ('condition', sgqlc.types.Arg(ModelTTPConditionInput, graphql_name='condition', default=None)),
))
    )


class PhishingConfiguration(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('template', 'subject', 'landing_page', 'send_from', 'redirect_url', 'hours')
    template = sgqlc.types.Field(String, graphql_name='template')
    subject = sgqlc.types.Field(String, graphql_name='subject')
    landing_page = sgqlc.types.Field(String, graphql_name='landingPage')
    send_from = sgqlc.types.Field(String, graphql_name='sendFrom')
    redirect_url = sgqlc.types.Field(String, graphql_name='redirectUrl')
    hours = sgqlc.types.Field(Int, graphql_name='hours')


class PhishingResult(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('email', 'status', 'ip', 'latitude', 'longitude')
    email = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='email')
    status = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='status')
    ip = sgqlc.types.Field(String, graphql_name='ip')
    latitude = sgqlc.types.Field(Float, graphql_name='latitude')
    longitude = sgqlc.types.Field(Float, graphql_name='longitude')


class Query(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('get_single_invoice', 'scores_by_date', 'findings_by_severity', 'assessment_by_type', 'search_assessments', 'get_assessment', 'list_assessments', 'assessment_run_by_write_key', 'search_assessment_runs', 'get_assessment_run', 'list_assessment_runs', 'list_assets', 'get_asset', 'assets_by_type', 'assets_by_source', 'assets_by_identifier', 'search_assets', 'get_asset_group', 'list_asset_groups', 'asset_groups_by_name', 'search_asset_groups', 'clients_by_name', 'clients_by_subscription', 'clients_by_stripe_customer', 'search_clients', 'get_client', 'list_clients', 'get_cloud_credential', 'list_cloud_credentials', 'list_credentials', 'get_credential', 'search_credentials', 'search_findings', 'search_leads', 'search_ttps')
    get_single_invoice = sgqlc.types.Field(AWSJSON, graphql_name='getSingleInvoice', args=sgqlc.types.ArgDict((
        ('client_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='clientId', default=None)),
        ('invoice_id', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='invoiceId', default=None)),
))
    )
    scores_by_date = sgqlc.types.Field(AWSJSON, graphql_name='scoresByDate', args=sgqlc.types.ArgDict((
        ('client_id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='clientId', default=None)),
        ('interval', sgqlc.types.Arg(sgqlc.types.non_null(DateInterval), graphql_name='interval', default=None)),
))
    )
    findings_by_severity = sgqlc.types.Field(ModelFindingConnection, graphql_name='findingsBySeverity', args=sgqlc.types.ArgDict((
        ('severity', sgqlc.types.Arg(Severity, graphql_name='severity', default=None)),
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelFindingFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    assessment_by_type = sgqlc.types.Field(ModelAssessmentConnection, graphql_name='assessmentByType', args=sgqlc.types.ArgDict((
        ('type', sgqlc.types.Arg(AssessmentType, graphql_name='type', default=None)),
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_assessments = sgqlc.types.Field('SearchableAssessmentConnection', graphql_name='searchAssessments', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableAssessmentFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableAssessmentSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    get_assessment = sgqlc.types.Field(Assessment, graphql_name='getAssessment', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_assessments = sgqlc.types.Field(ModelAssessmentConnection, graphql_name='listAssessments', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssessmentFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    assessment_run_by_write_key = sgqlc.types.Field(ModelAssessmentRunConnection, graphql_name='assessmentRunByWriteKey', args=sgqlc.types.ArgDict((
        ('write_key', sgqlc.types.Arg(String, graphql_name='writeKey', default=None)),
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssessmentRunFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_assessment_runs = sgqlc.types.Field('SearchableAssessmentRunConnection', graphql_name='searchAssessmentRuns', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableAssessmentRunFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableAssessmentRunSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    get_assessment_run = sgqlc.types.Field(AssessmentRun, graphql_name='getAssessmentRun', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_assessment_runs = sgqlc.types.Field(ModelAssessmentRunConnection, graphql_name='listAssessmentRuns', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssessmentRunFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    list_assets = sgqlc.types.Field(ModelAssetConnection, graphql_name='listAssets', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssetFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    get_asset = sgqlc.types.Field(Asset, graphql_name='getAsset', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    assets_by_type = sgqlc.types.Field(ModelAssetConnection, graphql_name='assetsByType', args=sgqlc.types.ArgDict((
        ('asset_type', sgqlc.types.Arg(AssetType, graphql_name='assetType', default=None)),
        ('updated_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='updatedAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    assets_by_source = sgqlc.types.Field(ModelAssetConnection, graphql_name='assetsBySource', args=sgqlc.types.ArgDict((
        ('asset_source', sgqlc.types.Arg(AssetSource, graphql_name='assetSource', default=None)),
        ('updated_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='updatedAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    assets_by_identifier = sgqlc.types.Field(ModelAssetConnection, graphql_name='assetsByIdentifier', args=sgqlc.types.ArgDict((
        ('asset_identifier', sgqlc.types.Arg(String, graphql_name='assetIdentifier', default=None)),
        ('updated_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='updatedAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_assets = sgqlc.types.Field('SearchableAssetConnection', graphql_name='searchAssets', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableAssetFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableAssetSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    get_asset_group = sgqlc.types.Field(AssetGroup, graphql_name='getAssetGroup', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_asset_groups = sgqlc.types.Field(ModelAssetGroupConnection, graphql_name='listAssetGroups', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelAssetGroupFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    asset_groups_by_name = sgqlc.types.Field(ModelAssetGroupConnection, graphql_name='assetGroupsByName', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelAssetGroupFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_asset_groups = sgqlc.types.Field('SearchableAssetGroupConnection', graphql_name='searchAssetGroups', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableAssetGroupFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableAssetGroupSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    clients_by_name = sgqlc.types.Field(ModelClientConnection, graphql_name='clientsByName', args=sgqlc.types.ArgDict((
        ('name', sgqlc.types.Arg(String, graphql_name='name', default=None)),
        ('updated_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='updatedAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelClientFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    clients_by_subscription = sgqlc.types.Field(ModelClientConnection, graphql_name='clientsBySubscription', args=sgqlc.types.ArgDict((
        ('stripe_subscription_id', sgqlc.types.Arg(String, graphql_name='stripeSubscriptionId', default=None)),
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelClientFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    clients_by_stripe_customer = sgqlc.types.Field(ModelClientConnection, graphql_name='clientsByStripeCustomer', args=sgqlc.types.ArgDict((
        ('stripe_customer_id', sgqlc.types.Arg(String, graphql_name='stripeCustomerId', default=None)),
        ('created_at', sgqlc.types.Arg(ModelStringKeyConditionInput, graphql_name='createdAt', default=None)),
        ('sort_direction', sgqlc.types.Arg(ModelSortDirection, graphql_name='sortDirection', default=None)),
        ('filter', sgqlc.types.Arg(ModelClientFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_clients = sgqlc.types.Field('SearchableClientConnection', graphql_name='searchClients', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableClientFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableClientSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    get_client = sgqlc.types.Field(Client, graphql_name='getClient', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_clients = sgqlc.types.Field(ModelClientConnection, graphql_name='listClients', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelClientFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    get_cloud_credential = sgqlc.types.Field(CloudCredential, graphql_name='getCloudCredential', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    list_cloud_credentials = sgqlc.types.Field(ModelCloudCredentialConnection, graphql_name='listCloudCredentials', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelCloudCredentialFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    list_credentials = sgqlc.types.Field(ModelCredentialConnection, graphql_name='listCredentials', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(ModelCredentialFilterInput, graphql_name='filter', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    get_credential = sgqlc.types.Field(Credential, graphql_name='getCredential', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )
    search_credentials = sgqlc.types.Field('SearchableCredentialConnection', graphql_name='searchCredentials', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableCredentialFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableCredentialSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_findings = sgqlc.types.Field('SearchableFindingConnection', graphql_name='searchFindings', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableFindingFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableFindingSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_leads = sgqlc.types.Field('SearchableLeadConnection', graphql_name='searchLeads', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableLeadFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableLeadSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )
    search_ttps = sgqlc.types.Field('SearchableTTPConnection', graphql_name='searchTTPs', args=sgqlc.types.ArgDict((
        ('filter', sgqlc.types.Arg(SearchableTTPFilterInput, graphql_name='filter', default=None)),
        ('sort', sgqlc.types.Arg(SearchableTTPSortInput, graphql_name='sort', default=None)),
        ('limit', sgqlc.types.Arg(Int, graphql_name='limit', default=None)),
        ('next_token', sgqlc.types.Arg(String, graphql_name='nextToken', default=None)),
))
    )


class S3Object(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('bucket', 'key', 'region')
    bucket = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='bucket')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    region = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='region')


class Schedule(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('frequency', 'time_expression', 'arn')
    frequency = sgqlc.types.Field(sgqlc.types.non_null(ScheduleFrequency), graphql_name='frequency', args=sgqlc.types.ArgDict((
        ('frequency', sgqlc.types.Arg(ScheduleFrequency, graphql_name='frequency', default=None)),
))
    )
    time_expression = sgqlc.types.Field(sgqlc.types.non_null('TimeExpression'), graphql_name='timeExpression')
    arn = sgqlc.types.Field(String, graphql_name='arn')


class SearchableAssessmentConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(Assessment), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableAssessmentRunConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssessmentRun), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableAssetConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(Asset), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableAssetGroupConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(AssetGroup), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableClientConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(Client), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableCredentialConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(Credential), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableFindingConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(Finding), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableLeadConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of(Lead), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SearchableTTPConnection(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('items', 'next_token', 'total')
    items = sgqlc.types.Field(sgqlc.types.list_of('TTP'), graphql_name='items')
    next_token = sgqlc.types.Field(String, graphql_name='nextToken')
    total = sgqlc.types.Field(Int, graphql_name='total')


class SlackConfiguration(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('enabled', 'webhook_url', 'enabled_events')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    webhook_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='webhookUrl')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')


class SplunkConfiguration(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('enabled', 'hec_url', 'hec_token', 'enabled_events')
    enabled = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='enabled')
    hec_url = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='hecUrl')
    hec_token = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='hecToken')
    enabled_events = sgqlc.types.Field(sgqlc.types.list_of(AlertEvent), graphql_name='enabledEvents')


class StripeSubscriptionItem(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('subscription_item_id', 'nickname', 'product_id')
    subscription_item_id = sgqlc.types.Field(String, graphql_name='subscriptionItemId')
    nickname = sgqlc.types.Field(String, graphql_name='nickname')
    product_id = sgqlc.types.Field(String, graphql_name='productId')


class Subscription(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('on_update_assessment_run',)
    on_update_assessment_run = sgqlc.types.Field(AssessmentRun, graphql_name='onUpdateAssessmentRun', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(ID), graphql_name='id', default=None)),
))
    )


class TTP(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('id', 'assessment_run_id', 'asset_id', 'created_at', 'updated_at', 'executed_on', 'technique', 'url', 'evidence', 'files', 'file_links', 'assessment_run', 'asset')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    assessment_run_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assessmentRunId')
    asset_id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='assetId')
    created_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='createdAt')
    updated_at = sgqlc.types.Field(sgqlc.types.non_null(AWSDateTime), graphql_name='updatedAt')
    executed_on = sgqlc.types.Field(AWSDateTime, graphql_name='executedOn')
    technique = sgqlc.types.Field(String, graphql_name='technique')
    url = sgqlc.types.Field(String, graphql_name='url')
    evidence = sgqlc.types.Field(String, graphql_name='evidence')
    files = sgqlc.types.Field(sgqlc.types.list_of(S3Object), graphql_name='files')
    file_links = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fileLinks')
    assessment_run = sgqlc.types.Field(AssessmentRun, graphql_name='assessmentRun')
    asset = sgqlc.types.Field(Asset, graphql_name='asset')


class TimeExpression(sgqlc.types.Type):
    __schema__ = schema
    __field_names__ = ('minute', 'hour', 'day_of_month', 'month', 'day_of_week', 'year')
    minute = sgqlc.types.Field(String, graphql_name='minute')
    hour = sgqlc.types.Field(String, graphql_name='hour')
    day_of_month = sgqlc.types.Field(String, graphql_name='dayOfMonth')
    month = sgqlc.types.Field(String, graphql_name='month')
    day_of_week = sgqlc.types.Field(String, graphql_name='dayOfWeek')
    year = sgqlc.types.Field(String, graphql_name='year')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
schema.query_type = Query
schema.mutation_type = Mutation
schema.subscription_type = Subscription

