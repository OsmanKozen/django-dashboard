from .forms import ReportForm, ServiceForm
from .models import Reports, Services, Users, Teams, Managers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .common.main import team_entry_statistics, send_mail_to, get_all_reports, search_in_reports
import datetime
import logging

logger = logging.getLogger("django")


@login_required()
def show(request):
    if request.method == "GET":
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]
        current_year = datetime.datetime.now().year
        weeknum = datetime.date.today().isocalendar()[1]
        subject = "{0} Haftalık Rapor – {1} {2}. Hafta".format(team, current_year, weeknum)
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today().year).values("entry_date__week").distinct().order_by("-entry_date__week")
        services = Services.objects.filter(teamname=team).order_by("servicename")
        
        # Login olan kullanıcının bağlı olduğu ekibe ait tüm raporlar (mevcut haftadaki)
        highlights, lowlights, escalations, infos, progress = get_all_reports(team, weeknum)

        # Ekipteki kullanıcıların rapor istatistikleri (mevcut haftadaki)
        entry_statistics = team_entry_statistics(team, weeknum)

        context = {
            "highlights": highlights, 
            "lowlights": lowlights, 
            "escalations": escalations, 
            "infos": infos, 
            "progress": progress,
            "team": team, 
            "services": services, 
            "subject": subject, 
            "available_weeknums": available_weeknums, 
            "entry_statistics": entry_statistics
        }

        return render(request, "weeklyreport/show.html", context)


@login_required()
def add(request, team):
    if request.method == "POST":
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Rapor başarıyla eklendi.")
            redirection_url = "/weeklyreport/{0}/add".format(team)
            return redirect(redirection_url)
        else:
            cur_user = request.user.username
            services = Services.objects.filter(teamname=team).order_by("servicename")
            users = Users.objects.filter(teamname=team)
            unit = Teams.objects.filter(teamname=team).values_list("unitname", flat=True)[0]
            manager = Managers.objects.filter(teamname=team).values_list("managername", flat=True)[0]
            available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today().year).values("entry_date__week").distinct().order_by("-entry_date__week")

            messages.add_message(request, messages.ERROR, "Rapor eklemesi başarısız.")

            context = {
                "form": form, 
                "services": services, 
                "users": users, 
                "unit": unit, 
                "manager": manager, 
                "team": team, 
                "cur_user": cur_user, 
                "available_weeknums": available_weeknums
            }

            return render(request, "weeklyreport/add.html", context)


    if request.method == "GET":
        form = ReportForm()
        cur_user = request.user.username
        services = Services.objects.filter(teamname=team).order_by("servicename")
        users = Users.objects.filter(teamname=team)
        unit = Teams.objects.filter(teamname=team).values_list("unitname", flat=True)[0]
        manager = Managers.objects.filter(teamname=team).values_list("managername", flat=True)[0]
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today().year).values("entry_date__week").distinct().order_by("-entry_date__week")

        context = {
            "form": form, 
            "services": services, 
            "users": users, 
            "unit": unit, 
            "manager": manager, 
            "team": team,
            "cur_user": cur_user, 
            "available_weeknums": available_weeknums
        }

        return render(request, "weeklyreport/add.html", context)


@login_required()
def details(request, team):
    if request.method == "GET":
        weeknum = datetime.date.today().isocalendar()[1]
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today().year).values("entry_date__week").distinct().order_by("-entry_date__week")
        reports = Reports.objects.filter(entry_date__week=weeknum, entry_date__year=datetime.date.today().year, team=team).order_by("service")
        services = Services.objects.filter(teamname=team).order_by("servicename")
        
        # Login olan kullanıcının bağlı olduğu ekibe ait tüm raporlar (mevcut haftadaki)
        highlights, lowlights, escalations, infos, progress = get_all_reports(team, weeknum)

        context = {
            "reports": reports, 
            "team": team, 
            "highlights": highlights, 
            "lowlights": lowlights,
            "escalations": escalations, 
            "infos": infos, 
            "progress": progress, 
            "services": services, 
            "available_weeknums": available_weeknums
        }

        return render(request, "weeklyreport/details.html", context)


@login_required()
def edit(request, team, id):
    if request.method == "GET":
        reports = Reports.objects.get(id=id)
        services = Services.objects.filter(teamname=team)
        users = Users.objects.filter(teamname=team)
        unit = Teams.objects.filter(teamname=team).values_list("unitname", flat=True)[0]
        manager = Managers.objects.filter(teamname=team).values_list("managername", flat=True)[0]

        context = {
            "reports": reports, 
            "services": services, 
            "users": users, 
            "unit": unit,
            "manager": manager, 
            "team": team
        }

        return render(request, "weeklyreport/edit.html", context)


