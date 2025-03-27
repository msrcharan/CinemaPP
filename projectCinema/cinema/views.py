from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Movie, Show
from datetime import datetime
# from .forms import RegForm
from .forms import RegistrationForm
from decimal import Decimal, ROUND_DOWN
import json
from django.utils import timezone
from django.db.models.signals import post_save
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.db.models import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.dispatch import receiver
from .forms import EditProfileForm, EditPaymentForm
import random
import string
import qrcode
from io import BytesIO
import base64
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
from .models import Show, Screen, Seat, PromoCode, Booking, User
from django.contrib.auth import get_user_model

User = get_user_model()


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

def filter_view(request):
    movies = Movie.objects.all()
    
    genre_filters = request.GET.getlist('genre')
    release_date = request.GET.get('release_date')
    print(genre_filters)
    print(release_date)
    query = Q()
    if genre_filters or release_date:
        if genre_filters:
            genre_filter_query = Q()
            for genre in genre_filters:
                genre_filter_query |= Q(genre__icontains=genre.strip())
            query &= genre_filter_query
        
       
        if release_date:
            print("inside")
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
            query &= Q(release_date=release_date)
            print(query)
        # query &= genre_filter_query
        queryset = Movie.objects.filter(query)
        print(queryset)
        return render(request, 'html/filter_movies.html', {'queryset': queryset})
    else:
        return redirect('login')
    
# def filter_view(request):
#     movies = Movie.objects.all()
#     print("inside")
#     genre_filters = request.GET.getlist('genre')
#     print(genre_filters)
#     # queryset = movies
#     if genre_filters:
#         genre_filter_query = Q()
#         for genre in genre_filters:
#             genre_filter_query |= Q(genre__icontains=genre.strip())
#         queryset = Movie.objects.filter(genre_filter_query)
#         print(queryset)
#         return render(request, 'html/filter_movies.html', {'queryset': queryset})
#     else:
#         return redirect('login')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            user = form.save(commit=False)
            user.is_active = False  # Set is_active to False initially
            user.save()
            
            token_generator = default_token_generator
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            current_site = get_current_site(request)
            verification_url = f"{current_site.domain}/verify/{uid}/{token}/"

            subject = 'Verify Your Email Address'
            message = render_to_string('html/verification_email.html', {
                'user': user,
                'verification_url': verification_url,
            })
            from_email = 'p@gmail.com'
            to_email = user.email
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, from_email, [to_email])
            if form.cleaned_data['receive_promotions'] and not form.cleaned_data['email']:  #not working <---------
               form.add_error('email', 'Email is required for receiving promotions.')
            if form.cleaned_data['password'] != form.cleaned_data['confirm_password']:
                form.add_error('password', 'Passwords do not match') 
            # else:
            #     user = form.save()
            #     return redirect('login')  # Redirect to a success page
            return redirect('login')
    else:
        form = RegistrationForm()
        messages.error(request, 'Passwords do not match..')
    return render(request, 'html/registration.html', {'form': form})


def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'html/email_verified.html')
    else:
        return render(request, 'html/invalid_link.html')


