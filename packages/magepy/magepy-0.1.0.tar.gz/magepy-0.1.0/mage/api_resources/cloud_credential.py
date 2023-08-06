from .abstract import *
from .. import schema

class CloudCredential( ListableAPIResource, MutableAPIResource ):
    """
    Attributes:
        id (str): Unique cloud credential ID (e.g., '11111111-1111-1111-1111-111111111111')
        created_at (str): When the cloud credential was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the cloud credential was last updated (e.g., '2020-01-02T03:04:56.789Z')
        assessment_id (str): ID of the associated assessment
        name (str):
        access_key (str):
        cloud_platform (mage.schema.CloudPlatform):
    """

    _GET_FN    = 'get_cloud_credential'
    _LIST_FN   = 'list_cloud_credentials'
    _UPDATE_FN = 'update_cloud_credential'
    _DELETE_FN = 'delete_cloud_credential'

    __field_names__ = schema.CloudCredential.__field_names__


    @property
    def assessment(self):
        """
        The associated assessment.

        Returns:
            `Assessment <assessment.Assessment>`
        """

        from .assessment import Assessment
        return Assessment.get(self.assessment_id)


    @classmethod
    def create(cls, assessment_id, **kwargs):
        """
        Creates a cloud credential associated with an assessment.

        Args:
            assessment_id: ID of the assessment
            **kwargs: Additional arguments to initialize the cloud credential with

        Returns:
            `CloudCredential <cloud_credential.CloudCredential>`

        Todo:
            Create example
        """
        
        from mage import client_id
        retval = cls.mutate('create_cloud_credential', input={'assessment_id': assessment_id, 'client_id': client_id, **kwargs})
        if retval:
            retval = cls.init(retval)
        return retval
