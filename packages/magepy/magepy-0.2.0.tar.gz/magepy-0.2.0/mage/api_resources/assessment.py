import json
from .abstract import *
from .. import logger
from .. import schema

class Assessment(ListableAPIResource, MutableAPIResource):
    """
    Attributes:
        id (str): Unique assessment ID
        created_at (str): When the assessment was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the assessment was last updated (e.g., '2020-01-02T03:04:56.789Z')
        type (mage.schema.AssessmentType): The assessment's type
        name (str): The assessment's name (e.g., 'My Assessment')
        externally_assess_cloud_assets (bool):
        phishing_configuration (mage.schema.PhishingConfiguration):
        report_recipients (list of :class:`mage.schema.AWSEmail`):
        schedule (mage.schema.Schedule): When and how often this assessment will automatically be run
    """

    _GET_FN = 'get_assessment'
    _LIST_FN = 'list_assessments'
    _SEARCH_FN = 'search_assessments'
    _UPDATE_FN = 'update_assessment'
    _DELETE_FN = 'delete_assessment'

    __field_names__ = schema.Assessment.__field_names__


    def connect(self, item = None, asset_id = None, asset_group_id = None):
        """
        Connect an assessment to an asset or asset group

        Args:
            item (object, optional): Assessment or AssessmentRun or AssetGroup to connect the asset to
            asset_id (str, optional): ID of the asset to connect the assessment to
            asset_group_id (str, optional): ID of the asset group to connect the asset to

        Returns:
            `assessment_asset_connection.AssessmentAssetConnection` or `assessment_asset_group_connection.AssessmentAssetGroupConnection`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> asset = mage.Asset.eq(asset_identifier='www.example.com')[0]
            >>> asset.connect(mage.Assessment.last()[0])
            >>> ar = mage.AssessmentRun.last()[0]
            >>> asset.connect(assessment_run_id=ar.id)
        """

        from .assessment import Assessment
        from .assessment_asset_connection import AssessmentAssetConnection
        from .assessment_run import AssessmentRun
        from .assessment_run_asset_connection import AssessmentRunAssetConnection
        from .asset_group import AssetGroup
        if isinstance(item, Asset) or asset_id:
            if item:
                asset_id = item.id
            retval = self.mutate('create_assessment_asset_connection', input={'assessment_id': self.id, 'asset_id': asset_id})
            if retval:
                retval = AssessmentAssetConnection.init(retval)
            return retval

        if isinstance(item, AssetGroup) or asset_group_id:
            if item:
                asset_group_id = item.id
            retval = self.mutate('create_assessment_asset_group_connection', input={'asset_group_id': asset_group_id, 'assessment_id': self.id})
            if retval:
                retval = AssessmentAssetGroupConnection.init(retval)
            return retval

        raise RuntimeException("%s not supported" % type(item))


    @classmethod
    def create(cls, assessment_type, **kwargs):
        """
        Creates a new assessment of the given type.

        Args:
            assessment_type (mage.schema.AssessmentType): The type of assessment to create.
            **kwargs: Additional arguments to initialize the assessment with.

        Returns:
            mage.api_resources.assessment.Assessment: Created assessment on success or None on failure.

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.create('EXTERNAL')
            >>> mage.Assessment.create('CLOUD', name='My Cloud Test')
        """

        from mage import client_id
        retval = cls.mutate('create_assessment', input={'type': assessment_type, 'assessmentClientId': client_id, **kwargs})
        if retval:
            retval = cls.init(retval)
        return retval


    @class_or_instance_method
    def start(cls_or_self, assessment_id = None):
        """
        Starts the assessment.

        Args:
            assessment_id (str, optional): Assessment ID to start

        Returns:
            str: Assessment run ID

        Examples:
            Class Method:

            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.start('11111111-1111-1111-1111-111111111111')

            Instance Method:

            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> assessment.start()
        """

        from mage import client_id
        if not assessment_id:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                assessment_id = self.id

        result = cls_or_self.mutate('start_assessment', assessment_id=assessment_id, client_id=client_id)
        result = json.loads(result)
        return result['runId']


    @class_or_instance_method
    def create_schedule(cls_or_self, frequency, time_expression, assessment_id = None):
        """
        Schedules the assessment to repeatedly run.

        Args:
            frequency (mage.schema.ScheduleFrequency): How often to run the assessment
            time_expression (dict): When to run the assessment at the given frequency
            assessment_id (str, optional): Assessment ID to schedule

        Returns:
            bool: True on success, False on error

        Examples:

            Class Method:

            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.create_schedule('DAILY', {'hour':'23', 'minute':'55'}, '11111111-1111-1111-1111-111111111111')

            Instance Method:

            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> assessment.create_schedule('DAILY', {'hour':'23', 'minute':'55'})
            >>> assessment.create_schedule('WEEKLY', {'hour':'23', 'minute':'55', 'day_of_week': '1'})
            >>> assessment.create_schedule('MONTHLY', {'hour':'23', 'minute':'55', 'day_of_month': '1'})
            >>> assessment.create_schedule('QUARTERLY', {'hour':'23', 'minute':'55'})
            >>> assessment.create_schedule('YEARLY', {'hour':'23', 'minute':'55', 'day_of_month': '15', 'month': '1'})
        """

        if not assessment_id:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                assessment_id = self.id

        result =  cls_or_self.mutate('schedule_assessment', input={'assessment_id': assessment_id, 'time_expression': time_expression, 'frequency': frequency})
        return result == 'true'


    @class_or_instance_method
    def delete_schedule(cls_or_self, assessment_id=None):
        """
        Stops the assessment from repeatedly running.

        Args:
            assessment_id (str, optional): Assessment ID to unschedule.

        Returns:
            bool: True on success, False on error

        Examples:
            Class Method:

            >>> import mage
            >>> mage.connect()
            >>> mage.Assessment.delete_schedule('11111111-1111-1111-1111-111111111111')

            Instance Method:

            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> assessment.delete_schedule()
        """

        if not assessment_id:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                assessment_id = self.id

        result = cls_or_self.mutate('unschedule_assessment', assessment_id=assessment_id)
        return result == 'true'


    @property
    def runs(self):
        """
        The list of assessment runs associated with this assessment.

        Returns:
            :class:`ListObject <mage.api_resources.abstract.listable_api_resource.ListObject>` of :class:`mage.api_resources.assessment_run.AssessmentRun`
        """
        from .assessment_run import AssessmentRun
        return self._nested_resource_list(AssessmentRun, 'runs')


    @property
    def runs_filter(self):
        """
        The list of assessment runs associated with this assessment.

        Returns:
            mage.api_resources.abstract.filterable_api_resource.Filter: Filter Object

        Example:
            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> lastrun = assessment.runs_filter.last()[0]
        """

        from .assessment_run import AssessmentRun
        return AssessmentRun.eq(assessment_id=self.id)


    @property
    def assets(self):
        """
        The list of assets associated with this assessment.

        Returns:
            mage.api_resources.abstract.listable_api_resource.ListObject: ListObject of :class:`mage.api_resources.asset.Asset` objects

        Example:
            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> for asset in assessment.assets.auto_paging_iter():
            >>>    print(asset.asset.asset_identifier())
        """

        from .assessment_asset_connection import AssessmentAssetConnection
        return self._nested_resource_list(AssessmentAssetConnection, 'assets', AssessmentAssetConnection.__field_names__)


    @property
    def asset_groups(self):
        """
        The list of asset groups associated with this assessment.

        Returns:
            mage.api_resources.abstract.listable_api_resource.ListObject: ListObject of :class:`mage.api_resources.asset_group.AssetGroup` objects
        """

        from .asset_group import AssetGroup
        return self._nested_resource_list(AssetGroup, 'asset_groups', 'asset_group')


    @property
    def asset_groups_filter(self):
        """
        The list of asset groups associated with this assessment.

        Returns:
            mage.api_resources.abstract.filterable_api_resource.Filter: Filter Object

        Example:
            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> for group in assessment.asset_groups_filter.search().auto_paging_iter():
            >>>    print(group.name)
        """

        from .asset_group import AssetGroup
        return AssetGroup.eq(assessment_id=self.id)


    def cloud_credentials(self):
        """
        The list of cloud credentials associated with this assessment.

        Returns:
            mage.api_resources.abstract.listable_api_resource.ListObject: ListObject of :class:`mage.api_resources.cloud_credential.CloudCredential` objects
        """

        from .cloud_credential import CloudCredential
        return self._nested_resource_list(CloudCredential, 'cloud_credentials')


    def cloud_credentials_filter(self):
        """
        The list of cloud credentials associated with this assessment.

        Returns:
            mage.api_resources.abstract.filterable_api_resource.Filter: Filter Object

        Example:
            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> assessment.cloud_credentials_filter
        """

        from .cloud_credential import CloudCredential
        return CloudCredential.eq(assessment_id=self.id)


    def load_assets(self, obj):
        """Loads assets into the assessment.  If an asset already exists (due to another assessment) then the existing asset will be used instead of creating a duplicate one.

        This method supports the following JSON format, where values can be
        either arrays or strings depending on how many values there are:

        {"cidrs":"192.168.1.0/24",
        "ips":["10.10.10.1", "10.10.10.2"],
        "domains": ["www.example.com", "smtp.example.com"],
        "emails": "administrator@example.com",
        "cloud_credentials": []}

        Args:
            obj: dict or file-like object or file name

        Returns:
            None

        Example:
            >>> import mage
            >>> mage.connect()
            >>> assessment = mage.Assessment.eq(name='My Cloud Test')[0]
            >>> assessment.load_assets({'ips': '10.10.10.1'})
            >>> assessment.load_assets("assets.json")
        """

        if isinstance(obj, dict):
            data = obj
        elif hasattr(file_name_or_object, 'read'):
            data = json.loads(f.read())
        else:
            with open(file_name_or_object, 'r') as f:
                data = json.loads(f.read())

        from .cloud_credential import CloudCredential
        from .asset import Asset
        logger.info('[*] Processing input data')
        type_map = {'cidrs': 'CIDR', 'ips': 'IP_ADDRESS', 'domains': 'DOMAIN', 'emails': 'EMAIL'}
        types = {'cidrs':[], 'ips':[], 'domains':[], 'cloud_credentials':[], 'emails':[]}
        for t in types:
            types[t] = data.get(t, [])
            if isinstance(types[t], str):
                types[t] = [types[t]]
            if not isinstance(types[t], list):
                raise ValueError('Unsupported type %s for %s' % (type(types[t]), t))

            logger.info('[*] %i %s' % (len(types[t]), t))

        for t in types:
            logger.info('\n[*] Processing %s' % t)
            if t == 'cloud_credentials':
                for credential in types[t]:
                    logger.info('[*] Adding cloud credential')
                    CloudCredential.create(self.id, credential)
            else:
                # If an asset already exists, add it to the assessment
                # If an asset does not exist, create it and add it to the assessment
                for asset in types[t]:
                    a = Asset.eq(asset_identifier=asset).first()[0]
                    if a:
                        logger.info('[!] Existing asset found, connecting asset ID %s to the assessment' % (a.id))
                    if not a:
                        logger.info('[+] Creating asset (%s) and connecting to assessment' % (asset))
                        a = Asset.create(type_map[t], asset)
                    a.connect(self)

        self.refresh()
