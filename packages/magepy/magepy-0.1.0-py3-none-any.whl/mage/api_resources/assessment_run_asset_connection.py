from .abstract import *
from .. import schema

class AssessmentRunAssetConnection( MutableAPIResource ):
    """
    Attributes:
        id (str): Unique connection ID
        created_at (str): When the connection was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the connection was last updated (e.g., '2020-01-02T03:04:56.789Z')
        asset_id (str): ID of the associated asset
        assessment_id (str): ID of the associated assessment
    """

    _UPDATE_FN = 'update_assessment_run_asset_connection'
    _DELETE_FN = 'delete_assessment_run_asset_connection'

    __field_names__ = schema.AssessmentRunAssetConnection.__field_names__


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
    def asset(self):
        """
        The associated asset.

        Returns:
            `Asset <asset.Asset>`
        """
        from .asset import Asset
        return self._nested_resource(Asset, 'asset')


    @classmethod
    def create(cls, assessment_run_id, asset_id):
        """
        Connects an asset to an assessment run.

        Args:
            assessment_run_id (str): ID of the assessment run
            asset_id (str): ID of the asset

        Returns:
            `AssessmentRunAssetConnection <assessment_run_asset_connection.AssessmentRunAssetConnection>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentRunAssetConnection.create('11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222')
        """

        retval = cls.mutate('create_assessment_run_asset_connection', input={'asset_id': asset_id, 'assessment_run_id': assessment_run_id})
        if retval:
            retval = cls.init(retval)
        return retval
