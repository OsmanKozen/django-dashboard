from django.db import models
from multiselectfield import MultiSelectField

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
    ('Veritabanı yok', 'Veritabanı yok'),
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
    ('CyberArk', 'CyberArk'),
    ('Coolgen', 'Coolgen'),
    ('ARK', 'ARK'),
    ('DWH(Raporlama)', 'DWH(Raporlama)'),
    ('STEP', 'STEP'),
    ('Ödeme Sistemleri', 'Ödeme Sistemleri'),
    ('Diğer', 'Diğer'),
)

class Services(models.Model):

    serviceid = models.PositiveIntegerField(verbose_name="Service ID", default=0)
    servicename = models.CharField(verbose_name="Servis adı", max_length=100, default="")
    teamname = models.CharField(verbose_name="Ekip adı", max_length=100, default="", editable=False)
    sre = models.CharField(verbose_name="SRE", max_length=100)
    srebackup = models.CharField(verbose_name="SRE Yedek", max_length=100)
    vendor = models.CharField(verbose_name="Vendor", help_text="GT ya da 'Firma adı' giriniz ", max_length=100, default="")
    serverlocation = MultiSelectField(verbose_name="Sunucu lokasyonu", help_text="Çoklu seçim yapabilirsiniz", max_length=100, choices=servicelocation)
    nonprodenvtypes = MultiSelectField(verbose_name="Production dışında hangi ortamlar var?", help_text="Çoklu seçim yapabilirsiniz", choices=nonprodenvtypes)
    servertype = MultiSelectField(verbose_name="Sunucu tipi", help_text="Çok seçim yapabilirsiniz", max_length=100, choices=servertype)
    ostype = MultiSelectField(verbose_name="İşletim sistemi tipi", help_text="Çoklu seçim yapabilirsiniz", max_length=100, choices=ostype)
    appservercount = models.PositiveIntegerField(verbose_name="Uygulama sunucu sayısı", default=0)
    serverhostnames = models.CharField(verbose_name="Sunucu bilgileri", max_length=300, default="")
    dbtype = MultiSelectField(verbose_name="Veritabanı tipi", help_text="Çoklu seçim yapabilirsiniz", max_length=100, choices=dbtype)
    dbconnstring = models.CharField(verbose_name="Veritabanı bağlantı bilgisi", max_length=300, default="")
    monitoringapps = MultiSelectField(verbose_name="Hangi uygulamalar ile monitor ediliyor?", help_text="Çoklu seçim yapabilirsiniz", choices=monitoringapps)
    logintegration = MultiSelectField(verbose_name="Log entegrasyonu var mı?", help_text="Çoklu seçim yapabilirsiniz. Sunucu üstündeki loglar yok olarak değerlendirilmelidir", choices=logintegration)
    logindex = models.CharField(verbose_name="Log index bilgisi nedir?", max_length=300, default="", blank=True) 
    supportdetail = MultiSelectField(verbose_name="Support detayları", help_text="Çoklu seçim yapabilirsiniz", choices=supportdetail, max_length=100)
    integratedservices = MultiSelectField(verbose_name="Entegre olduğu uygulamalar/servisler", help_text="Çoklu seçim yapabilirsiniz", blank=True, choices=integratedservices)
    other = models.CharField(verbose_name="Diğerleri (Eğer yukarıdaki seçeneklerin dışında bir entegrasyon varsa burada belirtiniz)", max_length=100, default="", blank=True)  
    sox = models.BooleanField(verbose_name="SOX kritik mi?", default=False)
    soxcriticdata = models.BooleanField(verbose_name="Müşteri kritik veri barındırır mı? (Örneğin; işlem detayı, adres bilgisi vs)", default=False)
    odmplatform = models.BooleanField(verbose_name="ODM platformu var mı?", default=False)
    highavailability = models.BooleanField(verbose_name="Kendi içinde yedeklilik (HA) var mı?", default=False)
    regulatoryintegration = models.BooleanField(verbose_name="Dış kurum entegrasyonu var mı?", default=False)
    customereffect = models.BooleanField(verbose_name="Servis kesintisi iç/dış müşteriyi etkiler mi?", default=False)
    backup = models.BooleanField(verbose_name="Uygulama sunucularının backup'ı var mı?", default=False)

    def __str__(self):
        return self.teamname, self.sre, self.servicename
