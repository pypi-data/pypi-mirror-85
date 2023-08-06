from .abstract import *
from .. import schema

class AssessmentAssetGroupConnection( MutableAPIResource ):
    """
    Attributes:
        id (str): Unique connection ID (e.g., '11111111-1111-1111-1111-111111111111')
        created_at (str): When the connection was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the connection was last updated (e.g., '2020-01-02T03:04:56.789Z')
        asset_group_id (str): ID of the associated asset group
        assessment_id (str): ID of the associated assessment
    """

    _UPDATE_FN = 'update_assessment_asset_group_connection'
    _DELETE_FN = 'delete_assessment_asset_group_connection'

    __field_names__ = schema.AssessmentAssetGroupConnection.__field_names__

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
    def asset_group(self):
        """
        The associated asset group.

        Returns:
            `AssetGroup <asset_group.AssetGroup>`
        """
        from .asset_group import AssetGroup
        return self._nested_resource(AssetGroup, 'asset_group')


    @classmethod
    def create(cls, assessment_id, group_id):
        """
        Connects an asset group to an assessment.

        Args:
            assessment_id (str): ID of the assessment
            group_id (str): ID of the asset group

        Returns:
            `AssessmentAssetGroupConnection <assessment_asset_group_connection.AssessmentAssetGroupConnection>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssessmentAssetGroupConnection.create('11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222')
        """

        retval = cls.mutate('create_assessment_asset_group_connection', input={'asset_group_id': group_id, 'assessment_id': assessment_id})
        if retval:
            retval = cls.init(retval)
        return retval
