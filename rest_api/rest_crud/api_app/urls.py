from django.urls import path,include
from.import views
urlpatterns=[
    path('api-auth/',include('rest_framework.urls')),
    path('create_data',views.add_items.as_view(),name='create_data'),
    path('view_data',views.view_items.as_view(),name='view_data'),
    path('update_data',views.update_items.as_view(),name='update_data'),
    path('delete_data',views.delete_items.as_view(),name='delete_data'),
    path('add_user',views.addUser.as_view(),name='add_user'),
    path('login',views.auth_login.as_view(),name='login'),
    path('search_item',views.search_item.as_view(),name='search_item'),
]