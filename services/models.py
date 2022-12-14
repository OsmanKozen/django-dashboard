from tkinter.messagebox import RETRY
from django.db import models
from multiselectfield import MultiSelectField

# Create your models here.
servicelocation = (
    ('Intranet', 'Intranet'),
    ('Extranet', 'Extranet'),
    ('Internet', 'Internet'),
)

nonprodenvtypes = (
    ('Dev', 'Dev'),
    ('Test', 'Test'),
    ('QA', 'QA'),
    ('Yok', 'Yok'),
)

servertype = (
    ('Fiziksel', 'Fiziksel'),
    ('Sanal', 'Sanal'),
)

ostype = (
    ('Windows Server 2008', 'Windows Server 2008'),
    ('Windows Server 2012', 'Windows Server 2012'),
    ('Windows Server 2016', 'Windows Server 2016'),
    ('Windows Server 2019', 'Windows Server 2019'),
    ('Windows Server 2022', 'Windows Server 2022'),
    ('Linux RedHat 5', 'Linux RedHat 5'),
    ('Linux RedHat 6', 'Linux RedHat 6'),
    ('Linux RedHat 7', 'Linux RedHat 7'),
    ('Linux RedHat 8', 'Linux RedHat 8'),
    ('Linux Debian', 'Linux Debian'),
    ('Linux CenOS', 'Linux CenOS'),
    ('Linux Suse', 'Linux Suse'),
    ('Linux Ubuntu', 'Linux Ubuntu'),
    ('Mainframe', 'Mainframe'),
    ('Unix', 'Unix'),
)

dbtype = (
    ('Oracle', 'Oracle'),
    ('MySQL', 'MySQL'),
    ('Microsoft SQL Server', 'Microsoft SQL Server'),
    ('DB2', 'DB2'),
    ('PostgreSQL', 'PostgreSQL'),
    ('MongoDB', 'MongoDB'),
    ('Redis', 'Redis'),
    ('Elasticsearch', 'Elasticsearch'),
    ('SQLite', 'SQLite'),
    ('Cassandra', 'Cassandra'),
    ('MariaDB', 'MariaDB'),
    ('Hive', 'Hive'),
    ('Couchbase', 'Couchbase'),
    ('InFluxDB', 'InFluxDB'),
    ('Veritaban─▒ yok', 'Veritaban─▒ yok'),
)

monitoringapps = (
    ('Dynatrace', 'Dynatrace'),
    ('SLM', 'SLM'),
    ('Microsoft SCOM', 'Microsoft SCOM'),
    ('Sitescope', 'Sitescope'),
    ('Prometheus', 'Prometheus'),
    ('DbVision', 'DbVision'),
    ('BPM', 'BPM'),
    ('AIOPS', 'AIOPS'),
    ('Monitor edilmiyor', 'Monitor edilmiyor'),
)

logintegration = (
    ('Splunk', 'Splunk'),
    ('ELK', 'ELK'),
    ('Prometheus', 'Prometheus'),
    ('ArcSight', 'ArcSight'),
    ('Log entegrasyonu yok', 'Log entegrasyonu yok'),
)

supportdetail = (
    ('SLA - Var', 'SLA - Var'),
    ('SLA - Yok', 'SLA - Yok'),
    ('Support - 24x7', 'Support - 24x7'),
    ('Support - 8x5', 'Support - 8x5'),
    ('Support Yok', 'Support Yok'),
    ('Bilmiyorum', 'Bilmiyorum'),
)

integratedservices = (
    ('LDAP', 'LDAP'),
    ('AD', 'AD'),
    ('ODI', 'ODI'),
    ('SSO', 'SSO'),
    ('IVR', 'IVR'),
    ('Smart', 'Smart'),
    ('Coolgen', 'Coolgen'),
    ('ARK', 'ARK'),
    ('DWH(Raporlama)', 'DWH(Raporlama)'),
    ('STEP', 'STEP'),
    ('├ľdeme Sistemleri', '├ľdeme Sistemleri'),
    ('Di─čer', 'Di─čer'),
)

