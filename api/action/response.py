from api.response import Response

class ActionListResponse(Response):
  def __init__(self, success, message, actions=None, status=None):
    super().__init__(success, message, status)
    self.data['actions'] = actions