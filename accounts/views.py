from django.shortcuts import render, redirect
from .forms import RegisterationForm
from .models import User
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# USER ACTIVATION

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def activate(request, uidb64, token):
    try:
      uid = urlsafe_base64_decode(uidb64).decode()
      user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('accounts:activation_complete')
    else:
        return render(request, 'accounts/activation_complete.html', {'invalid': True,})
        # return redirect('accounts:register')

@login_required
def activation_complete(request):
    return render(request, 'accounts/activation_complete.html')

@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def register(request):
    if request.method == 'POST':
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            try:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password
                )
                user.phone_number = phone_number
                user.save()

                # USER ACTIVATION

                current_site = get_current_site(request)
                mail_subject = 'Please activate your account'
                message = render_to_string('accounts/activation.html', {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                messages.success(request, "✅ User created successfully")
                # return redirect('accounts:activate_message')
                return redirect('/accounts/login/?command=verification&email='+email)

            except Exception as e:
                messages.error(request, f"❌ Error creating user: {str(e)}")
        else:
            messages.error(request, "❌ Error creating user")
    else:
        form = RegisterationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
    })

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Wrong Credentials')
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('accounts:login')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email = email).exists():
            user = User.objects.get(email__exact = email)

            current_site = get_current_site(request)
            mail_subject = "Click the link to Change your password"
            message = render_to_string('accounts/reset_password_validate.html',{
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Password reset email has been sent to your email address!")

        else:
            messages.error(request, "Account does not exist")

    return render(request, 'accounts/forget_password.html')


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        return redirect('accounts:reset_password')
    else:
        messages.error(request, "This link has been expired")
        return redirect('accounts:login')

def reset_password(request):
    if request.method == 'POST':
        password= request.POST.get('password')
        confirm_password= request.POST.get('confirm_password')

        if password == confirm_password:
            uid = request.session.get('uid')
            user = User.objects.get(pk=uid)
            if not user.check_password(password):
                user.set_password(password)
                user.save()
                messages.success(request, 'Your password has been reset')
                return redirect('accounts:login')
            else:
                messages.error(request, 'This is your old password')
                return redirect('accounts:reset_password')
        else:
            messages.error(request, 'Password does not match')
            return redirect('accounts:reset_password')
    return render(request, 'accounts/reset_password.html')