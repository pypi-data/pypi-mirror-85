import json
from .abstract import *
from .. import schema

class AssessmentRun(ListableAPIResource, MutableAPIResource, FilterableAPIResource):
    """
    Attributes:
        asm_graph (mage.schema.AWSJSON): A signed URL to the D3 network graph for ATTACK_SURFACE_MONITORING assessments
        assessment_id (str): ID of the associated assessment
        created_at (str): When the assessment run was created (e.g., '2020-01-02T03:04:56.789Z')
        fail_reason (str): The reason for assessment run failure
        id (str): Unique assessment run ID
        last_run_id (str): ID of the assessment run that ran previous to this one for this assessment
        metadata (mage.schema.AssessmentRunMetadata): Statistics for the assessment run
        phishing_results (list of :class:`mage.schema.PhishingResult`):
        recon (mage.schema.AWSJSON): The recon results for this assessment run
        score (float): The assessment run's score
        stager (str): The command to run on an internal computer to begin an internal assessment
        state (mage.schema.AssessmentState): Current state of the assessment run
        updated_at (str): When the assessment run was last updated (e.g., '2020-01-02T03:04:56.789Z')
    """
    _GET_FN = 'get_assessment_run'
    _LIST_FN = 'list_assessment_runs'
    _SEARCH_FN = 'search_assessment_runs'
    _UPDATE_FN = 'update_assessment_run'
    _DELETE_FN = 'delete_assessment_run'

    __field_names__ = [name for name in schema.AssessmentRun.__field_names__ if name not in ['last_run']]


    @property
    def assessment(self):
        """
        The associated assessment.

        Returns:
            `Assessment <assessment.Assessment>`
        """
        from .assessment import Assessment
        return self._nested_resource(Assessment, 'assessment')


    @property
    def connections(self):
        """
        A list of relationships between assets.

        Returns:
            `ListObject` of `AssetConnection <asset_connection.AssetConnection>`
        """
        from .asset_connection import AssetConnection
        return self._nested_resource_list(AssetConnection, 'connections', AssetConnection.__field_names__)


    @property
    def credentials(self):
        """
        The list of credentials associated with this assessment run.

        Returns:
            `ListObject` of `Credential <credential.Credential>`
        """
        from .assessment_run_credential_connection import AssessmentRunCredentialConnection
        return self._nested_resource_list(AssessmentRunCredentialConnection, 'credentials', 'credential')


    @property
    def discovered_assets(self):
        """
        Assets discovered during the assessment run.

        Returns:
            `ListObject` of `AssessmentRunAssetConnection <assessment_run_asset_connection.AssessmentRunAssetConnection>`
        """

        from .assessment_run_asset_connection import AssessmentRunAssetConnection
        return self._nested_resource_list(AssessmentRunAssetConnection, 'discovered_assets', 'asset')

    @class_or_instance_method
    def email_report(cls_or_self, emails = None, assessment_run_id = None):
        """
        Emails the assessment run's report to the provided email addresses.

        Args:
            emails (str or list of str, optional): List of email addresses to send the report to.  Defaults to the associated assessment's `report_recipients`
            assessment_run_id (str, optional): ID of the assessment run to generate the report for

        Examples:
            Class Method:

            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRun.email_report('someone@example.com', '12345')
            >>> mage.AssessmentRun.email_report(['thing1@example.com', 'thing2@example.com'], '12345')

            Instance Method:

            >>> import mage
            >>> mage.connect()
            >>> ar = mage.AssessmentRun.last()[0]
            >>> ar.email_report('someone@example.com')
            >>> ar.email_report(['thing1@example.com', 'thing2@example.com'])
        """

        from mage import client_id

        if not assessment_run_id:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                assessment_run_id = self.id

        if not emails:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                emails = self.assessment.report_recipients
            else:
                cls = cls_or_self
                assessment = cls.eq(id=assessment_run_id).select('report_recipients').limit(1)[0]
                emails = assessment.report_recipients

            if not emails:
                raise ValueError("No valid email addresses are associated with this assessment run.")

        if isinstance(emails, str):
            emails = [emails]
        elif not isinstance(emails, list):
            raise TypeError("'emails' parameter (%s) is neither string nor list." % type(emails).__name__)

        result = cls_or_self.mutate('generate_run_report_async', assessment_run_id=assessment_run_id, client_id=client_id, emails=emails)

        if result:
            result = json.loads(result)
            return result['success'] == True

        return False


    @property
    def findings(self):
        """
        Findings associated with this assessment run.

        Returns:
            `ListObject` of `Finding <finding.Finding>`
        """

        from .finding import Finding
        return self._nested_resource_list(Finding, 'findings')


    @property
    def findings_filter(self):
        """
        Findings associated with this assessment run.

        Returns:
            `Filter`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> ar = mage.AssessmentRun.last()[0]
            >>> list(ar.findings_filter.last(20))
        """

        from .finding import Finding
        return Finding.eq(assessment_id=self.id)


    @property
    def leads(self):
        """
        Leads associated with this assessment run.

        Returns:
            `ListObject` of `Lead <lead.Lead>`
        """

        from .lead import Lead
        return self._nested_resource_list(Lead, 'leads')


    @property
    def leads_filter(self):
        """
        Leads associated with this assessment run.

        Returns:
            `Filter`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> ar = mage.AssessmentRun.last()[0]
            >>> list(ar.leads_filter.select('title').match(title='http').auto_paging_iter())
        """

        from .lead import Lead
        return Lead.eq(assessment_run_id=self.id)


    @property
    def ttps(self):
        """
        TTPs associated with this assessment run.

        Returns:
            `ListObject` of `TTP <ttp.TTP>`
        """
        from .ttp import TTP
        return self._nested_resource_list(TTP, 'ttps')


    @property
    def ttps_filter(self):
        """
        TTPs associated with this assessment run.

        Returns:
            `Filter`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> ar = mage.AssessmentRun.last()[0]
            >>> list(ar.ttps_filter.last(20))
        """

        from .ttp import TTP
        return TTP.eq(assessment_run_id=self.id)


    @property
    def report_url(self):
        """
        The assessment report URL.

        Returns:
            str
        """
        if not hasattr(self, '_report'):
            result = self.get_report_url()
            if result:
                # _report is set this way to avoid the data
                # class from calling update_assessment_run
                object.__setattr__(self, '_report', result)
                return self._report
            else:
                return None

        return self._report


    @class_or_instance_method
    def get_report_url(cls_or_self, assessment_run_id = None):
        """
        Gets the download URL for the assessment run's report.

        Args:
            assessment_run_id (str, optional): ID of the assessment run to get the URL for

        Returns:
            str: URL to the assessment run's report

        Warning:
            This call may time out if it takes too long to generate the report.
            Consider using `email_report` instead.

        Examples:
            Class Method:

            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRun.get_report_url('11111111-1111-1111-1111-111111111111')

            Instance Method:

            >>> import mage
            >>> mage.connect()
            >>> ar = mage.AssessmentRun.last()[0]
            >>> ar.get_report_url()
        """

        from mage import client_id

        if not assessment_run_id:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                assessment_run_id = self.id

        result = cls_or_self.mutate('generate_run_report', assessment_run_id=assessment_run_id, client_id=client_id)

        if result:
            result = json.loads(result)
            return result['url']


    @class_or_instance_method
    def get_zip_url(cls_or_self, assessment_run_id = None):
        """
        Gets the download URL for a zip archive of the run's results.
        """
        from mage import client_id

        if not assessment_run_id:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                assessment_run_id = self.id

        return cls_or_self.mutate('zip_assessment_run', assessment_run_id=assessment_run_id)


    @class_or_instance_method
    def stop(cls_or_self, assessment_run_id = None):
        """
        Stops the assessment if running.

        Args:
            assessment_run_id (str, optional): ID of the assessment run to stop

        Returns:
            bool: True on success, False on error

        Examples:
            Class Method:

            >>> import mage
            >>> mage.connect()
            >>> a = mage.Assessment.eq(name="test")[0]
            >>> run_id = a.start()
            >>> mage.AssessmentRun.stop(run_id)

            Instance Method:

            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRun.last()[0].stop()
        """

        if not assessment_run_id:
            if not isinstance(cls_or_self, type):
                self = cls_or_self
                assessment_run_id = self.id

        result = cls_or_self.mutate('stop_assessment', assessment_run_id=assessment_run_id)
        if result == 'true':
            return True
        else:
            return False
