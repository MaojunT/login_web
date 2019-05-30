# login/views.py
 
from django.shortcuts import render, redirect, HttpResponse
from . import models
from .forms import UserForm, RegisterForm, UpdateEmailForm, UpdatePwdForm
#import hashlib
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.conf import settings
import json
from django.core.mail import EmailMessage
from smtplib import SMTPException

def send_email(request):
    email_title = 'Crypto'
    body = ""
    for user in User.objects.all():
        email_body = email_list(request)

        #send_mail(email_title, email_body, EMAIL_FROM, [user.email])
        email = EmailMessage(email_title, email_body, to=[user.email])
        email.send()

 
def index(request):
    if request.method=="POST":
        check_box_list = request.POST.getlist('cb')
        #print(check_box_list)
        if check_box_list:
            #print(check_box_list)
            u = request.user
            c = check_box_list
            models.UserChoice.objects.filter(username=u).delete()
            models.UserChoice.objects.create(username=u, choice_1 = c)
            return redirect("/index_2/")
        else:
            print("fail")
            return HttpResponse("fail")
    else:
        return render(request,'login/index.html')

def index_2(request):
    if request.method=="POST":
        check_box_list = request.POST.getlist('cb')
        #print(check_box_list)
        if check_box_list:
            #print(check_box_list)
            u = request.user
            c = check_box_list
            models.UserChoice.objects.filter(username=u).update(choice_2 = c)
            return redirect("/index_3/")
        else:
            print("fail")
            return HttpResponse("fail")
    else:
        a = get_coinbase()
        return render(request,'login/index_2.html',{'a':a})

def index_3(request):
    if request.method=="POST":
        check_box_list = request.POST.getlist('cb')
        #print(check_box_list)
        if check_box_list:
            #print(check_box_list)
            u = request.user
            c = check_box_list
            models.UserChoice.objects.filter(username=u).update(choice_3 = c)
            send_email(request)
            return HttpResponse("successful")
        else:
            print("fail")
            return HttpResponse("fail")
    else:
        a = get_coinbase_measures()
        return render(request,'login/index_3.html',{'a':a})

def email_list(request):
    u = request.user
    a = models.UserChoice.objects.get(username=u)
    user_token = a.choice_2
    new = "" 
    ut = []

    for x in user_token:
        if x != '[' and x != "'" and x!= ','and x != ' ' and x != ']':
            new += x
        if x == ',' or x == ']':
            ut.append(new)
            new = ""

    user_measure = a.choice_3
    um = []
    for x in user_measure:
        if x != '[' and x != "'" and x!= ','and x != ' ' and x != ']':
            new += x
            #print (x)
        if x == ',' or x == ']':
            um.append(new)
            new = ""


    with open('Coinbase.json') as json_file:
        data = json.load(json_file)

    elist = []
    for token in ut:
        for measure in um:
            m = data[token][0][measure]
            if m == 1 or m == 'true':
                if "||" + token + "-------"  not in elist:
                    elist.append("||" + token + "-------")
                elist.append(measure + " ")
    #elist = list(dict.fromkeys(elist))

    estring = "".join(map(str, elist))
    print (estring)
    return estring


def get_coinbase():
    with open('Coinbase.json') as json_file:
        data = json.load(json_file)
    token_list = list(data.keys())
    return token_list

def get_coinbase_measures():
    with open('Coinbase.json') as json_file:
        data = json.load(json_file)
    key = list(data.keys())[0]
    measure_list = list(data[key][0].keys())
    return measure_list
 
def login_view(request):
    if request.session.get('is_login',None):
        return redirect('/index')
 
    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "Error!"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                request.session['is_login'] = True
                login(request, user)
                return redirect("/index/")
            else:
                message = "Incorrect username or password!"
                return render(request, 'login/login.html', locals())
 
    login_form = UserForm()
    return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Error!"
        if register_form.is_valid(): 
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:
                message = "Please make sure the passwords you entered are the same!"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = User.objects.filter(username=username)
                if same_name_user:
                    message = 'user already exists'
                    return render(request, 'login/register.html', locals())
                same_email_user = User.objects.filter(email=email)
                if same_email_user:
                    message = 'email already exits'
                    return render(request, 'login/register.html', locals())
 
                #register a new user
                user = User.objects.create_user(username, email, password1)
                user.save()
                #new_user = models.User.objects.create()
                #new_user.name = username
                #new_user.password = hash_code(password1)
                #new_user.email = email
                #new_user.save()
                return redirect('/login/')
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())
 

def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/index/")
    request.session.flush()
    # or
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/index/")


#def hash_code(s, salt='mysite_login'):
#    h = hashlib.sha256()
#    s += salt
#    h.update(s.encode())
#    return h.hexdigest()

def profile(request):
    u = request.user
    uc = models.UserChoice.objects.get(username=u)
    UserChoice_1 = uc.choice_1
    UserChoice_2 = uc.choice_2
    UserChoice_3 = uc.choice_3
    return render(request,'login/profile.html', locals())


def profile_update(request):
    if request.POST:
        update_form = UpdateEmailForm(request.POST, instance=request.user)
        if update_form.is_valid():
            update_form.save()
            message = "Update email successful"
            return render(request, 'login/profile.html', locals())

    update_form = UpdateEmailForm()
    return render(request, 'login/profile_update.html', locals())

def pwd_update(request):
    if request.method=="POST":
        update_form = UpdatePwdForm(request.POST)
        message = "Error!"
        username = request.user.username
        oldpwd = request.POST.get('oldpwd', '')
        user = authenticate(username=username, password=oldpwd)
        if user is not None and user.is_active:
            newpwd = request.POST.get('newpwd', '')
            cfmpwd = request.POST.get('cfmpwd', '')
            if newpwd != cfmpwd:
                message = "Please make sure the passwords you entered are the same!"
                return render(request, 'login/pwd_update.html', locals())
            else:
                message = "Change password successful, please use your new password to login"
                user.set_password(newpwd)
                user.save()
                return render(request, 'login/profile.html', locals())
        else:
            message = "Please make sure you entered the correct password"
            return render(request, 'login/pwd_update.html', locals())
    update_form = UpdatePwdForm()
    return render(request, 'login/pwd_update.html', locals())
