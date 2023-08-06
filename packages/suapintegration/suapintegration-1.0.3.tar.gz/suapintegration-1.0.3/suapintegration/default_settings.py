from sc4py.env import env, env_as_bool, env_as_list

name = "suapintegration"

SOCIAL_AUTH_SUAP_KEY = env('SOCIAL_AUTH_SUAP_KEY', 'changeme')
SOCIAL_AUTH_SUAP_SECRET = env('SOCIAL_AUTH_SUAP_SECRET', 'changeme')
SOCIAL_AUTH_SUAP_AUTHORIZATION_URL = env('SOCIAL_AUTH_SUAP_AUTHORIZATION_URL', 'https://suap.ifrn.edu.br/o/authorize/')
SOCIAL_AUTH_SUAP_ACCESS_TOKEN_METHOD = env('SOCIAL_AUTH_SUAP_ACCESS_TOKEN_METHOD', 'POST')
SOCIAL_AUTH_SUAP_ACCESS_TOKEN_URL = env('SOCIAL_AUTH_SUAP_ACCESS_TOKEN_URL', 'https://suap.ifrn.edu.br/o/token/')
SOCIAL_AUTH_SUAP_ID_KEY = env('SOCIAL_AUTH_SUAP_ID_KEY', 'identificacao')
SOCIAL_AUTH_SUAP_RESPONSE_TYPE = env('SOCIAL_AUTH_SUAP_RESPONSE_TYPE', 'code')
SOCIAL_AUTH_SUAP_REDIRECT_STATE = env_as_bool('SOCIAL_AUTH_SUAP_REDIRECT_STATE', True)
SOCIAL_AUTH_SUAP_STATE_PARAMETER = env_as_bool('SOCIAL_AUTH_SUAP_STATE_PARAMETER', True)
SOCIAL_AUTH_SUAP_USER_DATA_URL = env('SOCIAL_AUTH_SUAP_USER_DATA_URL', 'https://suap.ifrn.edu.br/api/eu/')
SOCIAL_AUTH_SUAP_AUTO_CREATE = env_as_bool('SOCIAL_AUTH_SUAP_AUTO_CREATE', False)
SOCIAL_AUTH_SUAP_AUTO_CREATE_AS_STAFF = env_as_bool('SOCIAL_AUTH_SUAP_AUTO_CREATE_AS_STAFF', False)
SOCIAL_AUTH_SUAP_EXTRA_CONTEXT_PROCESSORS = env_as_list('SOCIAL_AUTH_SUAP_EXTRA_CONTEXT_PROCESSORS',
                                                        'social_django.context_processors.backends,'
                                                        'social_django.context_processors.login_redirect')

SUAPINTEGRATION_APPS = env_as_list('SUAPINTEGRATION_APPS', 'suapintegration,social_django')
AUTHENTICATION_BACKENDS = env_as_list('DJANGO_AUTHENTICATION_BACKENDS', 'suapintegration.backends.SuapOAuth2')
AUTH_USER_MODEL = env('DJANGO_AUTH_USER_MODEL', 'suapintegration.SuapUser')
LOGIN_URL = env('DJANGO_LOGIN_URL', '/oauth/login/suap/')
LOGIN_REDIRECT_URL = env('DJANGO_LOGIN_REDIRECT_URL', '/')
LOGOUT_URL = env('DJANGO_LOGOUT_URL', '/logout/')
LOGOUT_REDIRECT_URL = env("DJANGO_LOGOUT_REDIRECT_URL", LOGIN_REDIRECT_URL)
