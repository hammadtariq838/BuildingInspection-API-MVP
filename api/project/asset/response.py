from api.response import Response

class AssetResponse(Response):
  def __init__(self, success, message, asset=None, status=None):
    super().__init__(success, message, status)
    self.data['asset'] = asset

class AssetListResponse(Response):
  def __init__(self, success, message, assets=None, status=None):
    super().__init__(success, message, status)
    self.data['assets'] = assets
