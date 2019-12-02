from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from main import views
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

urlpatterns = [
    url(r'^', include('main.urls')),
    path('edit_comment/<int:comment_id>', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>', views.delete_comment, name='delete_comment'),
    url(r'^movies/', include('main.urls')),
    url(r'^admin/', admin.site.urls),
    path('create_seats/', views.create_seats, name='create_seats'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('account/', user_views.account, name='account'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),kwargs={'redirect_authenticated_user': True}, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/login.html'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
