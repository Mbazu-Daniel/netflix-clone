from django.shortcuts import render, redirect
from django.views import View 
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from core.models import Movie, Profile
from .forms import ProfileForm
# Create your views here.


class Home(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("core:profile_list")
        return render(request, "index.html")

@method_decorator(login_required, name="dispatch")
class ProfileList(View):
    def get(self, request, *args, **kwargs):
        profiles = request.user.profiles.all()
        context = { "profiles": profiles }
        return render(request, "profileList.html", context)

@method_decorator(login_required, name="dispatch")  
class ProfileCreate(View):
    def get(self, request, *args, **kwargs):
        # form for creating profile
        form = ProfileForm()
        context = { "form": form }
        return render(request, "profileCreate.html", context)
    
    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        
        if form.is_valid():
            profile  = Profile.objects.create(**form.cleaned_data)
            request.user.profiles.add(profile)
            if profile:
                return redirect("core:profile_list")
        context = { "form": form }
        return render(request, "profileCreate.html", context)
    

@method_decorator(login_required, name="dispatch")  
class Watch(View):
    def get(self, request, profile_id, *args, **kwargs):
        try:
            profile = Profile.objects.get(uuid=profile_id)
            movies = Movie.objects.filter(age_limit = profile.age_limit)
            
            try:
                showcase=movies[0]
            except :
                showcase=None
            
            if profile not in request.user.profiles.all():
                return redirect("core:profile_list")
            
            context = {"movies": movies,'show_case':showcase}
            return render(request, "movieList.html", context)

        except Profile.DoesNotExist:
             return redirect("core:profile_list")
         
         
         
@method_decorator(login_required, name="dispatch")         
class ShowMovieDetail(View):
    def get(self, request, movie_id, *args, **kwargs):
        try:
            movie = Movie.objects.get(uuid = movie_id)
            return render(request, "movieDetail.html", {"movie": movie})
        
        except Movie.DoesNotExist:
            return redirect("core:profile_list")
        
         
@method_decorator(login_required, name="dispatch")        
class ShowMovie(View):
    def get(self, request,movie_id, *args, **kwargs):
        try: 
            movie = Movie.objects.get(uuid = movie_id)
            movie = movie.videos.values()
            return render(request, "showMovie.html", {"movie": list(movie)})
        
        except Movie.DoesNotExist:
            return redirect("core:profile_list")
         