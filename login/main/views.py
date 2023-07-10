from datetime import datetime
from typing import Any
from django import http
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from main.decorators import  unauthenticated_user, allowed_users
from main.forms import CourseSearchForm, CreateUserForm, LoginForm, CourseCreationForm
from django.contrib.auth import authenticate, login, logout
from main.models import Courses, Profile, PublishRequest
from main.tokens import generate_token
from .filters import CourseFilter
from django.views import View
from django.views.generic import DetailView
# Create your views here.
def index(request):
    courses = Courses.objects.all()
    
    return render(request, 'main/index.html', {"courses": courses})


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'), email=form.cleaned_data.get('email'), first_name=form.cleaned_data.get('first_name'), last_name=form.cleaned_data.get('last_name'))
            messages.success(request, 'Account was created for ' + form.cleaned_data.get('username') + ". Please confirm your email!")
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Confirm'
            message2 = render_to_string('email_confirmation.html', {'name': user.first_name, 'domain': current_site.domain, 'uid': urlsafe_base64_encode(force_bytes(user.pk)), 'token': generate_token.make_token(user)})
            email = EmailMessage(
                email_subject,
                message2,
                to=[user.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'main/registration.html', {'form': form})


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'main/login.html')
    form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


class LoginPageView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'main/login.html', {'form': form})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return render(request, 'main/login.html')
    

def logoutUser(request):
    logout(request)
    return redirect('home')

class LogoutUserView(View):
    def get(self, request):
        logout(request)
        return redirect('home')



def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your confirmation. Now you can login.')
    else:
        return render(request, 'activation_failed.html')


@allowed_users(allowed_roles=['Admins'])
def adminPage(request):
    users = User.objects.all()
    courses = Courses.objects.all()
    requests = PublishRequest.objects.all()
    return render(request, 'main/admin.html', {'users': users, 'courses': courses, 'requests': requests})


def edit(request, pk):
    user = User.objects.get(id=pk)
    form = CreateUserForm(instance=user)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.password1 = request.POST.get('password1')
        user.password2 = request.POST.get('password2')
        user.save()
        return redirect('home')
    return render(request, 'main/registration.html', {'form': form})


@allowed_users(allowed_roles=['Admins'])
def details(request, pk):
    user = User.objects.get(id=pk)
    return render(request, 'main/details.html', {'user': user})


def delete(request, pk):
    user = User.objects.get(id=pk)
    user.delete()
    return redirect('admin')



def course_details(request, pk):
    course = Courses.objects.get(id=pk)
    course.last_viewed = datetime.now()
    course.save()
    last_viewed_items = request.session.get('last_viewed_items', [])
    if pk not in last_viewed_items:
        last_viewed_items.append(pk)
        request.session['last_viewed_items'] = last_viewed_items
    
    return render(request, 'main/course-details.html', {'course': course})


def create_course(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES)
        if form.is_valid():
            course = Courses.objects.create(title=form.cleaned_data.get('title'), description=form.cleaned_data.get('description'), price=form.cleaned_data.get('price'), image=form.cleaned_data.get('image'), author=form.cleaned_data.get('author'), published=False)
            if request.user.is_staff:
                course.published = True
                course.save()
            else:
                PublishRequest.objects.create(course=course, user=request.user)
            last_viewed_items = request.session.get('last_viewed_items', [])
            last_viewed_items.append({
                'title': course.title,
                'salary': course.price
            })
            request.session['last_viewed_items'] = last_viewed_items
            return redirect('courses')
        
    else:
        form = CourseCreationForm()
    return render(request, 'main/create-course.html', {'form': form})




@allowed_users(allowed_roles=['Admins'])
def course_delete(request, pk):
    course = Courses.objects.get(id=pk)
    course.delete()
    return redirect('admin')


@allowed_users(allowed_roles=['Admins'])
def course_update(request, pk):
    course = Courses.objects.get(id=pk)
    form = CourseCreationForm(request.POST or None, request.FILES or None, instance=course)
    if form.is_valid():
        form.save()
        return redirect('admin')
    return render(request, 'main/create-course.html', {'form': form})


def course_list(request):
    title_query = request.GET.get('title')
    author_query = request.GET.get('author')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    published_only = request.GET.get('published_only')
    courses = Courses.objects.all()
    if title_query:
        courses = courses.filter(title__icontains=title_query)
    if author_query:
        courses = courses.filter(author__icontains=author_query)
    if price_min:
        courses = courses.filter(price__gte=float(price_min))
    if price_max:
        courses = courses.filter(price__lte=float(price_max))
    if published_only:
        courses = courses.filter(published=True)
    form = CourseSearchForm()
    return render(request, 'main/course-list.html', {'courses': courses, 'form': form})
    
@allowed_users(allowed_roles=['Admins', 'Clients'])
def profile_page(request, pk):
    user = User.objects.get(id=pk)
    last_viewed_items = request.session.get('last_viewed_items', [])
    courses = Courses.objects.filter(id__in=last_viewed_items)

    return render(request, 'main/profile-page.html', {'user': user, 'courses': courses})


class ProfilePageView(DetailView):
    model = User
    template_name = 'main/profile-page.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_viewed_items = self.request.session.get('last_viewed_items', [])
        courses = Courses.objects.filter(id__in=last_viewed_items)
        context['courses'] = courses
        return context


@allowed_users(allowed_roles=['Admins'])
def accept_request(request, request_id):
    publish_request = PublishRequest.objects.get(pk=request_id)
    publish_request.approved = True
    publish_request.course.published = True
    publish_request.course.save()
    publish_request.delete()
    
    return redirect('admin')

@allowed_users(allowed_roles=['Admins'])
def reject_request(request, request_id):
    publish_request = PublishRequest.objects.get(pk=request_id)
    publish_request.course.delete()
    publish_request.delete()
    
    return redirect('admin')

def search(request):
    title_query = request.GET.get('title')
    author_query = request.GET.get('author')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    published_only = request.GET.get('published_only')
    courses = Courses.objects.all()
    if title_query:
        courses = courses.filter(title__icontains=title_query)
    if author_query:
        courses = courses.filter(author__icontains=author_query)
    if price_min:
        courses = courses.filter(price__gte=float(price_min))
    if price_max:
        courses = courses.filter(price__lte=float(price_max))
    if published_only:
        courses = courses.filter(published=True)

    return render(request, 'main/search.html', {'courses': courses})