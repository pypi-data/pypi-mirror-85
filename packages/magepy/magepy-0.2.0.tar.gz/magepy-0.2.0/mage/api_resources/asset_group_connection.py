from .abstract import *
from .. import schema

class AssetGroupConnection( MutableAPIResource ):
    """
    Attributes:
        id (str): Unique connection ID
        created_at (str): When the connection was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the connection was last updated (e.g., '2020-01-02T03:04:56.789Z')
        asset_id (str): ID of the associated asset
        group_id (str): ID of the associated group
    """
    _UPDATE_FN = 'update_asset_group_connection'
    _DELETE_FN = 'delete_asset_group_connection'

    __field_names__ = schema.AssetGroupConnection.__field_names__


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
    def create(cls, asset_id, group_id):
        """
        Connects an asset and an asset group.

        Args:
            asset_id (str): ID of the asset
            group_id (str): ID of the asset group

        Returns:
            `AssetGroupConnection <asset_group_connection.AssetGroupConnection>`

        Example:
            >>> import mage
            >>> mage.connect()
            >>> mage.AssetGroupConnection.create('11111111-1111-1111-1111-111111111111', '22222222-2222-2222-2222-222222222222')
        """

        retval = cls.mutate('create_asset_group_connection', input={'group_id': group_id, 'asset_id': asset_id})
        if retval:
            retval = cls.init(retval)
        return retval


    @property
    def group(self):
        """
        The associated asset group.

        Returns:
            `AssetGroup <asset_group.AssetGroup>`
        """
        from .asset import Asset
        return self._nested_resource(AssetGroup, 'group')
