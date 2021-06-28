from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, UserForm, UserProfileForm
from .models import Account, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from favorites.views import _favorites_id
from favorites.models import Favorites, FavoritesItem
import requests
from django.template.defaultfilters import slugify
from category.models import Category
from store.forms import AssetForm
from store.models import Asset


# Verification Email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            # Creat a user profile at registration
            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_picture = 'default/default-user.png'
            profile.save()

            
            # User Activation
            current_site = get_current_site(request)
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user), 
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering. We have sent a verification email to the email you provided. Please check your email to activate your account.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                favorites = Favorites.objects.get(favorites_id=_favorites_id(request))
                favorites_item_exists = FavoritesItem.objects.filter(favorites=favorites).exists()
                if favorites_item_exists:
                    favorites_item = FavoritesItem.objects.filter(favorites=favorites)

                    for item in favorites_item:
                        item.user = user
                        item.save()
            except:
                pass

            auth.login(request, user)
            messages.success(request, 'Login successful!')
            # Here, we are setting up our url and using the imported requested library
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # Here, we are splitting the query at the = index so that we can use a portion of it to add to the return, this whole bit of code is in a case where a quest user clicks checkout, then is prompted to login and then when they login we want them directed back to their cart page
                params = dict(x.split('=') for x in query.split('&'))

                if 'next' in params:
                    # Here, we are taking the value at the key next (remember, we created a dictionary in the params variable)
                    nextPage = params['next']
                    return redirect(nextPage)

                
            except:
                return redirect('dashboard')

        else:
            messages.error(request, 'Invalid login credentials.')
            return redirect('login')

    
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    request.session.clear()
    messages.success(request, 'Logout Successful!')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        # This will give us the pk of the user
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your Account is active!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('register')

@login_required(login_url='login')
def dashboard(request):
    userprofile = UserProfile.objects.get(user_id=request.user.id)

    context = {
        'userprofile': userprofile,
    }
    return render(request, 'accounts/dashboard.html', context)

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            # __exact checks case sensitive emails that match ones in our database, __iexact would be case insensitive
            user = Account.objects.get(email__exact=email)

            # RESET PASSWORD
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user), 
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email has been sent. Please check your email.')
            return redirect('login')
        else:
            messages.error(request, 'No account found for this email.')
            return redirect('forgotPassword')


    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('resetPassword')

    else:
        messages.error(request, 'This link is expired.')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect ('login')
        else:
            messages.error(request, 'Passwords must match.')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')

@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        # Using instance because we want to update the profile, not create anything new with this form
        user_form = UserForm(request.POST, instance=request.user)

        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid and profile_form.is_valid:
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }

    return render(request, 'accounts/edit_profile.html', context)

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_new_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth logout so they have to log back in
                # auth.logout(request)
                messages.success(request, 'Password update successful!')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password.')
                return redirect('change_password')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('change_password')
        
    return render(request, 'accounts/change_password.html')

@login_required(login_url='login')
def post_asset(request):
    # STORE THE CURRENT PAGE URL
    url = request.META.get('HTTP_REFERER')
    categories = Category.objects.all()
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = AssetForm(request.POST, request.FILES)
        print('Asset Form declare')
        if form.is_valid():
            print('Form valid')
            data = Asset()
            print('Asset declare')
            data.asset_name = form.cleaned_data['asset_name']
            print('Asset name form')
            data.slug = slugify(data.asset_name)
            data.description = form.cleaned_data['description']
            data.price = 0
            print('Asset description form')
            data.images = form.cleaned_data['images']
            print('Asset image form')
            data.category = form.cleaned_data['category']
            print('Asset category form')
            data.user_id = request.user.id
            print('Asset user form')
            data.save()
            print('Asset save')
            messages.success(request, 'Thanks! Your post was submitted.')
            print('success message')
            return redirect(url)
        else:
            messages.error(request, 'Form not valid.')
            return redirect(url)

    context = {
        'userprofile': userprofile,
        'categories': categories,
    }
    return render(request, 'store/post_asset.html', context)

