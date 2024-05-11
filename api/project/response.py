from api.response import Response

class ProjectResponse(Response):
  def __init__(self, success, message, project=None, status=None):
    super().__init__(success, message, status)
    self.data['project'] = project

class ProjectListResponse(Response):
  def __init__(self, success, message, projects=None, status=None):
    super().__init__(success, message, status)
    self.data['projects'] = projects