@receiver(post_save, sender=PromoCode)
def send_promo_email(sender, instance, created, **kwargs):
    if created:
        users_to_notify = User.objects.filter(receive_promotions=True)
        subject = 'New Promo Code Available!'
        html_message = render_to_string('html/new_promo_email.html', {'promo_code': instance})
        plain_message = strip_tags(html_message)
        from_email = 'p@gmail.com'  # Update with your email address
        recipient_list = [user.email for user in users_to_notify]

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)


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
            subject = 'Profile Updated'
            message = f'Hi {user.username},\n\n Your account has been successfully updated.'
            from_email = 'p@gmail.com'
            to_email = user.email
            send_mail(subject, message, from_email, [to_email])
            return redirect('/edit-profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'html/EditProfile.html', {'form': form}) #, 'password_form': password_form

@login_required
def logout_view(request):
        logout(request)
        return redirect('home')

def save_payment(request):
    if request.method == 'POST':
        form = EditPaymentForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment details saved successfully.')
            return redirect('/edit-profile/')
        else:
            messages.error(request, 'Error saving payment details. Please try again.')
    else:
        form = EditPaymentForm(request.POST, instance=request.user)
        return render(request, 'html/edit_profile.html', {'form': form})


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

def my_bookings(request):
    # Retrieve all bookings associated with the logged-in user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'html/myBookings.html', {'bookings': bookings})

class MovieListView(ListView):
    model = Movie
    template_name = 'html/movies.html'
    context_object_name = 'movies'

    # def get_queryset(self):
    #     movies = Movie.objects.all()
    #     print("inside")
    #     genre_filters = self.request.GET.getlist('genre')
    #     print(genre_filters)
    #     # queryset = movies
    #     if genre_filters:
    #         genre_filter_query = Q()
    #         for genre in genre_filters:
    #             genre_filter_query |= Q(genre__icontains=genre.strip())
    #         queryset = movies.filter(genre_filter_query)
    #         print(queryset)
    #     else:
    #         queryset = movies
    #     return queryset
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # release_date = self.request.GET.get('release_date')
    #     genre = self.request.GET.get('genre')

    #     # if release_date:
    #     #     queryset = queryset.filter(release_date__gte=release_date)

    #     if genre:
    #         queryset = queryset.filter(Q(genre__icontains=genre))
        
    #     return queryset

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     movies = Movie.objects.all()
    #     release_date = self.request.GET.get('release_date')
    #     genre = self.request.GET.get('genre')
    #     print(genre)
    #     if release_date:
    #         queryset = queryset.filter(release_date__gte=release_date)
    #     # else:
    #     #     # Show movies released from today onwards
    #     #     today = timezone.now().date()
    #     #     queryset = queryset.filter(release_date__gte=today)
    #     # if genre:
    #     #     queryset = queryset.filter(genre=genre)
    #     if genre:  # If genre filter is provided in the URL parameters
    #     # Filter movies by genre
    #         queryset = movies.filter(
    #             Q(genre__icontains=genre) # Add more fields if necessary
    #         )
    #     return queryset




@login_required
def individual_movie(request, movie_title):
    movie = get_object_or_404(Movie, title=movie_title)
    shows = movie.show_set.all() 
    return render(request, 'html/individual_movie.html', {'movie': movie, 'shows': shows})

def select_time_and_seats(request, movie_title):
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
    
    mpaa_rating = movie.rating
    print("movie:", movie)
    show = get_object_or_404(Show, movie__title=movie_title, start_time=show_time)
    show_id=show.show_id
    screen_id=show.screen
    print(screen_id)
    seats = Seat.objects.filter(screen_id=show.screen_id, is_booked=False)
    capacity=Screen.capacity
    ticket_quantity = request.POST.get('ticket_quantity')
    child_tickets = int(request.POST.get('child_tickets', 0))
    adult_tickets = int(request.POST.get('adult_tickets', 0))
    senior_tickets = int(request.POST.get('senior_tickets', 0))
    return render(request, 'html/show_seats.html', {
                                                    'movie': movie, 
                                                    'show': show, 
                                                    'selected_date': selected_date, 
                                                    'available_seats': seats, 
                                                    'ticket_quantity': ticket_quantity, 
                                                    'mpaa_rating':mpaa_rating,
                                                    "show_id":show_id,
                                                    "screen_id": screen_id
                                                    })

def get_blocked_seats(request):
    if request.method == 'GET':
        show_id = request.GET.get('show_id')
        print("inside get",show_id)
        if show_id:
            blocked_seats = Seat.objects.filter(show_id=show_id, is_booked=True).values_list('row', 'number')
            blocked_seats_list = [f"{seat[0]}{seat[1]}" for seat in blocked_seats]
            print("blocked: ", blocked_seats_list)
            return JsonResponse(blocked_seats_list, safe=False)

    return JsonResponse([], safe=False)

def tickets_sep(request, show_id, movie_title, selected_date, show_time):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, title=movie_title)
        screen_id = request.POST.get('screen_id')
        show_id = request.POST.get('show_id')
        print("screen_id:", screen_id)
        ticket_quantity = request.POST.get('ticket_quantity')
        mpaa_rating = movie.rating
        show = get_object_or_404(Show, movie__title=movie_title, start_time=show_time)
        ticket_price = 10
        total_price = int(ticket_quantity) * ticket_price
        tax = int(total_price)*0.07
        tax = Decimal(tax).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        booking_fees=2
        total_new_price= total_price+tax+booking_fees
        seats = request.POST.get('selected_seats_list')
        # formatted_seats = ", ".join(seats)
        formatted_seats = seats.replace("[", "").replace("]", "").replace('"', "").replace(",",", ")
        print(seats)
        child_tickets = int(request.POST.get('child_tickets', 0))
        adult_tickets = int(request.POST.get('adult_tickets', 0))
        senior_tickets = int(request.POST.get('senior_tickets', 0))
        print(child_tickets)

    return render(request, 'html/tickets_sep.html',{
        'movie_title': movie_title,
        'show': show, 
        'selected_date': selected_date, 
        'show_time':show_time, 
        'ticket_quantity': ticket_quantity, 
        'total_price':total_price ,
        'tax':tax,
        'booking_fees':booking_fees,
        'total_new_price':total_new_price,
        'mpaa_rating':mpaa_rating,
        'seats': seats,
        "formatted_seats": formatted_seats,
        "screen_id": screen_id,
        "show_id":show_id,
        "child_tickets": child_tickets,
        "adult_tickets":adult_tickets,
        "senior_tickets": senior_tickets
        })


