from django.urls import path
from . import views

urlpatterns = [
	path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutPage, name='logout'),
	path('', views.homePage, name='index'),
	path('/<str:tag>', views.allQuestionPage, name='all-questions'),
	path('/<str:tag>/blogs', views.allBlogPage, name='all-blog'),
	path('/<str:tag>/blogs/<int:id>', views.blogPage, name='blog'),
	path('/<str:tag>/blogs/new-blog', views.newBlog, name='new-blog'),
	path('/<str:tag>/<int:id>', views.questionPage, name='question'),
	path('/<str:tag>/new-question', views.newQquestion, name='new-question'),
	path('reply', views.replyPage, name='reply')
]