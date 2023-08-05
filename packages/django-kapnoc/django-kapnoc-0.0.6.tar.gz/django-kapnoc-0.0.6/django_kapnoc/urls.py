from django.urls import path

from . import views

app_name = 'django_kapnoc'
urlpatterns = [
    path('image/<str:name>', views.get_image_by_name, name='image_by_name'),
    path('thumb/<str:name>/<str:thumb_type>',
         views.get_thumbnail_by_name, name='thumbnail_by_name'),
    path('image/md_uploader/', views.markdown_uploader,
         name='markdown_uploader_page'),
]
