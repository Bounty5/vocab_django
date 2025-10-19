from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.group_list, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("show_vocab/", views.show_vocab, name="show_vocab"),
    path('vocab/<int:vocab_id>/toggle/', views.toggle_learned, name='toggle_learned'),
    path("groups/", views.group_list, name="group_list"), 
    path("groups/add/", views.add_group, name="add_group"),
    path("groups/<int:group_id>/", views.group_detail, name="group_detail"),
    path("groups/<int:group_id>/add_vocab/", views.add_vocab_to_group, name="add_vocab_to_group"),
    path('groups/<int:group_id>/toggle/', views.toggle_learned_group, name='toggle_learned_group'),
    path("groups/vocab/<int:vocab_id>/toggle/", views.toggle_learned_vocab_in_group, name="toggle_learned_vocab_in_group"),
    path("groups/<int:group_id>/delete_group/", views.delete_group, name="delete_group"),
    path("groups/vocab/<int:vocab_id>/delete/", views.delete_vocab, name="delete_vocab"),
    path("groups/<int:group_id>/test/", views.vocab_test, name="vocab_test"),
    path("groups/<int:group_id>/flash_card/", views.vocab_flashcard, name="flash_card"),
    path("friends/", views.friends_list, name="friends_list"),
    path("friends/send/<str:username>/", views.send_friend_request, name="send_friend_request"),
    path("friend/accept/<int:request_id>", views.accept_friend_request, name="accept_friend_request"),
    path("friend/reject/<int:request_id>", views.reject_friend_request, name="reject_friend_request"),
    path("friends/find/", views.find_friends, name="find_friends"),

]
