from .forms import ServicesForm
from .models import Services
from weeklyreport.models import Users
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import xlwt
import datetime
import logging

logger = logging.getLogger("django")


@login_required()
def showservice(request):
    if request.method == "GET":
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]
        services = Services.objects.filter(teamname=team).order_by("serviceid")
        context = {
            "services": services,
            "team" : team
        }

        return render(request, "services/showservice.html", context)

@login_required()
def addservice(request):
    if request.method == "POST":
        form = ServicesForm(request.POST)
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]
        if form.is_valid():
            service = form.save(commit=False)
            service.teamname = team
            service.save()
            service_name = service.servicename
            messages.success(request, "{0} isimli servis başarıyla oluşturuldu.".format(service_name))

            return  redirect("/services/show")
        else:
            context = {
                "form": form,
                "team": team
            }
            
            return render(request, "services/addservice.html", context)

    if request.method == "GET":
        form = ServicesForm()
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]
        context = {
            "form": form,
            "team": team
        }
        
        return render(request, "services/addservice.html", context)

@login_required()
def updateservice(request, team, id):
    if request.method == "POST":
        service = get_object_or_404(Services, serviceid = id, teamname=team)
        form = ServicesForm(request.POST, instance = service)
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]

        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            service_name = service.servicename
            messages.success(request, "{0} isimli servis başarıyla güncellendi.".format(service_name))

            return redirect("/services/show")
        else:
            context = {
                "form": form,
                "team": team
            }
            
            return render(request, "services/updateservice.html", context)

    if request.method == "GET":
        service = get_object_or_404(Services, serviceid = id, teamname=team)
        form = ServicesForm(instance = service)
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]
        context = {
            "form": form,
            "team": team
        }

        return render(request, "services/updateservice.html", context)

@login_required()
def deleteservice(request, team, id):
    if request.method == "GET":
        service = get_object_or_404(Services, serviceid = id, teamname=team)
        service.delete()
        service_name = service.servicename
        messages.success(request, "{0} isimli servis başarıyla silindi.".format(service_name))

        return redirect("/services/show")

@login_required()
def export_excel(request):
    if request.method == "GET":
        team = Users.objects.filter(username=request.user).values_list("teamname", flat=True)[0]

        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=Services_" + team + "_" + str(datetime.datetime.now()) + ".xls"
        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Services")
        row_num = 0
        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        columns = ["Servis ID","Servis adı","Ekip adı","SRE","SRE Yedek","Vendor","Sunucu lokasyonu","Prod dışı ortam bilgileri","Sunucu tipi","İşletim sistemi tipi","Uygulama sunucu sayısı","Sunucu bilgileri", "Veritabanı tipi","Veritabanı bağlantı bilgisi","Monitor edildiği uygulamalar","Log entegrasyonu","Log index","Support detayları","Entegre olduğu uygulamalar/servisler","Diğerleri","SOX kritik mi?","Müşteri kritik veri barındırır mı?","ODM Platformu var mı?","Kendi içinde yedeklilik (HA) var mı?","Dış kurum entegrasyonu var mı?","Servis kesintisi iç/dış müşteriyi etkiler mi?","Uygulama sunucularının backup\"ı var mı?"]

        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        font_style = xlwt.XFStyle()

        rows = Services.objects.filter(teamname=team).values_list("serviceid","servicename","teamname","sre","srebackup","vendor","serverlocation","nonprodenvtypes","servertype","ostype","appservercount","serverhostnames","dbtype","dbconnstring","monitoringapps","logintegration","logindex","supportdetail","integratedservices","other","sox","soxcriticdata","odmplatform","highavailability","regulatoryintegration","customereffect","backup").order_by("serviceid")

        for row in rows:
            row_num += 1

            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_style)

        wb.save(response)

        return response