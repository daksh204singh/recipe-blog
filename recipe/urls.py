from django.urls import path

from django.contrib.auth import views as auth_views

from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
	path('', views.index, name='index'),
	path('signup/', views.signup, name='signup'),
	path('dashboard/', views.dashboard, name='dashboard'),
	path('logout/', views.logout_request, name='logout'),
    path('<int:category_id>/', views.recipes, name='recipes'),
    path('login/', views.login_request, name='login'),
	path('contact/', views.contact, name='contact'),
	path('about/', views.about, name='about'),
	path('recipe-add/', views.add_recipe, name='add-recipe'),
	path('postrecipe/', views.postrecipe, name='postrecipe'),
    path('receipedetail/<int:id>/', views.receipedetail, name='receipedetail'),
	path('search/', views.search, name='search'),
	path('postComment/', views.postComment, name='postComment'),
	path('deleteRecipe/<int:recipe_id>/', views.deleteRecipe, name='deleteRecipe'),
	path('editRecipe/<int:recipe_id>/', views.editRecipe, name='editRecipe'),
    path('profile/', views.profile_page, name='profile'),
	path('comments/', views.mycomments, name='mycomments'),

	path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='recipe/password_change_done.html'), name='password_change_done'),
	path('password_change/', auth_views.PasswordChangeView.as_view(template_name='recipe/password_change.html'), name='password_change'),
	path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='recipe/password_reset_done.html'), name='password_reset_done'),
	path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
	path('password_reset/', auth_views.PasswordResetView.as_view(template_name='recipe/password_reset_form.html'), name="password_reset"),
	path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='recipe/password_reset_complete.html'), name='password_reset_complete'),
]