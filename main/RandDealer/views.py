from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from django.core.mail import send_mail
from random import randrange
from .models import *
from django.core.mail import EmailMessage

# Create your views here.
def index(request):
    return render(request, 'home.html')

def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        sender = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        # Create an EmailMessage object
        email = EmailMessage(
            subject,
            message,
            f"Contact Form <{sender}>",  # Set the "From" header to the user's email
            ["randdealer@gmail.com"],    # Your email address
            reply_to=[sender],           # Set the "Reply-To" header to the user's email
        )

        # Send the email
        email.send(fail_silently=False)
    return render(request, 'contact.html')

def sell(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to sell a car')
        return render(request, 'login.html')
    
    car_form = CarRegistrationForm()
    if request.method == 'POST':
        car_form = CarRegistrationForm(request.POST)
        
        if car_form.is_valid():
            car_form.save()
            images = request.FILES.getlist('images')
            for image in images:
                CarImage.objects.create(car=car_form.instance, image=image)

            messages.success(request, 'Car registered successfully')
            return render(request, 'regcar.html')


        else:
            messages.error(request, 'Error registering car')
            return render(request, 'regcar.html')
        
    context = {'car_form': car_form}
    return render(request, 'regcar.html', context)

def buy(request):
    cars = Cars.objects.prefetch_related('images').all()
    context = {'cars': cars}
    return render(request, 'carlist.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    else:
        storage = messages.get_messages(request)
        for _ in storage:
            pass 
        return render(request, 'login.html')

def signout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return render(request, 'login.html')

"""
Old signup method, replaced by the confirm user method
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'signup.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        messages.success(request, 'Signup successful')
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')
        
"""
    
def car(request, id):
    car = Cars.objects.prefetch_related('images').get(id=id)
    context = {'car': car}
    return render(request, 'car.html', context)

def test(request):
    car = Cars.objects.prefetch_related('images').get(id=4)
    return render(request, 'tests.html', {'car': car})


def confirmuser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'login.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'login.html')
        
        code = randrange(100000, 999999)
        userconfirmation.objects.create(username=username, email=email, code=code)
        send_mail(
            'Confirmation Code',
            'Your confirmation code is: ' + str(code),
            'randdealer@gmail.com',
            [email],
            fail_silently=False
            )
        context = {'username': username, 'email': email, 'code': code}
        return render(request, 'confirmuser.html', context)
    
    context = {'username': 'teste', 'email': 'teste@gmail.com', 'code': '123456'}
    return render(request, 'confirmuser.html', context)

def userconfirmed(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        code = request.POST['code']
        context = {'username': username, 'email': email, 'code': code}
        if userconfirmation.objects.filter(username=username, email=email, code=code).exists():
            context['confirmed'] = True
            return render(request, 'confirmuser.html', context)
        else:
            context['confirmed'] = False
            messages.error(request, 'Invalid code')
            return render(request, 'confirmuser.html', context)
    return render(request, 'confirmuser.html')

def setpassword(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Password set successfully for ' + username + '. You can now login') 
        return render(request, 'login.html')
    
    return render(request, 'setpassword.html')