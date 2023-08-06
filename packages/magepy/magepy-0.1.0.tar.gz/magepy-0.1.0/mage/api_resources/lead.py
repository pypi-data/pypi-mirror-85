from .abstract import *
from .. import schema

class Lead( ListableAPIResource, MutableAPIResource ):
    """
    Attributes:
        id (str): Unique lead ID
        assessment_run_id (str): ID of the associated assessment run
        created_at (str): When the lead was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the lead was last updated (e.g., '2020-01-02T03:04:56.789Z')
        title (str): Title of the lead
        description (str): Description of the lead
        evidence (mage.schema.AWSJSON): Evidence supporting the lead
        references (list of str): List of references to additional information
        confidence (mage.schema.Confidence): Confidence level of the lead
        files (list of mage.schema.S3Object): Associated files
        file_links (list of str): Associated files
    """

    _SEARCH_FN = 'search_leads'
    _UPDATE_FN = 'update_lead'
    _DELETE_FN = 'delete_lead'

    __field_names__ = schema.Lead.__field_names__


    @property
    def assessment(self):
        """
        Associated assessment run.

        Returns:
            `AssessmentRun <assessment_run.AssessmentRun>`
        """

        from .assessment_run import AssessmentRun
        return self._nested_resource(AssessmentRun, 'assessment')


    @classmethod
    def create(cls, title, description, assessment_run_id, **kwargs):
        """
        Creates a lead for an assessment run.

        Args:
            title (str):
            description (str):
            assessment_run_id (str):
            **kwargs: Additional arguments to initialize the lead with

        Returns:
            `Lead <lead.Lead>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.Lead.create('Default Password on WEBSRV1', 'Password has not been changed yet.', '11111111-1111-1111-1111-111111111111')
        """
        retval = cls.mutate('create_lead', input={'description': description, 'title': title, 'assessmentRunId': assessment_run_id, **kwargs})
        if retval:
            retval = cls.init(retval)
        return retval
