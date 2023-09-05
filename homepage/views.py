from weeklyreport.models import Users, Services
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import logging

logger = logging.getLogger("django")


@login_required()
def dashboard_view(request):
    try:
        if request.method == "POST":
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                # log the user in
                user = form.get_user()
                login(request, user)
                return redirect("homepage:dashboard")
        
        team = Users.objects.filter(username=request.user).values_list(
            "teamname", flat=True)[0]
        services = Services.objects.filter(teamname=team).order_by("servicename")
    
        context = {
            "user": request.user,
            "team": team,
            "services": services
        }

        return render(request, "homepage/dashboard.html", context)

    except IndexError:
        return render(request, "homepage/unauthorized_user.html")
        

def logout_view(request):
    logout(request)
    return redirect("/")