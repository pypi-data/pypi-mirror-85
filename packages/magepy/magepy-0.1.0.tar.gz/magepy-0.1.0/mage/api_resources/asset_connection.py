from .abstract import *
from .. import schema

class AssetConnection( MutableAPIResource ):
    """
    Attributes:
        id (str): Unique connection ID
        created_at (str): When the connection was created (e.g., '2020-01-02T03:04:56.789Z')
        updated_at (str): When the connection was last updated (e.g., '2020-01-02T03:04:56.789Z')
        discovery_method (mage.schema.DiscoveryMethod): How the connection was discovered
        state (mage.schema.AssetConnectionState): The state of the connection
        assessment_run_id (str): ID of the associated assessment run 
        asset_source_id (str): ID of the source asset
        asset_destination_id (str): ID of the destination asset
    """

    _UPDATE_FN = 'update_asset_connection'
    _DELETE_FN = 'delete_asset_connection'

    __field_names__ = schema.AssetConnection.__field_names__


    @property
    def assessment(self):
        raise NotImplementedError("Call 'assessment_run' instead of 'assessment'")


    @property
    def assessment_run(self):
        """
        The associated assessment run.

        Returns:
            `AssessmentRun <assessment_run.AssessmentRun>`
        """
        from .assessment_run import AssessmentRun
        return self._nested_resource(AssessmentRun, 'assessment')


    @property
    def asset_source(self):
        """
        The associated source asset.

        Returns:
            `Asset <asset.Asset>`
        """
        from .asset import Asset
        return self._nested_resource(Asset, 'asset_source')


    @property
    def asset_destination(self):
        """
        The associated destination asset.

        Returns:
            `Asset <asset.Asset>`
        """
        from .asset import Asset
        return self._nested_resource(Asset, 'asset_destination')
