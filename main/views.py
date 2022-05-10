from django.shortcuts import  render, redirect, get_object_or_404
from .forms import NewUserForm
from .forms import RateMoviesForm
from .forms import CommentForm
from .models import Rating
from .models import Movie
from .models import Comment

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib import messages

# Create your views here.
def homepage(request):
	all_movies = Movie.objects.all()
	return render(request=request, template_name='main/home.html', context={'all_movies': all_movies})


def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("main:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="main/register.html", context={"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("main:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="main/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("main:homepage")


def rating_request(request):
	if request.method == "POST":
		form = RateMoviesForm(request.POST)
		if form.is_valid():
			user = request.user.username
			useremail = request.user.email
			messages.success(request, "Voting successful." )

			#if the user has already voted, we just want to update
			if Rating.objects.filter(username = user).exists():
				vote=Rating.objects.filter(username = user).update(email=useremail,\
					Movie_1 = int(form.cleaned_data['movie1']), Movie_2 = int(form.cleaned_data['movie2']), Movie_3 = int(form.cleaned_data['movie3']),\
					Movie_4 = int(form.cleaned_data['movie4']), Movie_5 = int(form.cleaned_data['movie5']), Movie_6 = int(form.cleaned_data['movie6']),\
					Movie_7 = int(form.cleaned_data['movie7']), Movie_8 = int(form.cleaned_data['movie8']), Movie_9 = int(form.cleaned_data['movie9']), \
					Movie_10 =int(form.cleaned_data['movie10']))
			#if user has not voted, we want to create
			else:
				vote=Rating.objects.create(username=user,email=useremail,\
					Movie_1 = int(form.cleaned_data['movie1']), Movie_2 = int(form.cleaned_data['movie2']), Movie_3 = int(form.cleaned_data['movie3']),\
					Movie_4 = int(form.cleaned_data['movie4']), Movie_5 = int(form.cleaned_data['movie5']), Movie_6 = int(form.cleaned_data['movie6']),\
					Movie_7 = int(form.cleaned_data['movie7']), Movie_8 = int(form.cleaned_data['movie8']), Movie_9 = int(form.cleaned_data['movie9']), \
					Movie_10 =int(form.cleaned_data['movie10']))

			return redirect("main:recommendation")
		messages.error(request, "Unsuccessful survey info. Try again.")
	form = RateMoviesForm()
	return render (request=request, template_name="main/rating.html", context={"rating_form":form})

def movie_detail(request, id):
    movie =  Movie.objects.filter(id=id).first()
    comments = movie.comments
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
       
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie_id = movie
            new_comment.user = request.user
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    return render(request=request, template_name='main/movie.html', context={"movie": movie, 'comments': comments, 'new_comment': new_comment,'comment_form': comment_form})

def recommendation_request(request):
	user = request.user.username
	soulmate, cosine_similarity = Movie_Soul_Mate(user)
	movie_rec = Recommendation2(user)
	soulmate_email = Rating.objects.filter(username = soulmate).first().email
    
	details  ={
		'soulmate' : soulmate,
		'cosine' : cosine_similarity,
		'movie_rec': movie_rec,
        'soulmate_email' : soulmate_email,
	}
	return render(request = request, template_name = 'main/recommendation.html', context = details)


def read_in_movie_preference():
	preference = {}
	movies = []
	
	#iterate through the ratings and add to preference dictionary
	for item in Rating.objects.all():
		user = item.username
		prefArray = []
		prefArray.append(item.Movie_1)
		prefArray.append(item.Movie_2)
		prefArray.append(item.Movie_3)
		prefArray.append(item.Movie_4)
		prefArray.append(item.Movie_5)
		prefArray.append(item.Movie_6)
		prefArray.append(item.Movie_7)
		prefArray.append(item.Movie_8)
		prefArray.append(item.Movie_9)
		prefArray.append(item.Movie_10)

		preference[user] = prefArray

	#read in movie names
	for mov in Movie.objects.all():
		movies.append (mov.title)

	return [movies,preference]


def movies_popularity_ranking():
    movie_popularity = {}
    movie_popularity_rank = []
    total_likes = 0
    total_dislikes = 0
    
    # read in using previous function
    [movies, preference] = read_in_movie_preference()
    
    #initialize array of a spcific movies likes and dislikes
    movie_likes = [0]*len(movies)
    movie_dislikes = [0]*len(movies)
    
    #check likes and dislikes for each movie for each person and update corresponding list
    for person in preference.keys():
        for i in range(len(preference[person])):
            if preference[person][i] == 1:
                total_likes += 1
                movie_likes[i] += 1
            elif preference[person][i] == -1:
                total_dislikes += 1
                movie_dislikes[i] += 1
                
    #go through each movie, calculate popularity, and update movie popularity dictionary
    for i in range(len(movies)):
        popularity = movie_likes[i] - total_likes / total_dislikes * movie_dislikes[i]
        movie_popularity[movies[i]] = popularity
        
    # sort the dictionary based on popularity, store it as a list, and return everything
    sorted_dict = dict(sorted(movie_popularity.items(), key=lambda item: item[1], reverse = True))
    movie_popularity_rank = list(sorted_dict.keys())
    return movie_popularity, movie_popularity_rank, total_likes, total_dislikes


def Recommendation(name):
    
    
    recommended_movie = ""
    # YOUR CODE HERE
    #initialize stuff
    [movies, preference] = read_in_movie_preference()
    movie_popularity, movie_popularity_rank, total_likes, total_dislikes = movies_popularity_ranking()
    
    movie_watched = [False]*len(movies)
    count_watched = 0
    total_popularity = 0
    current_max_popularity = -100000000
    
    #check if valid user
    if name not in preference:
        return 'Invalid user.'
    
    #check if watched a movie
    watched_all = True
    for i in range(len(preference[name])):
        #if they havent watched
        if preference[name][i] == 0:
            watched_all = False    
            popularity = movie_popularity[movies[i]]
            #if current movie is better than current max movie
            if popularity > current_max_popularity:
                current_max_popularity = popularity
                recommended_movie = movies[i]
                
        #if they have watched
        else:
            movie_watched[i] = True
            count_watched += 1
            popularity = movie_popularity[movies[i]]
            total_popularity +=  popularity
            
    average_popularity = total_popularity / count_watched
            
    #if user watched all movies or there are no more movies to watch that are more popular than average 
    if watched_all or current_max_popularity < average_popularity:
        return 'Unfortunately, no new movies for you.'
    
    return recommended_movie


def Similarity(name_1, name_2):
    """Given two names and preference, get the similarity 
    between two people"""
    cosine = 0
    
    # YOUR CODE HERE
    [movies, preference] = read_in_movie_preference()
    movie_popularity, movie_popularity_rank, total_likes, total_dislikes = movies_popularity_ranking()
    
    #check if either person not in database
    if name_1 not in preference or name_2 not in preference:
        return 0
    
    #calculating everything based on math formulas
    vector_1 = preference[name_1]
    vector_2 = preference[name_2]
    numerator = dot(vector_1, vector_2)
    
    dotProduct_1 = dot(vector_1, vector_1)
    dotProduct_2 = dot(vector_2, vector_2)
    
    denominator = (dotProduct_1**0.5) * (dotProduct_2**0.5)

    if denominator == 0:
        cosine = -1000
    else:
        cosine = numerator/denominator

    
    return cosine

def dot(a,b):
    length = len(a)
    sum = 0
    for i in range(length):
        sum+= a[i] + b[i]

    return sum


def Movie_Soul_Mate(name):
    """Given a name, get the player that has highest Jaccard 
    similarity with this person."""
    soulmate = "test1"
    cosine_similarity = -100
    
    
    #import useful stuff
    [movies, preference] = read_in_movie_preference()
    movie_popularity, movie_popularity_rank, total_likes, total_dislikes = movies_popularity_ranking()
    
    #if name not in dictionary
    if name not in preference:
        return "test1"
    
    #iterate through everyone other than focal person, check cosine, and update soulmate if better similarity
    for person in preference.keys():
        if person != name:
            cosine = Similarity(name,person).real
            if cosine > cosine_similarity:
                soulmate = person
                cosine_similarity = cosine
            elif cosine == cosine_similarity:
                if len(person) < len(soulmate):
                    soulmate = person
                    cosine_similarity = cosine

    return soulmate, cosine_similarity

#find all movies name has not watched, but souldmate watched and liked
#highest pop score of those movies
def Recommendation2(name):
    recommended_movie = "Unfortunately, no new movies for you."
    
    #bring in important data
    [movies, preference] = read_in_movie_preference()
    movie_popularity, movie_popularity_rank, total_likes, total_dislikes = movies_popularity_ranking()
    
    #check to see if name is in database
    if name not in preference:
        return "Invalid User."
    
    #soulmate data
    soulmate, cosine_similarity = Movie_Soul_Mate(name)
    
    #create temp list, fill with movies soulmate liked, but name has not seen
    temp_list = []
    
    for i in range(len(preference[soulmate])):
        if preference[soulmate][i] == 1 and preference[name][i] == 0:
            temp_list.append(movies[i])
            

    #if there are no movies with the above criteria, do what we did in 3.2
    if temp_list == []:
        return Recommendation(name)
        
    #if there are movies mathcing above conditions, pick the one ranked the highest and return
    for movie in movie_popularity_rank:
        if movie in temp_list:
            recommended_movie = movie
            break

    return recommended_movie


