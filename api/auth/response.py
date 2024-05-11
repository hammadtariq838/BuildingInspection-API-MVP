from api.response import Response

class UserResponse(Response):
  def __init__(self, success, message, user=None, token=None, status=None):
    super().__init__(success, message, status)
    if user:
      self.data['user'] = user
    if token:
      self.data['token'] = token


class UserListResponse(Response):
  def __init__(self, success, message, users=None, status=None):
    super().__init__(success, message, status)
    self.data['users'] = users

class TokenResponse(Response):
  def __init__(self, success, message, token=None, status=None):
    super().__init__(success, message, status)
    self.data['token'] = token