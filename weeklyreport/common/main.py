from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.template.loader import render_to_string
from email.mime.image import MIMEImage
from weeklyreport.models import Reports, Users, Teams
import datetime
import os


def team_entry_statistics(team: str, weeknum: int):
    """
    Haftalık rapor uygulamasında, ekipteki kullanıcıların rapor istatistiklerini (mevcut haftadaki) getirir.
    """
    entry_statistics_query = (Reports.objects
                                  .filter(team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year)
                                  .values("entry_owner")
                                  .annotate(entry_count=Count("entry"))
                                  .order_by()
                                  )

    entry_statistics = []
    [entry_statistics.append((entry["entry_owner"], entry["entry_count"])) for entry in entry_statistics_query]

    has_entry_statistics_users = []
    [has_entry_statistics_users.append(has_entry_user[0]) for has_entry_user in entry_statistics]

    team_users = Users.objects.filter(teamname=team).values_list("username", flat=True)

    [entry_statistics.append((user, 0)) for user in team_users if user not in has_entry_statistics_users]

    def take_second_param(elem):
        return elem[1]
    
    entry_statistics.sort(key=take_second_param, reverse=True)
    
    return entry_statistics


def send_mail_to(request, team: str, to_whom: int):
    """
    Haftalık rapor uygulaması üzerinden mail gönderir.
    to_whom değerine göre login olan Kişiye, Ekip Yöneticisine ya da Birim Müdürüne mail gönderir.
    
        to_whom = 0 => Login olan Kişiye mail gönderir.\n
        to_whom = 1 => Ekip Yöneticisine mail gönderir.\n
        to_whom = 2 => Birim Müdürüne mail gönderir.\n
    
    diğer to_whom değerleri için "Geçersiz parametre. Sistemsel bir hata oluştu." döner.
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    if to_whom == 0:
        to_mail = Users.objects.filter(username=request.user.username).values_list("mail", flat=True).get()
        to_list = to_mail.split(";")
    elif to_whom == 1:
        to_mail = Teams.objects.filter(teamname=team).values_list("manager_mail", flat=True).get()
        to_list = to_mail.split(";")
    elif to_whom == 2:
        to_mail = Teams.objects.filter(teamname=team).values_list("unithead_mail", flat=True).get()
        to_list = to_mail.split(";")
    else:
        print("Geçersiz parametre. Sistemsel bir hata oluştu.")
        return "Geçersiz parametre. Sistemsel bir hata oluştu."
    
    current_year = datetime.datetime.now().year
    weeknum = datetime.date.today().isocalendar()[1]
    yearnum = datetime.date.today().year
    highlights = Reports.objects.filter(type="Highlight", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    lowlights = Reports.objects.filter(type="Lowlight", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    escalations = Reports.objects.filter(type="Waiting for Executive Support", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    infos = Reports.objects.filter(type="Info", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    progress = Reports.objects.filter(type="Progress", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")

    msg = EmailMultiAlternatives()
    subject = "{0} Haftalık Rapor – {1} {2}.Hafta".format(team, current_year, weeknum)

    msg.content_subtype = "html"
    msg.content_subtype = "utf-8"
    html_content = render_to_string("weeklyreport/email.html",
                                        {
                                            "highlights": highlights, 
                                            "lowlights": lowlights, 
                                            "escalations": escalations,
                                            "infos": infos, 
                                            "progress": progress, 
                                            "team": team, 
                                            "subject": subject
                                        }
                                    )
    subject = "{0} Haftalık Rapor – {1} {2}.Hafta".format(team, current_year, weeknum)
    msg = EmailMultiAlternatives(subject, "", "FinancialHub-WeeklyReport@garantibbva.com.tr", to_list)
    msg.attach_alternative(html_content, "text/html")
    msg.mixed_subtype = "related"

    try:
        for f in os.listdir(os.path.join(BASE_DIR, "media/REPORT/documents/uploads/{0}/{1}".format(yearnum, weeknum))):
            if Reports.objects.filter(team=team, entry_date__week=weeknum,entry_date__year=datetime.date.today().year, document="REPORT/documents/uploads/{0}/{1}/{2}".format(yearnum, weeknum, f)).exists():
                print("Eklenecek Image adı: ", f)
                fp = open(os.path.join(BASE_DIR, "media/REPORT/documents/uploads/{0}/{1}".format(yearnum, weeknum), f), "rb")
                msg_img = MIMEImage(fp.read())
                fp.close()
                msg_img.add_header("Content-ID", "<REPORT/documents/uploads/{0}/{1}/{2}>".format(yearnum, weeknum, f))
                msg.attach(msg_img)
                print("Image başarıyla eklendi.")
            else:
                print("{0} isimli Image eklenemedi".format(f))
    except FileNotFoundError:
        print("Rapora eklenecek Image bulunamadı.")

    fp = open(os.path.join(BASE_DIR, "homepage/static/images/weeklyreport/hl.png"), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header("Content-ID", "<hl.png>")
    msg.attach(msg_img)

    fp = open(os.path.join(BASE_DIR, "homepage/static/images/weeklyreport/ll.png"), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header("Content-ID", "<ll.png>")
    msg.attach(msg_img)

    fp = open(os.path.join(BASE_DIR, "homepage/static/images/weeklyreport/wfes.png"), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header("Content-ID", "<wfes.png>")
    msg.attach(msg_img)

    fp = open(os.path.join(BASE_DIR, "homepage/static/images/weeklyreport/info.png"), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header("Content-ID", "<info.png>")
    msg.attach(msg_img)

    fp = open(os.path.join(BASE_DIR, "homepage/static/images/weeklyreport/progress.png"), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header("Content-ID", "<progress.png>")
    msg.attach(msg_img)

    fp = open(os.path.join(BASE_DIR, "homepage/static/images/weeklyreport/gt-logo-small.png"), "rb")
    msg_img = MIMEImage(fp.read())
    fp.close()
    msg_img.add_header("Content-ID", "<gt-logo-small.png>")
    msg.attach(msg_img)

    msg.send()


def get_all_reports(team: str, weeknum: int):
    """
    Haftalık rapor uygulamasında, login olan kullanıcının bağlı olduğu ekibe ait tüm raporları (mevcut haftadaki) getirir.
    """
    highlights = Reports.objects.filter(type="Highlight", team=team,entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    lowlights = Reports.objects.filter(type="Lowlight", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    escalations = Reports.objects.filter(type="Waiting for Executive Support", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    infos = Reports.objects.filter(type="Info", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    progress = Reports.objects.filter(type="Progress", team=team, entry_date__week=weeknum, entry_date__year=datetime.date.today().year).values().order_by("priority", "service")
    
    return highlights, lowlights, escalations, infos, progress


def search_in_reports(team: str, keyword: int):
    """
    Haftalık rapor uygulamasında, login olan kullanıcının Search button'ı kullanarak aradığı raporları getirir.
    """
    highlights = Reports.objects.filter(type="Highlight", team=team, entry__contains=keyword).values().order_by("priority", "service") | Reports.objects.filter(type="Highlight", team=team, entry_owner__contains=keyword).values().order_by("priority", "service")
    lowlights = Reports.objects.filter(type="Lowlight", team=team, entry__contains=keyword).values().order_by("priority", "service") | Reports.objects.filter(type="Lowlight", team=team, entry_owner__contains=keyword).values().order_by("priority", "service")
    escalations = Reports.objects.filter(type="Waiting for Executive Support", team=team, entry__contains=keyword).values().order_by("priority", "service") | Reports.objects.filter(type="Waiting for Executive Support", team=team, entry_owner__contains=keyword).values().order_by("priority", "service")
    infos = Reports.objects.filter(type="Info", team=team, entry__contains=keyword).values().order_by("priority", "service") | Reports.objects.filter(type="Info", team=team, entry_owner__contains=keyword).values().order_by("priority", "service")
    progress = Reports.objects.filter(type="Progress", team=team, entry__contains=keyword).values().order_by("priority", "service") | Reports.objects.filter(type="Progress", team=team, entry_owner__contains=keyword).values().order_by("priority", "service")
    
    return highlights, lowlights, escalations, infos, progress
