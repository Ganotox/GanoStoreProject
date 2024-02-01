from django.urls import path
from . import views
from .views import manage_moderators, add_moderator, remove_moderator, user_list, block_user, unblock_user, \
    password_reset_request, secret_question

urlpatterns = [
    path('register/', views.register, name='register'),  #
    path('login/', views.login_view, name='login'),  #
    path('logout/', views.logout_view, name='logout'),  #
    path('about/', views.about_us, name='about_us'),  #
    path('contact/', views.contact, name='contact'),  #
    path('edit_profile/', views.edit_profile, name='edit_profile'),  #
    path('upload_program/', views.upload_program, name='upload_program'),  #
    path('program/<int:program_id>/', views.program_detail, name='program_detail'),  #
    path('program/<int:program_id>/edit/', views.edit_program, name='edit_program'),  #
    path('program/<int:program_id>/delete/', views.delete_program, name='delete_program'),  #
    path('program/<int:program_id>/comment/', views.add_comment, name='add_comment'),  #
    path('program/<int:program_id>/complaint/', views.submit_complaint, name='submit_complaint'),  #
    path('search/', views.search, name='search'),  #
    path('rules/', views.rules, name='rules'),  #
    path('change_theme/', views.change_theme, name='change_theme'),  #
    path('manage_users/', views.manage_users, name='manage_users'),  #
    path('manage_programs/', views.manage_programs, name='manage_programs'),  #
    path('view_complaints/', views.view_complaints, name='view_complaints'),  #
    path('manage_moderators/', views.manage_moderators, name='manage_moderators'),  #
    path('user/<str:username>/', views.user_profile, name='user_profile'),  #
    path('user/<str:username>/programs/', views.user_programs, name='user_programs'),  #
    path('program/<int:program_id>/rate/', views.rate_program, name='rate_program'),
    path('manage_moderators/', manage_moderators, name='manage_moderators'),
    path('add_moderator/<int:user_id>/', add_moderator, name='add_moderator'),
    path('remove_moderator/<int:user_id>/', remove_moderator, name='remove_moderator'),
    path('users/', user_list, name='user_list'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('complaints/', views.view_complaints, name='view_complaints'),
    path('complaints/resolve/<int:complaint_id>/', views.resolve_complaint, name='resolve_complaint'),
    path('users/unblock/<int:user_id>/', unblock_user, name='unblock_user'),
    path('password_reset_request/', password_reset_request, name='password_reset_request'),
    path('secret_question/<int:user_id>/', secret_question, name='secret_question'),
    # Головна сторінка
    path('', views.home, name='home'),
]
