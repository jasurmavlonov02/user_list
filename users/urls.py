from django.urls import path

from users.views.auth import logout_page, LoginPage
from users.views.views import user_list, user_details, user_add, user_delete, user_update

urlpatterns = [
    path('user-list/', user_list, name="user_list"),
    path('user-details/<int:pk>', user_details, name="user_details"),
    path('user-delete/<int:pk>', user_delete, name="user_delete"),
    path('user-update/<int:pk>', user_update, name="user_update"),
    path('user-add/', user_add, name="user_add"),

    path('', LoginPage.as_view(), name="login_page"),
    path('logout-page/', logout_page, name='logout_page'),
    path('category/<str:cats>/', user_list, name='category_by_slug'),


]
