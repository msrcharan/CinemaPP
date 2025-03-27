from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Movie, Show
from datetime import datetime
# from .forms import RegForm
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordChangeView as DjangoPasswordChangeView
from django.urls import reverse_lazy
from django.utils.html import strip_tags
from django.contrib import messages
from django.views.generic import ListView
from django.http import JsonResponse
from django.http import Http404
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Show, Screen, Seat




# Create your views here.

def home(request):
    now_showing=Movie.objects.filter(release_date__lte=datetime.now())
    coming_soon = Movie.objects.filter(release_date__gt=datetime.now())
    return render(request,'html/index.html',{'now_showing':now_showing, 'coming_soon':coming_soon})

def search_view(request):
    print(request)
    query = request.GET.get('q')
    if query:
        results = Movie.objects.filter(title__icontains=query)
        return render(request, 'html/search_results.html', {'results': results})
    else:
        return redirect('search_page')
    
# def register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             # Redirect to a success page or login page
#             return redirect('login') #home
#     else:
#         form = RegistrationForm()
#     return render(request, 'html/registration.html', {'form': form})
    
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            
            # Send confirmation email
            subject = 'Welcome to Our Website!'
            message = f'Hi {user.username},\n\nThank you for registering on our website. Your account has been successfully created.'
            from_email = 'spinox.spingamer@gmail.com'  # Update with your email
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])

            # Redirect to a success page or login page
            return redirect('login')  # Or any other page you want to redirect to
    else:
        form = RegistrationForm()
        messages.error(request, 'Passwords do not match.')
    return render(request, 'html/registration.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:
                    request.session['remembered_username'] = username
                    request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.pop('remembered_username', None)
                    request.session.set_expiry(0)
                
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.') #added this<---------------
                return render(request, 'html/login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = UserLoginForm()
        # if 'remembered_username' in request.session:
        #     form = UserLoginForm(initial={'username': request.session['remembered_username']})
        if 'remembered_username' in request.session:
            form = UserLoginForm(initial={'username': request.session['remembered_username']})
    return render(request, 'html/login.html', {'form': form})


# @login_required
# def edit_profile(request):
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             # Redirect to profile page or any other appropriate page
#             return redirect('home')
#     else:
#         form = EditProfileForm(instance=request.user)
#     return render(request, 'html/EditProfile.html', {'form': form})


# @login_required
# def edit_profile(request):
#     username = request.user.username
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, request.FILES, instance=request.user)
#         password_form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid() and password_form.is_valid():
#             # user = form.save()
#             # password = password_form.cleaned_data['new_password1']
#             user = form.save(commit=False)
#             receive_promotions = form.cleaned_data.get('receive_promotions')
#             user.receive_promotions = receive_promotions  # Update receive_promotions field
#             user.save()
            
#             password = password_form.cleaned_data['new_password1']

#             if password:
#                 user.set_password(password)
#                 user.save()
#                 update_session_auth_hash(request, user)  
#             return redirect('home')
#     else:
#         form = EditProfileForm(instance=request.user)
#         password_form = PasswordChangeForm(request.user)
#     return render(request, 'html/EditProfile.html', {'form': form, 'password_form': password_form})

@login_required
def edit_profile(request):
    username = request.user.username
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        # password_form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid(): #and password_form.is_valid():
            user = form.save(commit=False)
            receive_promotions = form.cleaned_data.get('receive_promotions')
            user.receive_promotions = receive_promotions  # Update receive_promotions field
            user.save()
            
            # password = password_form.cleaned_data['new_password1']

            # if password:
            #     user.set_password(password)
            #     user.save()
            #     update_session_auth_hash(request, user)
                
            # Send email to the user
            subject = 'Profile Updated'
            message = f'Hi {user.username},\n\n Your account has been successfully updated.'
            # plain_message = strip_tags(html_message)
            from_email = 'p@gmail.com' 
            to_email = user.email
            # send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
            send_mail(subject, message, from_email, [to_email])
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)
        # password_form = PasswordChangeForm(request.user)
    return render(request, 'html/EditProfile.html', {'form': form}) #, 'password_form': password_form

@login_required
def logout_view(request):
        logout(request)
        return redirect('home')

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'registration/password_reset_form.html'
#     form_class = CustomPasswordResetForm
#     email_template_name = 'registration/password_reset_email.html'
#     success_url = '/password_reset/done/'

class PasswordChangeView(DjangoPasswordChangeView):
    template_name = 'html/password_change.html'
    success_url = '/edit-profile/'

