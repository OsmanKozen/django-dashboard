from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*.com.tr"]

# Fetch Service User's password from CyberArk

# Dashboard CyberArk informations
cyberark_url = config('PROD_CYBERARK_URL')
cyberark_appid = config('PROD_CYBERARK_APPID')
cyberark_safename = config('PROD_CYBERARK_SAFENAME')

# CyberArk Object names
cyberark_ldap_object = config('PROD_CYBERARK_LDAP_OBJECT')
cyberark_mssql_object = config('PROD_CYBERARK_MSSQL_OBJECT')

# CyberArk URL's
cyberark_ldap_url = f"https://{cyberark_url}/AIMWebService/api/Accounts?AppID={cyberark_appid}&Query=Safe={cyberark_safename};Object={cyberark_ldap_object}"
cyberark_mssql_url = f"https://{cyberark_url}/AIMWebService/api/Accounts?AppID={cyberark_appid}&Query=Safe={cyberark_safename};Object={cyberark_mssql_object}"

# Send request to URL's
cyberark_request_ldap = requests.get(cyberark_ldap_url)
cyberark_ldap_response = cyberark_request_ldap.json()
cyberark_ldap_password = cyberark_ldap_response['Content']

cyberark_request_mssql = requests.get(cyberark_mssql_url)
cyberark_mssql_response = cyberark_request_mssql.json()
cyberark_mssql_password = cyberark_mssql_response['Content']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': config('MSSQL_PROD_NAME'),
        'USER': config('MSSQL_PROD_USERNAME'),
        'PASSWORD': cyberark_mssql_password,
        'HOST': config('MSSQL_PROD_HOST'),
        'PORT': config('MSSQL_PROD_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 60 * 60 * 24  # one day

# LDAP Configuration

AUTHENTICATION_BACKENDS = [
    "django_python3_ldap.auth.LDAPBackend",
]

# The URL of the LDAP server(s).  List multiple servers for high availability ServerPool connection.
LDAP_AUTH_URL = [config('PROD_LDAP_AUTH_URL')]

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = False

# Specify which TLS version to use (Python 3.10 requires TLSv1 or higher)
import ssl
LDAP_AUTH_TLS_VERSION = ssl.PROTOCOL_TLSv1_2

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = config('PROD_LDAP_AUTH_SEARCH_BASE')

# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = "user"

# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    "username": "sAMAccountName",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)

# Path to a callable that takes a dict of {model_field_name: value},
# returning a dict of clean model data.
# Use this to customize how data loaded from LDAP is saved to the User model.
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"

# Path to a callable that takes a user model, a dict of {ldap_field_name: [value]}
# a LDAP connection object (to allow further lookups), and saves any additional
# user relationships based on the LDAP data.
# Use this to customize how data loaded from LDAP is saved to User model relations.
# For customizing non-related User model fields, use LDAP_AUTH_CLEAN_USER_DATA.
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"

# Path to a callable that takes a dict of {ldap_field_name: value},
# returning a list of [ldap_search_filter]. The search filters will then be AND'd
# together when creating the final search filter.
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

# Path to a callable that takes a dict of {model_field_name: value}, and returns
# a string of the username to bind to the LDAP server.
# Use this to support different types of LDAP server.
# LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_openldap"
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"
# LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory_principal"

# Sets the login domain for Active Directory users.
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = config('PROD_LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN')

# The LDAP username and password of a user for querying the LDAP database for user
# details. If None, then the authenticated user will be used for querying, and
# the `ldap_sync_users`, `ldap_clean_users` commands will perform an anonymous query.
LDAP_AUTH_CONNECTION_USERNAME = config('PROD_LDAP_AUTH_CONNECTION_USERNAME')
LDAP_AUTH_CONNECTION_PASSWORD = cyberark_ldap_password

# Set connection/receive timeouts (in seconds) on the underlying `ldap3` library.
LDAP_AUTH_CONNECT_TIMEOUT = config('PROD_LDAP_AUTH_CONNECT_TIMEOUT', cast=int)
LDAP_AUTH_RECEIVE_TIMEOUT = config('PROD_LDAP_AUTH_RECEIVE_TIMEOUT', cast=int)

# Logging

LOGGING ={
    'version':1,
    'loggers':{
        'django':{
            'handlers':['file'],
            'level':'DEBUG'
        }
    },
    'handlers':{
        'file':{
            'level':'INFO',
            'class': 'logging.FileHandler',
            'filename':'./logs/info.log',
            'formatter':'simpleRe',
        }
    },
    'formatters':{
        'simpleRe': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        }
    }
}