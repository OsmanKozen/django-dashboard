import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ReportForm, ServiceForm
from .models import Reports, Services, Users, Teams, Units, Managers
from django.contrib.auth.decorators import login_required
import logging
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.template.loader import render_to_string
from django.db.models import Count
import os

logger = logging.getLogger('django')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@login_required()
def show(request):
    if request.method == "GET":
        team = Users.objects.filter(username=request.user).values_list(
            'teamname', flat=True)[0]

        current_year = datetime.datetime.now().year
        weeknum = datetime.date.today().isocalendar()[1]
        subject = "{0} Haftalık Rapor – {1} {2}. Hafta".format(
            team, current_year, weeknum)
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today(
        ).year).values('entry_date__week').distinct().order_by('-entry_date__week')
        highlights = Reports.objects.filter(type='Highlight', team=team,
                                            entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        lowlights = Reports.objects.filter(type='Lowlight', team=team,
                                           entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        escalations = Reports.objects.filter(type='Waiting for Executive Support', team=team,
                                             entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        infos = Reports.objects.filter(type='Info', team=team,
                                       entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        progress = Reports.objects.filter(type='Progress', team=team,
                                          entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        services = Services.objects.filter(
            teamname=team).order_by('servicename')

        # Team Entry Statistics
        entry_statistics_query = (Reports.objects
                                  .filter(team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year)
                                  .values('entry_owner')
                                  .annotate(entry_count=Count('entry'))
                                  .order_by()
                                  )

        entry_statistics = []
        [entry_statistics.append((entry['entry_owner'], entry['entry_count']))
         for entry in entry_statistics_query]

        has_entry_statistics_users = []
        [has_entry_statistics_users.append(has_entry_user[0])
         for has_entry_user in entry_statistics]

        team_users = Users.objects.filter(
            teamname=team).values_list('username', flat=True)

        [entry_statistics.append(
            (user, 0)) for user in team_users if user not in has_entry_statistics_users]

        def takeSecond(elem):
            return elem[1]
        entry_statistics.sort(key=takeSecond, reverse=True)

        context = {'highlights': highlights, 'lowlights': lowlights, 'escalations': escalations, 'infos': infos, 'progress': progress,
                   'team': team, 'services': services, 'subject': subject, 'available_weeknums': available_weeknums, 'entry_statistics': entry_statistics}

        return render(request, 'weeklyreport/show.html', context)


@login_required()
def add(request, team):
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "Rapor başarıyla eklendi.")
            redirection_url = '/weeklyreport/{0}/add'.format(team)
            return redirect(redirection_url)
        else:
            form = ReportForm()
            cur_user = request.user.username.upper()
            services = Services.objects.filter(
                teamname=team).order_by('servicename')
            users = Users.objects.filter(teamname=team)

            unit = Teams.objects.filter(teamname=team).values_list(
                'unitname', flat=True)[0]
            manager = Managers.objects.filter(
                teamname=team).values_list('managername', flat=True)[0]
            available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today(
            ).year).values('entry_date__week').distinct().order_by('-entry_date__week')

            messages.add_message(request, messages.WARNING,
                                 "Lütten Entry alanını doldurunuz.")

            context = {'form': form, 'services': services, 'users': users, 'unit': unit,
                    'manager': manager, 'team': team, 'cur_user': cur_user, 'available_weeknums': available_weeknums}

            return render(request, 'weeklyreport/add.html', context)

    if request.method == "GET":
        form = ReportForm()
        cur_user = request.user.username.upper()
        services = Services.objects.filter(
            teamname=team).order_by('servicename')
        users = Users.objects.filter(teamname=team)

        unit = Teams.objects.filter(teamname=team).values_list(
            'unitname', flat=True)[0]
        manager = Managers.objects.filter(
            teamname=team).values_list('managername', flat=True)[0]
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today(
        ).year).values('entry_date__week').distinct().order_by('-entry_date__week')

        context = {'form': form, 'services': services, 'users': users, 'unit': unit,
                   'manager': manager, 'team': team, 'cur_user': cur_user, 'available_weeknums': available_weeknums}

        return render(request, 'weeklyreport/add.html', context)


@login_required()
def details(request, team):
    if request.method == "GET":
        weeknum = datetime.date.today().isocalendar()[1]
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today(
        ).year).values('entry_date__week').distinct().order_by('-entry_date__week')
        reports = Reports.objects.filter(
            entry_date__week=weeknum, entry_date__year=datetime.date.today().year, team=team).order_by('service')
        highlights = Reports.objects.filter(type='Highlight', team=team,
                                            entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        lowlights = Reports.objects.filter(type='Lowlight', team=team,
                                           entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        escalations = Reports.objects.filter(type='Waiting for Executive Support', team=team,
                                             entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        infos = Reports.objects.filter(type='Info', team=team,
                                       entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        progress = Reports.objects.filter(type='Progress', team=team,
                                          entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        services = Services.objects.filter(
            teamname=team).order_by('servicename')

        context = {'reports': reports, 'team': team, 'highlights': highlights, 'lowlights': lowlights,
                   'escalations': escalations, 'infos': infos, 'progress': progress, 'services': services, 'available_weeknums': available_weeknums}

        return render(request, "weeklyreport/details.html", context)


@login_required()
def edit(request, team, id):
    if request.method == "GET":
        reports = Reports.objects.get(id=id)
        services = Services.objects.filter(teamname=team)
        users = Users.objects.filter(teamname=team)
        unit = Teams.objects.filter(teamname=team).values_list(
            'unitname', flat=True)[0]
        manager = Managers.objects.filter(
            teamname=team).values_list('managername', flat=True)[0]

        context = {'reports': reports, 'services': services, 'users': users, 'unit': unit,
                   'manager': manager, 'team': team}

        return render(request, 'weeklyreport/edit.html', context)


@login_required()
def update(request, team, id):
    if request.method == "POST":
        instance = get_object_or_404(Reports, id=id)
        form = ReportForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            redirection_url = '/weeklyreport/{0}/details'.format(team)
            messages.add_message(request, messages.SUCCESS,
                                 "Rapor başarıyla güncellendi.")

            return redirect(redirection_url)
        else:
            messages.add_message(request, messages.WARNING,
                                 "Lütten Entry alanını doldurunuz.")
            redirection_url = '/weeklyreport/{0}/edit/{1}'.format(team, instance.id)

            return redirect(redirection_url)


@login_required()
def destroy(request, team, id):
    if request.method == "GET":
        reports = Reports.objects.get(id=id)
        reports.delete()
        redirection_url = '/weeklyreport/{0}/details'.format(team)
        messages.add_message(request, messages.ERROR,
                             "Rapor başarıyla silindi.")

        return redirect(redirection_url)


@login_required()
def showold(request):
    if request.method == "POST":
        current_year = datetime.datetime.now().year
        team = Users.objects.filter(username=request.user).values_list(
            'teamname', flat=True)[0]
        weeknum = request.POST['weeknum']
        available_weeknums = Reports.objects.filter(entry_date__year=datetime.date.today(
        ).year).values('entry_date__week').distinct().order_by('-entry_date__week')

        highlights = Reports.objects.filter(type='Highlight', team=team,
                                            entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        lowlights = Reports.objects.filter(type='Lowlight', team=team,
                                           entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        escalations = Reports.objects.filter(type='Waiting for Executive Support', team=team,
                                             entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        infos = Reports.objects.filter(type='Info', team=team,
                                       entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        progress = Reports.objects.filter(type='Progress', team=team,
                                          entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        subject = "{0} Haftalık Rapor – {1} {2}. Hafta".format(
            team, current_year, weeknum)

        context = {'highlights': highlights, 'lowlights': lowlights, 'escalations': escalations, 'infos': infos, 'progress': progress,
                   'team': team, 'weeknum': weeknum, 'subject': subject, 'available_weeknums': available_weeknums
                   }

        return render(request, 'weeklyreport/showold.html', context)


@login_required()
def add_service(request, team):
    if request.method == "POST":
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            redirection_url = '/weeklyreport/{0}/add_service'.format(team)
            service_name = service.servicename
            messages.add_message(request, messages.SUCCESS,
                                 "{0} isimli servis başarıyla eklendi.".format(service_name))

            return redirect(redirection_url)
        else:
            form = ServiceForm()

    if request.method == "GET":
        form = ServiceForm()
        user = request.user.username.upper()
        team = Users.objects.filter(
            username=request.user.username.upper()).values_list('teamname', flat=True)[0]
        unit = Users.objects.filter(
            username=request.user.username.upper()).values_list('unitname', flat=True)[0]
        services = Services.objects.filter(
            teamname=team, username=request.user.username.upper())

        context = {'form': form, 'user': user, 'unit': unit, 'team': team, 'services': services}

        return render(request, 'weeklyreport/add_service.html', context)


@login_required()
def delete_service(request, team, id):
    if request.method == "GET":
        service = Services.objects.get(id=id)
        service.delete()
        redirection_url = '/weeklyreport/{0}/add_service'.format(team)
        service_name = service.servicename
        messages.add_message(request, messages.ERROR,
                             "{0} isimli servis başarıyla silindi.".format(service_name))
                             
        return redirect(redirection_url)


@login_required()
def send_mail_to_me(request, team):
    if request.method == "GET":
        current_year = datetime.datetime.now().year

        weeknum = datetime.date.today().isocalendar()[1]
        highlights = Reports.objects.filter(type='Highlight', team=team,
                                            entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        lowlights = Reports.objects.filter(type='Lowlight', team=team,
                                           entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        escalations = Reports.objects.filter(type='Waiting for Executive Support', team=team,
                                             entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        infos = Reports.objects.filter(type='Info', team=team,
                                       entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')
        progress = Reports.objects.filter(type='Progress', team=team,
                                          entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by('priority', 'service')

        msg = EmailMultiAlternatives()
        subject = "{0} Haftalık Rapor – {1} {2}.Hafta".format(
            team, current_year, weeknum)
        user_mail_str = Users.objects.filter(
            username=request.user.username.upper()).values_list('mail', flat=True).get()
        user_mail = []
        user_mail.append(user_mail_str)
        msg.content_subtype = "html"
        msg.content_subtype = "utf-8"
        html_content = render_to_string('weeklyreport/email.html',
                                        {'highlights': highlights, 'lowlights': lowlights, 'escalations': escalations,
                                         'infos': infos, 'progress': progress, 'team': team, 'subject': subject
                                         })
        subject = "{0} Haftalık Rapor – {1} {2}.Hafta".format(
            team, current_year, weeknum)
        msg = EmailMultiAlternatives(subject, "",
                                     "FinancialHub-WeeklyReport@garantibbva.com.tr",
                                     user_mail)
        msg.attach_alternative(html_content, "text/html")

        msg.mixed_subtype = 'related'

        fp = open(os.path.join(
            BASE_DIR, 'homepage/static/images/weeklyreport/hl.png'), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<hl.png>')
        msg.attach(msg_img)

        fp = open(os.path.join(
            BASE_DIR, 'homepage/static/images/weeklyreport/ll.png'), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<ll.png>')
        msg.attach(msg_img)

        fp = open(os.path.join(
            BASE_DIR, 'homepage/static/images/weeklyreport/wfes.png'), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<wfes.png>')
        msg.attach(msg_img)

        fp = open(os.path.join(
            BASE_DIR, 'homepage/static/images/weeklyreport/info.png'), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<info.png>')
        msg.attach(msg_img)

        fp = open(os.path.join(
            BASE_DIR, 'homepage/static/images/weeklyreport/progress.png'), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<progress.png>')
        msg.attach(msg_img)

        fp = open(os.path.join(
            BASE_DIR, 'homepage/static/images/weeklyreport/gt-logo-small.png'), 'rb')
        msg_img = MIMEImage(fp.read())
        fp.close()
        msg_img.add_header('Content-ID', '<gt-logo-small.png>')
        msg.attach(msg_img)

        msg.send()
        redirection_url = '/weeklyreport/show'.format(team)
        messages.add_message(request, messages.SUCCESS,
                             "Mail başarıyla gönderildi.")
        return redirect(redirection_url)
