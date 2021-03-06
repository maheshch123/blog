from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from blog.models import Post
from .models import Profile
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'users/profile.html', context)


def userprofile(request, username):
    user = User.objects.filter(username=username)
    if user:
        user = user[0]
        posts = Post.objects.filter(author=user).order_by('-date_posted')
        profile = Profile.objects.get(user=user)
        image = profile.image
        address = profile.address
        cover_pic = profile.cover_pic
        context = {
            'user_obj':user,
            'image':image,
            'address':address,
            'cover_pic':cover_pic,
            'posts':posts,
        }
    else:
        return HttpResponse("No such user")
    return render(request,'users/userprofile.html',context)
