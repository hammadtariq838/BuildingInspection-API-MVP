from rest_framework.response import Response as BaseResponse

class Response(BaseResponse):
  def __init__(self, success, message, status=None):
    super().__init__({
      'success': success,
      'message': message,
    }, status=status)

class ErrorResponse(Response):
  def __init__(self, message, status=None, error=None):
    super().__init__(False, message, status)
    if error:
      self.data['error'] = error
