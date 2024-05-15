from api.response import Response

class ProjectResponse(Response):
  def __init__(self, success, message, project=None, status=None):
    super().__init__(success, message, status)
    self.data['project'] = project

class ProjectTemplateResponse(Response):
  def __init__(self, success, message, project_template=None, status=None):
    super().__init__(success, message, status)
    self.data['project_template'] = project_template

class ProjectTemplateListResponse(Response):
  def __init__(self, success, message, project_templates=None, status=None):
    super().__init__(success, message, status)
    self.data['project_templates'] = project_templates

class ProjectListResponse(Response):
  def __init__(self, success, message, projects=None, status=None):
    super().__init__(success, message, status)
    self.data['projects'] = projects