def book_tickets(request, show_id, movie_title, selected_date, show_time):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, title=movie_title)
        screen_id = request.POST.get('screen_id')
        show_id = request.POST.get('show_id')
        print("screen_id:", screen_id)
        ticket_quantity = request.POST.get('ticket_quantity')
        mpaa_rating = movie.rating
        show = get_object_or_404(Show, movie__title=movie_title, start_time=show_time)
        ticket_price = 10
        total_price = int(ticket_quantity) * ticket_price
        tax = int(total_price)*0.07
        tax = Decimal(tax).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        booking_fees=2
        total_new_price= total_price+tax+booking_fees
        seats = request.POST.get('selected_seats_list')
        # formatted_seats = ", ".join(seats)
        formatted_seats = seats.replace("[", "").replace("]", "").replace('"', "").replace(",",", ")

        print(seats)
        

    return render(request, 'html/book_tickets.html',{
        'movie_title': movie_title,
        'show': show, 
        'selected_date': selected_date, 
        'show_time':show_time, 
        'ticket_quantity': ticket_quantity, 
        'total_price':total_price ,
        'tax':tax,
        'booking_fees':booking_fees,
        'total_new_price':total_new_price,
        'mpaa_rating':mpaa_rating,
        'seats': seats,
        "formatted_seats": formatted_seats,
        "screen_id": screen_id,
        "show_id":show_id
        })

def apply_promo(request, show_id, movie_title, selected_date, show_time):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, title=movie_title)
        screen_id = request.POST.get('screen_id')
        show_id = request.POST.get('show_id')
        
        mpaa_rating = movie.rating
        ticket_quantity = request.POST.get('ticket_quantity')
        selected_seats = request.POST.get('selected_seats')
        show = get_object_or_404(Show, movie__title=movie_title, start_time=show_time)
        ticket_price = 10
        total_price = int(ticket_quantity) * ticket_price
        tax = int(total_price)*0.07
        tax = Decimal(tax).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
        booking_fees=2
        total_new_price= total_price+tax+booking_fees
        promo_code = request.POST.get('promo_code')
        discount = Decimal(0)
        # total_new_price= total_new_price - discount
        seats = request.POST.get('selected_seats_list') #added this <---------
        formatted_seats = seats.replace("[", "").replace("]", "").replace('"', "").replace(",",", ")
        if promo_code:
            promo = PromoCode.objects.filter(code=promo_code).first()
            if promo:
                # Check if the promo is valid
                if promo.valid_from <= show.start_time <= promo.valid_to:
                    # Check if the promo code has reached its max usage count
                    if promo.current_usage_count < promo.max_usage_count:
                        # Apply discount based on the type
                        if promo.discount_type == 'Percentage':
                            discount = total_new_price * (promo.discount_value / 100)
                            discount = Decimal(discount).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
                        elif promo.discount_type == 'Fixed Amount':
                            discount = promo.discount_value
                        total_new_price -= discount
                        # Increment usage count
                        promo.current_usage_count += 1
                        promo.save()

    return render(request, 'html/book_tickets.html',{
        'movie_title': movie_title,
        'show': show, 
        'selected_date': selected_date, 
        'show_time':show_time, 
        'selected_seats':selected_seats, 
        'ticket_quantity': ticket_quantity, 
        'total_price':total_price ,
        'tax':tax,
        'booking_fees':booking_fees,
        'total_new_price':total_new_price,
        'discount': discount,
        'mpaa_rating':mpaa_rating,
        "formatted_seats": formatted_seats,
        "screen_id": screen_id,
        "show_id":show_id
        })
    



