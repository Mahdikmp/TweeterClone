from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Tweet
from django.contrib import messages
from .forms import TweetForm, RegisterForm, EditProfileForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User



def home(request):
    if request.user.is_authenticated:
        tweets = Tweet.objects.all().order_by('-created')
        form = TweetForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid:
                tweeted = form.save(commit=False)
                tweeted.user = request.user
                tweeted.save()
                messages.success(request, 'Your tweet has been posted successfully!')
                return redirect('home')
        return render(request, 'home.html', {'tweets':tweets, 'form': form})
    else:
        tweets = Tweet.objects.all().order_by('-created')
        return render(request, 'home.html', {'tweets':tweets})



def profiles(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profiles.html', {'profiles': profiles})
    else:
        messages.error(request, ('You should login first ...'))
        return redirect('home')
    


def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by('-created')

        currentUser = request.user.profile
        
        if request.method == 'POST':
            action = request.POST['follow']
            if action == 'follow':
                currentUser.follows.add(profile)
            elif action == 'unfollow':
                currentUser.follows.remove(profile)

        return render(request, 'profile.html', {'profile': profile, 'tweets': tweets})
    else:
        messages.error(request, ('You should login first ...'))
        return redirect('home')
    


def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong! Please try again!')
            return redirect('home')
    else:
        return render(request, 'login.html')
    


def userLogout(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('home')



def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You are registered successfully! Now login...')
            return redirect('login')
        else:
            messages.error(request, 'Something went wrong! try again...')
            return redirect('register')
        
    return render(request, 'register.html', {'form': form})



def userUpdate(request):
    if request.user.is_authenticated:
        currentUser = User.objects.get(id = request.user.id)
        profileUser = Profile.objects.get(user__id = request.user.id)
        user_form = EditProfileForm(instance=currentUser)
        profile_form = ProfilePicForm(instance=profileUser)
        if request.method == 'POST':
            user_form = EditProfileForm(request.POST or None, request.FILES or None, instance = currentUser)
            profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance = profileUser)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile has been updated!')
                return redirect('home')
        return render(request, 'userupdate.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        messages.error(request, 'You must login first!')
        return redirect('home')
    


def tweet_like(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'You should login first ...')
        return redirect('home')
    


def tweet_detail(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    if tweet:
        return render(request, 't_detail.html', {'tweet': tweet})
    else:
        messages.error(request, 'Sorry, this tweet does not exist!')
        return redirect('home')