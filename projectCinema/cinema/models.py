from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import random
import string
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator



class User(AbstractUser):
   # Make email, phone_number, first_name, and last_name required
    email = models.EmailField('email address', blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=False, null=False)
    first_name = models.CharField('first name', max_length=150, blank=False, null=False)
    last_name = models.CharField('last name', max_length=150, blank=False, null=False)

    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    receive_promotions = models.BooleanField(default=False)

    CARD_CHOICES = [
        ('Visa', 'Visa'),
        ('MasterCard', 'MasterCard'),
        ('American Express', 'American Express'),
        ('Discover', 'Discover')
    ]

    credit_card_type = models.CharField(max_length=255, null=True, blank=True, choices=CARD_CHOICES, default="")
    credit_card_name = models.CharField(max_length=255, null=True, blank=True, default="")
    credit_card_number = models.CharField(max_length=20, null=True, blank=True, default="")
    credit_card_expiry = models.CharField(max_length=20, null=True, blank=True, default="")
    credit_card_cvv = models.CharField(max_length=4, null=True, blank=True, default="")
    credit_card_address = models.CharField(max_length=255, null=True, blank=True, default="")
    credit_card_city = models.CharField(max_length=255, null=True, blank=True, default="")
    credit_card_state = models.CharField(max_length=255, null=True, blank=True, default="")
    credit_card_zip = models.CharField(max_length=255, null=True, blank=True, default="")

    credit_card_type_2 = models.CharField(max_length=255, null=True, blank=True, choices=CARD_CHOICES)
    credit_card_name_2 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_number_2 = models.CharField(max_length=20, null=True, blank=True)
    credit_card_expiry_2 = models.DateField(null=True, blank=True)
    credit_card_cvv_2 = models.CharField(max_length=4, null=True, blank=True)
    credit_card_address_2 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_city_2 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_state_2 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_zip_2 = models.CharField(max_length=255, null=True, blank=True)

    credit_card_type_3 = models.CharField(max_length=255, null=True, blank=True, choices=CARD_CHOICES)
    credit_card_name_3 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_number_3 = models.CharField(max_length=20, null=True, blank=True)
    credit_card_expiry_3 = models.DateField(null=True, blank=True)
    credit_card_cvv_3 = models.CharField(max_length=4, null=True, blank=True)
    credit_card_address_3 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_city_3 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_state_3 = models.CharField(max_length=255, null=True, blank=True)
    credit_card_zip_3 = models.CharField(max_length=255, null=True, blank=True)

class Movie(models.Model):
    MPAA_RATING_CHOICES = [
        ('G', 'General Audiences'),
        ('PG', 'Parental Guidance Suggested'),
        ('PG-13', 'Parents Strongly Cautioned'),
        ('R', 'Restricted'),
        ('NC-17', 'No One 17 and Under Admitted'),
        ('NR', 'Not Rated')
    ]

    GENRE_CHOICES = [
        ('none', 'None'), 
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('sci-fi', 'Science Fiction'),
    ]
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100, default='N/A')
    cast = models.CharField(max_length=1000, default='N/A')
    producer = models.CharField(max_length=100, default='N/A')
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()  # Duration in minutes
    trailer_url = models.URLField(blank=True)
    # image = models.ImageField(upload_to='img/movie_images/', null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    genre = models.CharField(max_length=100, default='none')
    rating = models.CharField(max_length=5, choices=MPAA_RATING_CHOICES, default='NR')
    star_rating = models.FloatField(
        validators=[
            MinValueValidator(0.0),  # Minimum value is 0.0
            MaxValueValidator(10.0)  # Maximum value is 10.0
        ],
        default=5.0  # Default value is 5.0
    )
    def __str__(self):
        return self.title

class Screen(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    def __str__(self):
        return self.name
    
class ShowBuilder:
    def __init__(self, movie, screen):
        self.movie = movie
        self.screen = screen
        self.start_time = None
        self.end_time = None
        self.price = None

    def set_show_time(self, start_time, duration):
        self.start_time = start_time
        self.end_time = start_time + timedelta(minutes=duration)
        return self

    def set_price(self, price):
        self.price = price
        return self

    def build(self):
        if not all([self.start_time, self.end_time, self.price]):
            raise ValueError("Incomplete show details provided.")
        overlapping_shows = Show.objects.filter(
            screen=self.screen,
            start_time__lt=self.end_time + timedelta(hours=1),
            end_time__gt=self.start_time
        )
        if overlapping_shows.exists():
            raise ValidationError('Another show is scheduled for this screen within 1 hour of this show\'s end time.')
        return Show.objects.create(
            movie=self.movie,
            screen=self.screen,
            start_time=self.start_time,
            end_time=self.end_time,
            price=self.price
        )
    
class Show(models.Model):
    show_id = models.CharField(max_length=10, unique=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    def __str__(self):
        return f"ID: {self.show_id} {self.movie.title} on Screen {self.screen} at {self.start_time}"
        # return self.show_id
    def clean(self):
        overlapping_shows = Show.objects.filter(
            screen=self.screen,
            start_time__lt=self.end_time + timedelta(hours=1),
            end_time__gt=self.end_time
        ).exclude(pk=self.pk)
        
        if overlapping_shows.exists():
            raise ValidationError('Another show is scheduled for this screen within 1 hour of this show\'s end time.')
        
class Seat(models.Model):
    # show_id = models.ForeignKey(Show, on_delete=models.CASCADE) #Added now
    show_id = models.CharField(max_length=10)
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)
    row = models.CharField(max_length=1)  # A, B, C, ...
    number = models.IntegerField()
    is_booked = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.screen} - row {self.row}"

# class Booking(models.Model):
#     STATUS_CHOICES = [
#         ('Pending', 'Pending'),
#         ('Confirmed', 'Confirmed'),
#         ('Cancelled', 'Cancelled'),
#     ]
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     show = models.ForeignKey(Show, on_delete=models.CASCADE)
#     booking_time = models.DateTimeField(auto_now_add=True)
#     total_amount = models.DecimalField(max_digits=8, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES)
#     def __str__(self):
#         return self.user

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # show = models.ForeignKey(Show, on_delete=models.CASCADE)
    show = models.CharField(max_length=2000, default=None)
    booking_time = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    booking_id = models.CharField(max_length=8, unique=True)
    seats = models.CharField(max_length=2000, default=None)


    def __str__(self):
        return f"Booking ID: {self.booking_id}, User: {self.user.username}"

    # def save(self, *args, **kwargs):
    #     # Generate a random booking ID
    #     self.booking_id = ''.join(random.choices(string.digits, k=5))
    #     super().save(*args, **kwargs)

class PromoCode(models.Model):
    DISCOUNT_CHOICES = [
        ('Percentage', 'Percentage'),
        ('Fixed Amount', 'Fixed Amount'),
    ]
    code = models.CharField(max_length=20, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES)
    discount_value = models.DecimalField(max_digits=8, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_usage_count = models.IntegerField()
    current_usage_count = models.IntegerField(default=0)
    def __str__(self):
        return self.code

class PromoCodeUsage(models.Model):
    promo_code = models.ForeignKey(PromoCode, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    def __str__(self):
        return self.promo_code