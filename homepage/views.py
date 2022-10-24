from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from weeklyreport.models import Users, Services


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # log the user in
            user = form.get_user()
            login(request, user)
            return redirect("homepage:dashboard")
    # else:
    #     form = AuthenticationForm()

    return render(request, "homepage/login.html", {'form': form})


@login_required()
def dashboard_view(request):
    try:    
        team = Users.objects.filter(username=request.user).values_list(
            'teamname', flat=True)[0]
        services = Services.objects.filter(teamname=team).order_by('servicename')
    except IndexError:
        return render(request, "homepage/unauthorized_user.html")
        
    content = {
        "user": request.user,
        "team": team,
        "services": services
    }

    return render(request, "homepage/dashboard.html", content)


def logout_view(request):
    logout(request)
    return redirect("/")
