from .abstract import *
from .. import schema

class AssetGroup( ListableAPIResource, MutableAPIResource ):
    """
    Attributes:
        id (str): Unique asset group ID (e.g., '11111111-1111-1111-1111-111111111111')
        name (str): Name of the group
        created_at (str): When the asset group was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the asset group was last updated (e.g., '2020-01-02T03:04:56.789Z')
    """

    _GET_FN     = 'get_asset_group'
    _LIST_FN    = 'list_asset_groups'
    _SEARCH_FN  = 'search_asset_groups'
    _UPDATE_FN  = 'update_asset_group'
    _DELETE_FN  = 'delete_asset_group'
    _SORT_FIELD = 'name'

    __field_names__ = schema.AssetGroup.__field_names__


    @property
    def assessments(self):
        """
        Associated assessments.

        Returns:
            `ListObject` of `AssessmentAssetGroupConnection <assessment_asset_group_connection.AssessmentAssetGroupConnection>`
        """
        from .assessment_asset_group_connection import AssessmentAssetGroupConnection
        return self._nested_resource_list(AssessmentAssetGroupConnection, 'assessments', AssessmentAssetGroupConnection.__field_names__)


    @property
    def assets(self):
        """
        Associated assets.

        Returns:
            `ListObject` of `AssetGroupConnection <asset_group_connection.AssetGroupConnection>`
        """
        from .asset_group_connection import AssetGroupConnection
        return self._nested_resource_list(AssessmentAssetGroupConnection, 'assets', AssessmentAssetGroupConnection.__field_names__)


    def connect(self, item = None, assessment_id = None, asset_id = None):
        """
        Connect an asset group to an assessment or asset

        Args:
            item (object, optional): Assessment or Asset to connect the group to
            assessment_id (str, optional): ID of the assessment to connect the group to
            asset_id (str, optional): ID of the asset to connect the group to

        Returns:
            `AssessmentAssetGroupConnection <assessment_asset_group_connection.AssessmentAssetGroupConnection>` or `AssetGroupConnection <asset_group_connection.AssetGroupConnection>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> ag = mage.AssetGroup.eq(name='My Group')[0]
            >>> ag.connect(mage.Assessment.eq(name='MyAssessment')[0])
            >>> ag.connect(asset_id=mage.Asset.eq(id='192.168.1.1')[0].id)
        """
        from .assessment import Assessment
        from .assessment_asset_group_connection import AssessmentAssetGroupConnection
        from .asset import Asset
        from .asset_group_connection import AssetGroupConnection

        if isinstance(item, Assessment) or assessment_id:
            if item:
                assessment_id = item.id
            retval = self.mutate('create_assessment_asset_group_connection', input={'asset_group_id': self.id, 'assessment_id': assessment_id})
            if retval:
                retval = AssessmentAssetGroupConnection.init(retval)
            return retval

        if isinstance(item, Asset) or asset_id:
            if item:
                asset_id = item.id
            retval = self.mutate('create_asset_group_connection', input={'group_id': self.id, 'asset_id': asset_id})
            if retval:
                retval = AssetGroupConnection.init(retval)
            return retval

        raise RuntimeError("%s not supported" % type(item))


    @classmethod
    def create(cls, name, **kwargs):
        """
        Creates an asset group.

        Args:
            name (str): Name of the asset group
            **kwargs: Additional arguments to initialize the asset group with.

        Returns:
            `AssetGroup <asset_group.AssetGroup>`: The created asset group

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssetGroup.create('web servers')
        """

        from mage import client_id
        retval = cls.mutate('create_asset_group', input={'assetGroupClientId': client_id, 'name': name, **params})
        if retval:
            retval = cls.init(retval)
        return retval