@login_required()
def update(request, team, id):
    if request.method == "POST":
        instance = get_object_or_404(Reports, id=id)
        form = ReportForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            redirection_url = "/weeklyreport/{0}/details".format(team)
            messages.add_message(request, messages.SUCCESS, "Rapor başarıyla güncellendi.")

            return redirect(redirection_url)
        else:
            messages.add_message(request, messages.ERROR, "Rapor güncellemesi başarısız.")
            redirection_url = "/weeklyreport/{0}/edit/{1}".format(team, instance.id)

            return redirect(redirection_url)


@login_required()
def destroy(request, team, id):
    if request.method == "GET":
        reports = Reports.objects.get(id=id)
        reports.delete()
        redirection_url = "/weeklyreport/{0}/details".format(team)
        messages.add_message(request, messages.SUCCESS, "Rapor başarıyla silindi.")

        return redirect(redirection_url)


@login_required()
def showold(request):
    if request.method == "POST":
        current_year = datetime.datetime.now().year
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]
        weeknum = request.POST["weeknum"]
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today().year).values("entry_date__week").distinct().order_by("-entry_date__week")
        subject = "{0} Haftalık Rapor – {1} {2}. Hafta".format(team, current_year, weeknum)

        # Login olan kullanıcının bağlı olduğu ekibe ait tüm raporlar (mevcut haftadaki)
        highlights, lowlights, escalations, infos, progress = get_all_reports(team, weeknum)

        context = {
            "highlights": highlights, 
            "lowlights": lowlights, 
            "escalations": escalations, 
            "infos": infos, 
            "progress": progress,
            "team": team, 
            "weeknum": weeknum, 
            "subject": subject, 
            "available_weeknums": available_weeknums
        }

        return render(request, "weeklyreport/showold.html", context)


@login_required()
def add_service(request, team):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            redirection_url = "/weeklyreport/{0}/add_service".format(team)
            service_name = service.servicename
            messages.add_message(request, messages.SUCCESS, "{0} isimli servis başarıyla eklendi.".format(service_name))

            return redirect(redirection_url)
        else:
            form = ServiceForm()

    if request.method == "GET":
        form = ServiceForm()
        user = request.user.username.upper()
        team = Users.objects.filter(username=request.user.username).values_list("teamname", flat=True)[0]
        unit = Users.objects.filter(username=request.user.username).values_list("unitname", flat=True)[0]
        services = Services.objects.filter(teamname=team, username=request.user.username.upper())

        context = {
            "form": form, 
            "user": user, 
            "unit": unit, 
            "team": team, 
            "services": services
        }

        return render(request, "weeklyreport/add_service.html", context)


@login_required()
def delete_service(request, team, id):
    if request.method == "GET":
        service = Services.objects.get(id=id)
        service.delete()
        redirection_url = "/weeklyreport/{0}/add_service".format(team)
        service_name = service.servicename
        messages.add_message(request, messages.SUCCESS, "{0} isimli servis başarıyla silindi.".format(service_name))

        return redirect(redirection_url)


@login_required()
def search(request, team):
    team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]
    keyword = request.POST["search"]

    highlights, lowlights, escalations, infos, progress = search_in_reports(team, keyword)

    context = {
        "highlights": highlights, 
        "lowlights": lowlights, 
        "escalations": escalations, 
        "infos": infos, 
        "progress": progress,
        "team": team,
        "keyword": keyword
    }

    return render(request, "weeklyreport/showsearch.html", context)


@login_required()
def send_mail_to_me(request, team):
    if request.method == "GET":
        try:
            send_mail_to(request, team, to_whom=0)
            redirection_url = "/weeklyreport/show"
            messages.add_message(request, messages.SUCCESS, "Mail başarıyla gönderildi.")
            
            return redirect(redirection_url)
        except Exception as error:
            print("Sistemsel bir hata oluştu.", error)
            redirection_url = "/weeklyreport/show"
            messages.add_message(request, messages.ERROR, "Mail gönderimi başarısız.")
            
            return redirect(redirection_url)


@login_required()
def send_mail_to_manager(request, team):
    if request.method == "GET":
        try:
            send_mail_to(request, team, to_whom=1)
            redirection_url = "/weeklyreport/show"
            messages.add_message(request, messages.SUCCESS, "Mail başarıyla gönderildi.")
            
            return redirect(redirection_url)
        except Exception as error:
            print("Sistemsel bir hata oluştu.", error)
            redirection_url = "/weeklyreport/show"
            messages.add_message(request, messages.ERROR, "Mail gönderimi başarısız.")
            
            return redirect(redirection_url)


@login_required()
def send_mail_to_unithead(request, team):
    if request.method == "GET":
        try:
            send_mail_to(request, team, to_whom=2)
            redirection_url = "/weeklyreport/show"
            messages.add_message(request, messages.SUCCESS, "Mail başarıyla gönderildi.")
            
            return redirect(redirection_url)
        except Exception as error:
            print("Sistemsel bir hata oluştu.", error)
            redirection_url = "/weeklyreport/show"
            messages.add_message(request, messages.ERROR, "Mail gönderimi başarısız.")
            
            return redirect(redirection_url)