class Services(models.Model):

    serviceid = models.PositiveIntegerField(verbose_name="Service ID", default=0)
    servicename = models.CharField(verbose_name="Servis ad─▒", max_length=100, default="")
    teamname = models.CharField(verbose_name="Ekip ad─▒", max_length=100, default="", editable=False)
    sre = models.CharField(verbose_name="SRE", max_length=100)
    srebackup = models.CharField(verbose_name="SRE Yedek", max_length=100)
    vendor = models.CharField(verbose_name="Vendor", help_text="GT ya da 'Firma ad─▒' giriniz ", max_length=100, default="")
    serverlocation = MultiSelectField(verbose_name="Sunucu lokasyonu", help_text="├çoklu se├žim yapabilirsiniz", max_length=100, choices=servicelocation)
    nonprodenvtypes = MultiSelectField(verbose_name="Production d─▒┼č─▒nda hangi ortamlar var?", help_text="├çoklu se├žim yapabilirsiniz", choices=nonprodenvtypes)
    servertype = MultiSelectField(verbose_name="Sunucu tipi", help_text="├çok se├žim yapabilirsiniz", max_length=100, choices=servertype)
    ostype = MultiSelectField(verbose_name="─░┼čletim sistemi tipi", help_text="├çoklu se├žim yapabilirsiniz", max_length=100, choices=ostype)
    appservercount = models.PositiveIntegerField(verbose_name="Uygulama sunucu say─▒s─▒", default=0)
    serverhostnames = models.CharField(verbose_name="Sunucu bilgileri", max_length=300, default="")
    dbtype = MultiSelectField(verbose_name="Veritaban─▒ tipi", help_text="├çoklu se├žim yapabilirsiniz", max_length=100, choices=dbtype)
    dbconnstring = models.CharField(verbose_name="Veritaban─▒ ba─člant─▒ bilgisi", max_length=300, default="")
    monitoringapps = MultiSelectField(verbose_name="Hangi uygulamalar ile monitor ediliyor?", help_text="├çoklu se├žim yapabilirsiniz", choices=monitoringapps)
    logintegration = MultiSelectField(verbose_name="Log entegrasyonu var m─▒?", help_text="├çoklu se├žim yapabilirsiniz. Sunucu ├╝st├╝ndeki loglar yok olarak de─čerlendirilmelidir", choices=logintegration)
    logindex = models.CharField(verbose_name="Log index bilgisi nedir?", max_length=300, default="", blank=True) 
    supportdetail = MultiSelectField(verbose_name="Support detaylar─▒", help_text="├çoklu se├žim yapabilirsiniz", choices=supportdetail, max_length=100)
    integratedservices = MultiSelectField(verbose_name="Entegre oldu─ču uygulamalar/servisler", help_text="├çoklu se├žim yapabilirsiniz", blank=True, choices=integratedservices)
    other = models.CharField(verbose_name="Di─čerleri (E─čer yukar─▒daki se├ženeklerin d─▒┼č─▒nda bir entegrasyon varsa burada belirtiniz)", max_length=100, default="", blank=True)  
    sox = models.BooleanField(verbose_name="SOX kritik mi?", default=False)
    soxcriticdata = models.BooleanField(verbose_name="M├╝┼čteri kritik veri bar─▒nd─▒r─▒r m─▒? (├ľrne─čin; i┼člem detay─▒, adres bilgisi vs)", default=False)
    odmplatform = models.BooleanField(verbose_name="ODM platformu var m─▒?", default=False)
    highavailability = models.BooleanField(verbose_name="Kendi i├žinde yedeklilik (HA) var m─▒?", default=False)
    regulatoryintegration = models.BooleanField(verbose_name="D─▒┼č kurum entegrasyonu var m─▒?", default=False)
    customereffect = models.BooleanField(verbose_name="Servis kesintisi i├ž/d─▒┼č m├╝┼čteriyi etkiler mi?", default=False)
    backup = models.BooleanField(verbose_name="Uygulama sunucular─▒n─▒n backup'─▒ var m─▒?", default=False)

    def __str__(self):
        return self.servicename
