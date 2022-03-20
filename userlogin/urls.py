from re import template
from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from django.urls import reverse_lazy

urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('profile',views.profile,name="profile"),
    path('upload_comp',views.upload_comp,name="upload_comp"),
    path('upload_webcam',views.upload_webcam,name="upload_webcam"),
    path('view',views.view,name="view"),
    path('login',auth_view.LoginView.as_view(template_name='userlogin/login.html'),name="login"),
    path('logout',auth_view.LogoutView.as_view(template_name='userlogin/logout.html'),name="logout"),
    path('change_pass',auth_view.PasswordChangeView.as_view(template_name='userlogin/change_pass.html'),name="change"),
    path('password_change/done/',auth_view.PasswordChangeDoneView.as_view(template_name='userlogin/changed.html'), name='password_change_done'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
