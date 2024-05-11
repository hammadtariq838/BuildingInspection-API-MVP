import logging
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		# Log the request object
		logger.debug("Request: %s %s", request.method, request.path)
		# logger.debug("Headers: %s", request.headers)
		# logger.debug("Body: %s", request.body)

		response = self.get_response(request)
		return response