def change_password(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            # Update session authentication hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('')  # Redirect to home page after password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        password_form = PasswordChangeForm(request.user)  # Initialize password change form
    return render(request, 'changepassword.html', {'password_form': password_form})

def admin_view(request):
    return render(request,'html/admin.html')

def adminmovies_view(request):
    return render(request,'html/adminmovies.html')

def adminpromotions_view(request):
    return render(request,'html/adminpromotions.html')

def confirmation_view(request):
    return render(request,'html/confirmation.html')

# def movies_view(request):
#     return render(request,'html/movies.html')

def payment_view(request):
    return render(request,'html/payment.html')

def userprofile_view(request):
    return render(request,'html/userprofile.html')

# def movie_list(request):
#     movies = Movie.objects.all()  # Fetch all movies from the database
#     return render(request, 'html/movies.html', {'movies': movies})

class MovieListView(ListView):
    model = Movie
    template_name = 'html/movies.html'
    context_object_name = 'movies'

# def individual_movie(request, movie_title):
#     # Retrieve the movie details using the movie_id
#     # movie = get_object_or_404(Movie, title=movie_title)
#     # context = {
#     #     'title': movie.title,
#     #     'trailer_url': movie.trailer_url,
#     #     'poster_image_url': movie.image.url if movie.image else None,
#     #     'description': movie.description,
#     # }
#     movie= request.GET.get('movie_title')
#     return render(request, 'html/individual_movie.html', {'movie_title': movie_title})
    
def individual_movie(request, movie_title):
    # # Retrieve the movie details from the database based on the provided movie title
    # movie = get_object_or_404(Movie, title=movie_title)

    # # Pass the movie details to the HTML template
    # context = {
    #     'movie': movie,  # Pass the entire movie object to access all its attributes in the template
    # }
    # movie1= request.GET.get('movie_title')
    # return render(request, 'html/individual_movie.html', context)
    movie = get_object_or_404(Movie, title=movie_title)
    shows = movie.show_set.all()  # Retrieve all shows for this movie
    # shows = Show.objects.filter(movie=movie)
    return render(request, 'html/individual_movie.html', {'movie': movie, 'shows': shows})

def select_time_and_seats(request, movie_title):
    # selected_date = request.GET.get('selected_date')
    # if not selected_date:
    #     raise Http404("No date selected.")
    
    # try:
    #     datetime.strptime(selected_date, '%Y-%m-%d')
    # except ValueError:
    #     raise Http404("Invalid date format. Date must be in YYYY-MM-DD format.")

    # # movie = get_object_or_404(Movie, title=movie_title)
    # # # Filter shows based on the selected date (date only, without time)
    # # # shows = Show.objects.filter(movie=movie, start_time__date=selected_date)
    # # shows = Show.objects.filter(movie=movie, start_time__date=selected_date)
    # # # Print start_time__date for each show
    # # # for show in shows:
    # # #     print(show.start_time__date)
    
    # # return render(request, 'html/select_time_and_seats.html', {'movie': movie, 'selected_date': selected_date, 'shows': shows})
    # movie = get_object_or_404(Movie, title=movie_title)
    # # Filter shows based on the selected date
    # shows = Show.objects.filter(movie=movie, start_time__date=selected_date)
    # for show in shows:
    #         print(show.start_time__date)

    # return render(request, 'html/select_time_and_seats.html', {'movie': movie, 'selected_date': selected_date, 'shows': shows})
    selected_date = request.GET.get('selected_date')
    if not selected_date:
        raise Http404("No date selected.")
    
    try:
        datetime.strptime(selected_date, '%Y-%m-%d')
    except ValueError:
        raise Http404("Invalid date format. Date must be in YYYY-MM-DD format.")

    movie = get_object_or_404(Movie, title=movie_title)
    shows = Show.objects.filter(movie=movie, start_time__date=selected_date)
    
    return render(request, 'html/select_time_and_seats.html', {'movie': movie, 'selected_date': selected_date, 'shows': shows})

def show_seats(request, show_id, movie_title, selected_date, show_time):
    movie = get_object_or_404(Movie, title=movie_title)
    print("movie:", movie)
    # show = get_object_or_404(Show, movie=movie, start_time=show_time)
    # screen = get_object_or_404(Screen, number=screen_number)
    # show = get_object_or_404(Show, screen__number=screen_number, movie__title=movie_title, start_time=show_time)
    show = get_object_or_404(Show, movie__title=movie_title, start_time=show_time)
    print("show:", show)
    # Now you can access the screen number associated with the show
    # screen_number = show.screen
    # show_id=show.id
    seats = Seat.objects.filter(screen_number=show.screen, is_booked=False)
    return render(request, 'html/show_seats.html', {'movie': movie, 'show': show, 'selected_date': selected_date, 'available_seats': seats})
    
