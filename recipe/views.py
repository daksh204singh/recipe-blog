from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime
from django.forms.models import inlineformset_factory, modelformset_factory
from django.contrib import messages
from recipe.models import Category, Recipe, Comment, userprofile

def index(request):
    rdata=Recipe.objects.order_by('-votes', '-rating')[:20]
    cdata=Category.objects.all()
    recipe_count = Recipe.objects.count()
    user_count = User.objects.count()
    comment_count = Comment.objects.count()
    return render(request, 'recipe/index.html',{'rhead': rdata[:5], 'rdata':rdata,'cdata':cdata, 'rcount': recipe_count, 'usercount': user_count, 'comment_count': comment_count})

def add_recipe(request):
    return render(request,'recipe/add_recipe.html')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        if  User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        elif pass1 != pass2:
            messages.error(request, "Password mismatch!")
        else:
            userRegister = User.objects.create_user(
                    username=username,
                    password=pass1,
                    email=email,
                )
            if userRegister is not None:
                userRegister.save()
                userProfile = userprofile(user = userRegister)
                if userProfile is not None:
                    userProfile.save()
                    login(request, userRegister)
                    return redirect('profile')
            else:
                messages.error(request, "User not Created, Try Again!")

    return render(request = request,
                    template_name = "recipe/signup.html")

def dashboard(request):
    recipes = Recipe.objects.filter(recipe_posted_by=request.user.id).order_by('-recipe_date')
    return render(request, 'recipe/dashboard.html', {'recipes': recipes})

def contact(request):
    return render(request, 'recipe/contact.html')

def about(request):
    return render(request, 'recipe/about.html')

def logout_request(request):
    logout(request)
    return redirect('index')

def login_request(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Invalid username or password!")
    return render(request=request, 
            template_name="recipe/login.html")


def receipedetail(request,id=None):
    recipe=Recipe.objects.get(pk=id)
    comments = Comment.objects.filter(recipe=id).order_by('-create_at')
    recipes = Recipe.objects.filter(recipe_cat=recipe.recipe_cat).exclude(pk=id)
    return render(request, 'recipe/detail.html',{'recipe':  recipe, 'rating_range': range(recipe.rating), 'empty_stars': range(5-recipe.rating), 'comments': comments, 'commentsCount': comments.count(), 'similarRecipes': recipes})

def postrecipe(request):
    if request.method == 'POST':
        recipe_name = request.POST['recipe_name']
        recipe_posted_by = request.user.id
        recipe_des = request.POST['recipe_des']
        recipe_preptime = request.POST['recipe_preptime']
        recipe_cooktime = request.POST['recipe_cooktime']
        recipe_des = request.POST['recipe_des']
        recipe_img1 = request.FILES.get('recipe_img1')
        recipe_img2 = request.FILES.get('recipe_img2')
        recipe_img3 = request.FILES.get('recipe_img3')
        recipe_img4 = request.FILES.get('recipe_img4')
        recipe_servings = request.POST['recipe_servings']
        recipe_cat = request.POST['category']

        data=Recipe(recipe_name=recipe_name,recipe_posted_by=User.objects.get(pk=recipe_posted_by),
               recipe_des=recipe_des,recipe_preptime=recipe_preptime,
               recipe_cooktime=recipe_cooktime,recipe_img1=recipe_img1,recipe_img2=recipe_img2
               ,recipe_img3=recipe_img3,recipe_img4=recipe_img4,recipe_servings=recipe_servings,
               recipe_cat=Category.objects.get(pk=recipe_cat))
        data.save()
        return render(request, 'recipe/post.html',{'success':'Recipe Posted Successfully'})

    else:
        catdata=Category.objects.all();
        return render(request, 'recipe/post.html',{'catdata':catdata})

def recipes(request, category_id):
        rec = Recipe.objects.select_related().filter(recipe_cat=category_id)
        cat = Category.objects.get(pk=category_id).cat_name
        return render(request, 'recipe/recipes.html', {'Recipe': rec, 'category_name': cat})

def search(request):
    search = request.GET['search']
    src = Recipe.objects.filter(recipe_name__icontains=search)
    return render(request, 'recipe/search.html', {'src':src})

def postComment(request):
    if request.method == 'POST':
        comment_subject = request.POST['comment_subject']
        comment_rating = request.POST['rating']
        comment_message = request.POST['message']
        user = request.user.id
        recipe_id = request.POST['recipeId']
        comment = Comment(recipe=Recipe.objects.get(pk=recipe_id), user=User.objects.get(pk=user),
                            subject=comment_subject, message=comment_message, 
                            rate=comment_rating)
        comment.save()
        Recipe.objects.get(pk=recipe_id).update_rating(int(comment_rating))
        return redirect("/recipe/receipedetail/%s/" % recipe_id)

def deleteRecipe(request, recipe_id):
    recipe = Recipe.objects.filter(id=recipe_id).delete()
    return redirect('dashboard')    

def editRecipe(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    catdata = Category.objects.all().exclude(id=recipe.recipe_cat.id);

    if request.method == 'POST':
        recipe_name = request.POST['recipe_name']
        recipe_des = request.POST['recipe_des']
        recipe_preptime = request.POST['recipe_preptime']
        recipe_cooktime = request.POST['recipe_cooktime']
        recipe_img1 = request.FILES.get('recipe_img1')
        recipe_img2 = request.FILES.get('recipe_img2')
        recipe_img3 = request.FILES.get('recipe_img3')
        recipe_img4 = request.FILES.get('recipe_img4')
        recipe_servings = request.POST['recipe_servings']
        recipe_cat = request.POST['category']

        recipe.recipe_name = recipe_name
        recipe.recipe_des = recipe_des
        recipe.recipe_preptime = recipe_preptime
        recipe.recipe_cooktime = recipe_cooktime
        recipe.recipe_servings = recipe_servings
        recipe.recipe_cat = Category.objects.get(pk=recipe_cat)
        if recipe_img1 is not None:
            recipe.recipe_img1 = recipe_img1
        if recipe_img2 is not None:
            recipe.recipe_img2 = recipe_img2
        if recipe_img3 is not None:
            recipe.recipe_img3 = recipe_img3
        if recipe_img4 is not None:
            recipe.recipe_img4 = recipe_img4
        recipe.save()
        return redirect('dashboard')

    else: 
        return render(request, 'recipe/editRecipe.html', {'recipe': recipe, 'catdata': catdata })

def profile_page(request):
    currentUser = request.user
    userProfile = userprofile.objects.get(pk=currentUser)
    
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        phoneNumber = request.POST['phone']
        userCity = request.POST['city']
        userCountry = request.POST['country']
        userBio = request.POST['userBio']
        profilePic = request.FILES.get('profilePic')

        currentUser.first_name = fname
        currentUser.last_name = lname
        currentUser.username = username
        currentUser.email = email
        userProfile.phone = phoneNumber
        userProfile.city = userCity
        userProfile.country = userCountry
        userProfile.bio = userBio
        if profilePic is not None:
            userProfile.profile_pic = profilePic
        
        currentUser.save()
        userProfile.save()

    return render(request, 'recipe/userprofile.html', {'currentUser': currentUser, 'profile': userProfile })

def mycomments(request):
    comments = Comment.objects.filter(user=request.user).order_by('-create_at')
    return render(request, 'recipe/comments.html', {'comments': comments })