def payments(request):
    if request.method == 'POST':
        # Retrieve payment details from the form data
        screen_id = request.POST.get('screen_id')
        show_id = request.POST.get('show_id')
        
        movie_title = request.POST.get('movie_title')
        selected_date = request.POST.get('selected_date')
        show_time = request.POST.get('show_time')
        ticket_quantity = request.POST.get('ticket_quantity')
        selected_seats = request.POST.get('selected_seats_list')
        total_price = request.POST.get('total_price')
        tax = request.POST.get('tax')
        booking_fees = request.POST.get('booking_fees')
        mpaa_rating = request.POST.get('mpaa_rating')
        total_new_price = request.POST.get('total_new_price')
        seats=request.POST.get("formatted_seats")
        print("Seats are:",seats)
        user = request.user
        credit_card_number = user.credit_card_number
        credit_card_expiry = user.credit_card_expiry
        credit_card_cvv = user.credit_card_cvv
        dt = datetime.strptime(show_time, "%Y-%m-%d %H:%M:%S")

        time_str = dt.strftime("%H:%M:%S")
        date_str=dt.strftime("%Y-%m-%d")
        # print(credit_card_number)
        # print("seats"+selected_seats)
        payment_success_message = f"Payment successful for {ticket_quantity} ticket(s) for {movie_title} on {date_str} at {time_str}. Total price: ${total_new_price}"
        print(payment_success_message)
        # Render a response page with the payment success message
        return render(request, 'html/payment.html', {'payment_success_message': payment_success_message, 
                                                     'movie_title':movie_title,
                                                     'total_price':total_price,
                                                     'total_new_price':total_new_price,
                                                     'ticket_quantity': ticket_quantity,
                                                     'booking_fees':booking_fees,
                                                     'show_time': show_time,
                                                     'selected_seats':selected_seats,
                                                     'tax':tax,
                                                     'mpaa_rating':mpaa_rating,
                                                     'credit_card_number': credit_card_number,
                                                     'credit_card_expiry': credit_card_expiry,
                                                     'credit_card_cvv': credit_card_cvv,
                                                     "seats": seats,
                                                     "screen_id": screen_id,
                                                     "show_id":show_id,
                                                     "date":date_str,
                                                     "time": time_str
                                                     })

    else:
        # Return an error response if the request method is not supported
        return HttpResponse("Unsupported request method")
    
def success(request):
    if request.method == 'POST':
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choices(characters, k=8))
        date = request.POST.get('date')
        time = request.POST.get('time')
        movie_title = request.POST.get('movie_title')
        mpaa_rating = request.POST.get('mpaa_rating')
        show_id = request.POST.get('show_id')
        print("show id:", show_id)
        selected_date = request.POST.get('selected_date')
        screen_id = request.POST.get('screen_id')
        show_time = request.POST.get('show_time')
        ticket_quantity = request.POST.get('ticket_quantity')
        seats = request.POST.get('seats')
        total_price = request.POST.get('total_price')
        tax = request.POST.get('tax')
        print("Seats pay:",seats)

        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )

        # Add data to the QR code
        qr.add_data(code)
        qr.make(fit=True)
        qr_image_stream = BytesIO()

        # Create an image from the QR code
        qr.make_image(fill_color="black", back_color="white").save(qr_image_stream)
        qr_image_base64 = base64.b64encode(qr_image_stream.getvalue()).decode()



        booking_fees = request.POST.get('booking_fees')
        total_new_price = request.POST.get('total_new_price')
        print(seats)
        n_seats=seats.replace(" ","")
        k=[]
        k.append(n_seats.split(","))
        for seat_info in k:
            for i in seat_info:
                row = i[0]
                number = (i[1:])
                print(number)
                # show_instance = get_object_or_404(Show, pk=show_id)
                seat, created = Seat.objects.get_or_create(
                show_id=show_id,
                screen_id=screen_id,
                row=row,
                number=number
                )
        

                if created:
                    seat.is_booked = True  
                    seat.save()
        booking = Booking.objects.create(
        user=request.user,
        show=movie_title,
        # booking_time=datetime.now(), 
        booking_time=show_time,
        total_amount=total_new_price,
        status='Confirmed',
        booking_id=code, 
        seats=n_seats 
    )
        booking.save()
                    # Send email to user
        subject = 'Order Confirmation'
        html_message = render_to_string('html/email_template.html', {
            'booking_id':code,
            'movie_title': movie_title,
            'show_time': show_time,
            'ticket_quantity': ticket_quantity,
            'seats': seats,
            'mpaa_rating': mpaa_rating,
            "qr_code":qr_image_base64
        })
        plain_message = strip_tags(html_message)
        from_email = 'p@gmail.com'
        to_email = request.user.email  # Assuming the user is logged in
        send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)
        return render(request, 'html/payment_success.html', {
                                                     'movie_title':movie_title,
                                                     'show_time': show_time,
                                                     "seats": seats,
                                                     'total_price':total_price,
                                                     'total_nesw_price':total_new_price,
                                                     'ticket_quantity': ticket_quantity,
                                                     'booking_fees':booking_fees,
                                                     'tax':tax,
                                                     'mpaa_rating':mpaa_rating,
                                                     "show_id":show_id,
                                                     'booking_id':code,
                                                     "qr_code":qr_image_base64
                                                     })

def movie_list(request):

    movies = Movie.objects.all().values('title', 'image', 'trailer_url', 'description', 'duration', 'rating')

    movies_list = list(movies)  # convert queryset to list

    return JsonResponse(movies_list, safe=False)
