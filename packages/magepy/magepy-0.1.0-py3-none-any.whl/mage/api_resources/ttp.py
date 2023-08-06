from .abstract import *
from .. import schema

class TTP( ListableAPIResource, MutableAPIResource ):
    """
    Attributes:
        id (str): Unique TTP ID
        created_at (str): When the TTP was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the TTP was last updated (e.g., '2020-01-02T03:04:56.789Z')
        assessment_run_id (str): ID of the associated assessment run
        asset_id (str): ID of the associated asset
        executed_on (mage.schema.AWSDateTime): Time this TTP was executed
        technique (str): Type of technique
        url (str): Technique URL
        evidence (str): Evidence supporting the technique
        files (list of mage.schema.S3Object): Associated files
        file_links (list of str): Associated files
    """

    _SEARCH_FN = 'search_ttps'
    _UPDATE_FN = 'update_ttp'
    _DELETE_FN = 'delete_ttp'

    __field_names__ = schema.TTP.__field_names__


    @property
    def assessment_run(self):
        """
        Associated assessment run.

        Returns:
            `AssessmentRun <assessment_run.AssessmentRun>`
        """

        from .assessment_run import AssessmentRun
        return self._nested_resource(AssessmentRun, 'assessment_run')


    @property
    def asset(self):
        """
        The associated asset.

        Returns:
            `Asset <asset.Asset>`
        """

        from .asset import Asset
        return self._nested_resource(Asset, 'asset')


    @classmethod
    def create(cls, technique, assessment_run_id, asset_id, **params):
        """
        Creates a TTP for an assessment run.

        Args:
            technique (str):
            description (str):
            assessment_run_id (str):
            asset_id (str):
            **kwargs: Additional arguments to initialize the TTP with

        Returns:
            `TTP <ttp.TTP>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.TTP.create('Port scan', '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222')
            >>> mage.TTP.create('Port scan', '11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222', evidence="Scanned all the ports")
        """
        retval = cls.mutate('create_ttp', input={'technique': technique, 'assessment_run_id': assessment_run_id, 'asset_id': asset_id, **params})
        if retval:
            retval = cls.init(retval)
        return retval
