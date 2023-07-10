import django.contrib.auth.views
from django.conf import settings
from django.conf.urls.static import static
from django.template.defaulttags import url
from django.urls import path, include
from .views import LoginPageView, LogoutUserView, ProfilePageView

from main import views

urlpatterns =[
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('admin/user/int:<pk>/', views.details, name='details'),
    path('admin/user/int:<pk>/update/', views.edit, name='update'),
    path('admin/user/int:<pk>/delete/', views.delete, name='delete'),
    path('admin/course/int:<pk>/', views.course_details, name='course-details'),
    path('admin/course/create', views.create_course, name='create-course'),
    path('admin/course/int:<pk>/delete', views.course_delete, name='course-delete'),
    path('admin/course/int:<pk>/update', views.course_update, name='course-update'),
    path(r'^activate/(?P<uid64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('courses/', views.course_list, name='courses'),
    path('profile/int:<pk>/', ProfilePageView.as_view(), name='profile'),
    path('publish-requests/accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('publish-requests/reject/<int:request_id>/', views.reject_request, name='reject_request'),
    path('courses/search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)