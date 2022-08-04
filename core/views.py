from email import message
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from numpy import imag
from requests import delete, request
from core.models import *
from django.contrib.auth.decorators import login_required
from itertools import chain
# Create your views here.

# home page

@login_required(login_url='login')

def index(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=Profile.objects.get(user=user_object)
    #posts=Post.objects.all()
    
    user_following_list = []
    feed = []
    
    user_following=FollowersCount.objects.filter(follower=request.user.username)
    
    for users in user_following:
        user_following_list.append(users.user)
        
    for username in user_following_list:
        feed_list = Post.objects.filter(user=username)
        feed.append(feed_list)
        
    feed_list = list(chain(*feed))
    
    return render(request, "index.html" ,{'user_profile': user_profile ,'posts':feed_list })



@login_required(login_url='login')

def upload(request):
  if request.method ==  "POST":
      user=request.user.username
      image=request.FILES.get('image_upload')
      caption=request.POST['caption']
      
      p=Post()
      p=Post.objects.create(user=user,image=image,caption=caption)
      p.save()
      
      return redirect('/')
  else:
      return redirect("/")
  
  return redirect('/')



#like post


def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    
    post=Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id , username=username ).first()
    
    if like_filter == None :
        new_like=LikePost.objects.create(post_id=post_id , username=username)
        new_like.save()
        post.no_of_likes=post.no_of_likes+1
        post.save()
        
        return redirect('/')
    
    else:
        like_filter.delete()
        post.no_of_likes=post.no_of_likes-1
        post.save()
        
        return redirect('/')
    
    
        
#settings


@login_required(login_url='login')
def settings(request):
    user_profile=Profile.objects.get(user=request.user)
    
    if request.method=="POST":
        if request.FILES.get('image') == None:
            image=user_profile.profile_img
            bio=request.POST['bio']
            location=request.POST['location']
            
            user_profile.profile_img = image
            user_profile.bio= bio
            user_profile.location= location
            user_profile.save()
            
        elif request.FILES.get('image')  != None:
                image=request.FILES.get('image')
                bio=request.POST['bio']
                location=request.POST['location']
                
                user_profile.profile_img = image
                user_profile.bio= bio
                user_profile.location= location
                user_profile.save()
                
                return redirect('settings')
            
    
    return render(request, "setting.html" , {'user_profile': user_profile})


#profile
@login_required(login_url='login')
def profile(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=Profile.objects.get(user=user_object)
    user_post=Post.objects.filter(user=user_object)
    user_post_lenth=len(user_post)
    
    follower = request.user.username
    user=pk
    
    if FollowersCount.objects.filter(follower=follower , user = user).first():
        button_text ='unfollow'
    else:
        button_text="follow"    
        
    
    user_follower= len(FollowersCount.objects.filter(user=pk))
    user_following= len(FollowersCount.objects.filter(follower=pk))
        
    
    context ={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_post':user_post,
        'user_post_lenth':user_post_lenth,
        'button_text':button_text,
        'user_follower':user_follower,
        'user_following':user_following,
    }
    
    return render(request, "profile.html" ,context)


#follow
@login_required(login_url='login')
def follow(request):
    if request.method=="POST":
        follower=request.POST['follower']
        user=request.POST['user']
        
        if FollowersCount.objects.filter(follower=follower , user=user).first():
            delete_user = FollowersCount.objects.get(follower=follower, user=user)
            delete_user.delete()
            
            return redirect('/profile/'+user)
        
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
        
            
            
    else:
        return redirect("/")



# signup


def signup(request):
    if request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "Note: Email Taken!")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                    messages.info(request,"Note: Username Taken!")
                    return redirect('signup')
            else:
                p=User()
                p=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password2)
                messages.info(request,"Note: Successfully Created!")    
                p.save()
                
                #log in to the settings pages
                
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                
                
                #create a profile object for new user
                
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model ,id_user=user_model.id , first_name=user_model.first_name , last_name=user_model.last_name)
                new_profile.save()
                return redirect('settings')
                
            
        else:
            messages.info(request,"Note:Password Not Matched!")
            return redirect ("signup")
        
        
    else:
        return render(request , "signup.html")
    
    
def login(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect("home")
        else:
            messages.info(request,"Credentials Invalid!")
            return redirect("login")
            
    else:
        return render(request,"signin.html")    
    
    
    
def logout(request):
    
    
    auth.logout(request)
    return redirect("login")    