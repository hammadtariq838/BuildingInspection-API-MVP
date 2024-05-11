from django.urls import path, include

urlpatterns = [
  path('auth/', include('api.auth.urls')),
  path('project/', include('api.project.urls')),
  path('action/', include('api.action.urls')),
	# path('', include(router.urls)),
]