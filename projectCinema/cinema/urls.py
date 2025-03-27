from django.urls import path
from . import views
from .views import login_view
from django.contrib.auth import views as auth_views
from .views import edit_profile
from .views import logout_view
from .forms import CustomPasswordResetForm
from .views import PasswordChangeView


from .forms import UserLoginForm



urlpatterns = [
 path('',views.home, name="home"),
 path('search/', views.search_view,name="search"),
 path('filter/', views.filter_view,name="genre"),
#  path('registration/',views.usrreg,name="reg"),
 path('registration/', views.register, name='register'),
#   path('verify_email/<int:uid>/<str:token>/', views.verify_email, name='verify_email'),
 path('verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),

 path('login/', login_view, name='login'),
 path('edit-profile/', edit_profile, name='edit_profile'),
 path('save-payment/', views.save_payment, name='save_payment'),
 path('logout/', logout_view, name='logout'),
 path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             form_class=CustomPasswordResetForm,
             template_name='html/password_reset_form.html',
             email_template_name='html/password_reset_email.html',
             subject_template_name='html/password_reset_subject.txt',
             success_url='/password_reset/done/', 
         ), 
         name='password_reset'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='html/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='html/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='html/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
     path('admin/', views.admin_view,name="admin"),
 path('admin/movies', views.adminmovies_view,name="admin_movies"),
 path('admin/promotions', views.adminpromotions_view,name="admin_promotions"),
 path('confirmation/', views.confirmation_view,name="confirmation"),
#  path('movies/', views.movies_view,name="movies"),
 path('payment/', views.payment_view,name="payment"),
 path('userprofile/', views.userprofile_view,name="userprofile"),
#  path('movies/', views.movie_list, name='movie_list'),
path('movies/', views.MovieListView.as_view(), name='movie-list'),
 path('mybookings/', views.my_bookings,name="my_bookings"),
#  path('movies/', views.get_movies, name='get_movies'),
path('api/movies/', views.movie_list, name='movie_list'),
path('individual_movie/<str:movie_title>/', views.individual_movie, name='individual_movie'),
path('select_time_and_seats/<str:movie_title>', views.select_time_and_seats, name='select_time_and_seats'),
path('show_seats/<str:movie_title>/<str:selected_date>/<str:show_time>/<int:show_id>/', views.show_seats, name='show_seats'),
path('book_tickets/<str:movie_title>/<str:selected_date>/<str:show_time>/<int:show_id>/', views.book_tickets, name='book_tickets'),
path('get_blocked_seats/', views.get_blocked_seats, name='get_blocked_seats'), #<------------added this
path('apply_promo/<str:movie_title>/<str:selected_date>/<str:show_time>/<int:show_id>/', views.apply_promo, name='apply_promo'),
path('payments/', views.payments, name='payments'),
path('success/',views.success, name='success'),
]