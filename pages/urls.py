from django.urls import path
from .views import listPost,createPost,updatePost,deletePost,userPostList
from . import views

urlpatterns = [
path("", listPost.as_view(), name='page-home'),
path("about/", views.about, name='page-about'),
path("register/", views.register, name='page-register'),
path("login/", views.loginPage, name='page-login'),
path("logout/", views.logoutUser, name='page-logout'),
path("account/", views.account_settings, name='page-account'),
path("profile/", views.profilePage, name='page-profile'),
path("post/<int:pk>/", views.detailPost, name='page-detail'),
path("post/new/", createPost.as_view(), name='page-create'),
path("post/<int:pk>/update", updatePost.as_view(), name='page-update'),
path("post/<int:pk>/delete", deletePost.as_view(), name='page-delete'),
path("user/<str:username>", userPostList.as_view(), name='user-posts'),
]
