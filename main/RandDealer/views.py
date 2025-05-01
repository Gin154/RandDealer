from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import *
from django.core.mail import send_mail
from random import randrange
from .models import *
from django.core.mail import EmailMessage
from django.urls import reverse

#homepage
def index(request):
    return render(request, 'home.html')
#base (header, footer)
def base(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

#contact page send e-mail
def contact(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        sender = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        email = EmailMessage(
            subject,
            message,
            f"Contact Form <{sender}>",
            ["randdealer@gmail.com"],
            reply_to=[sender],
        )

        #send the email
        email.send(fail_silently=False)
    return render(request, 'contact.html')

#Sell form to add car
def sell(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to be logged in to sell a car')
        return render(request, 'login.html')
    
    car_form = CarRegistrationForm()
    if request.method == 'POST':
        car_form = CarRegistrationForm(request.POST)
        
        if car_form.is_valid():
            user = request.user
            car = car_form.save(commit=False)
            car.owner = user
            car.save()
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

#Car list
def buy(request):
    cars = Cars.objects.prefetch_related('images').all()
    context = {'cars': cars}
    return render(request, 'carlist.html', context)

#Go to login page
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
    
    #reads messages (to "delete" them)
    else:
        storage = messages.get_messages(request)
        for i in storage:
            pass
        return render(request, 'login.html')

#signs out the user
def signout(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return render(request, 'login.html')


#old signup function, replaced by the 'confirmuser' function
"""
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

#open car page with it's information
def car(request, id):
    car = (
    Cars.objects
    .select_related('owner')
    .prefetch_related('images')
    .get(id=id)
    )

    context = {'car': car}
    return render(request, 'car.html', context)

#test page
def test(request):
    car = Cars.objects.prefetch_related('images').get(id=4)
    return render(request, 'tests.html', {'car': car})

#confirm user after signup
def registeruser(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        #perform validation
        if not username:
            messages.error(request, 'Username is required')
        if not email:
            messages.error(request, 'Email is required')
        if not password1:
            messages.error(request, 'Password is required')
        if password1 != password2:
            messages.error(request, 'Passwords do not match')

        if not any(message for message in messages.get_messages(request)):
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
        
        if not any(message for message in messages.get_messages(request)):
            user = User.objects.create(
                username=username,
                email=email,
                is_active=False
                )
            user.set_password(password1)
            user.save()
            
            confirmation = EmailVerificationToken.objects.create(user=user)

            #build verification URL
            verification_url = request.build_absolute_uri(
                reverse('verifyemail', kwargs={'token': str(confirmation.token)})
            )

            #send verification email
            send_mail(
                subject='Verify Your Email',
                message=f'Click to verify your account: {verification_url}',
                from_email='noreply@example.com',
                recipient_list=[email],
                fail_silently=False,
                html_message=f'''
                    <h1>Welcome to our site!</h1>
                    <p>Please <a href="{verification_url}">click here</a> to verify your email.</p>
                    <p>The link expires in 24 hours.</p>
                '''
            )

            messages.success(request, 'Registration successful! Please check your email to verify your account.')
            return redirect(signin)
        #in case of an issue, check if the user is verified, if not, delete
        else:
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    user.delete()
                    EmailVerificationToken.objects.filter(user=user).delete()
                    
            except User.DoesNotExist:
                pass
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return render(request, 'afterregister.html')
            
            return render(request, 'afterregister.html')

    return redirect(index)

def afterregister(request):
    return render(request, 'afterregister.html')

#user clicks e-mail link:
def verifyemail(request, token):
    try:
        token_obj = EmailVerificationToken.objects.get(token=token)

        if token_obj.is_expired():
            messages.error(request, 'The verification link has expired. Please register again.')
            token_obj.user.delete()
            return redirect('signin')

        if token_obj.is_verified:
            messages.info(request, 'This email has already been verified.')
        else:
            token_obj.is_verified = True
            token_obj.save()
            token_obj.user.is_active = True
            token_obj.user.save()
            messages.success(request, 'Email successfully verified! You can now log in.')

        return redirect('signin')

    except EmailVerificationToken.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('registeruser')


def profile(request):
    try:
        user = User.objects.select_related('userprofile').get(pk=request.user.pk)
        cars = user.cars.all().prefetch_related('images')
        edit=True
        context = {
        'cars': cars,
        'user': user,
        'edit': edit
        }
        return render(request, 'profile/profile.html', context)
    except:
        messages.error(request, f"You need to be logged in to access your profile")
        return render(request, 'login.html')
    

def editprofileinfo(request):
    try:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user = request.user

        if request.method == 'POST':
            form = ProfilePictureForm(request.POST, request.FILES, instance=user_profile)
            if form.is_valid():
                form.save()

        if request.method =='POST':
            form = AddUserInfo(request.POST, instance=user)
            if form.is_valid():
                form.save()
        
        
        formpic = ProfilePictureForm(instance=user_profile)
        forminfo = AddUserInfo(instance=user)
                
        return render(request, 'profile/editprofileinfo.html', {'formpic': formpic, 'forminfo':forminfo})
    except Exception as e:
        messages.error(request, f"{e}")
        return render(request, 'error.html')