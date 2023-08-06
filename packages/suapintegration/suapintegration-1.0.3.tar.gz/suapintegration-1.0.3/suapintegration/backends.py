from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from django.core.exceptions import FieldDoesNotExist
from social_core.backends.oauth import BaseOAuth2
from suapintegration import get_setting
from suapintegration.models import LoginHistory


def set_mapping(mapping, fieldname, response, key):
    try:
        User = get_user_model()
        User._meta.get_field(fieldname)
        if key in response:
            mapping[fieldname] = response[key]
        else:
            mapping[fieldname] = None
    except FieldDoesNotExist:
        mapping[fieldname] = None


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')


class SuapOAuth2(BaseOAuth2):
    name = 'suap'
    AUTHORIZATION_URL = get_setting('SOCIAL_AUTH_SUAP_AUTHORIZATION_URL')
    ACCESS_TOKEN_METHOD = get_setting('SOCIAL_AUTH_SUAP_ACCESS_TOKEN_METHOD')
    ACCESS_TOKEN_URL = get_setting('SOCIAL_AUTH_SUAP_ACCESS_TOKEN_URL')
    ID_KEY = get_setting('SOCIAL_AUTH_SUAP_ID_KEY')
    RESPONSE_TYPE = get_setting('SOCIAL_AUTH_SUAP_RESPONSE_TYPE')
    REDIRECT_STATE = get_setting('SOCIAL_AUTH_SUAP_REDIRECT_STATE')
    STATE_PARAMETER = get_setting('SOCIAL_AUTH_SUAP_STATE_PARAMETER')
    USER_DATA_URL = get_setting('SOCIAL_AUTH_SUAP_USER_DATA_URL')
    AUTO_CREATE = get_setting('SOCIAL_AUTH_SUAP_AUTO_CREATE')
    AUTO_CREATE_AS_STAFF = get_setting('SOCIAL_AUTH_SUAP_AUTO_CREATE_AS_STAFF')

    def user_data(self, access_token, *args, **kwargs):
        return self.request(
            url=self.USER_DATA_URL,
            data={'scope': kwargs['response']['scope']},
            method='GET',
            headers={'Authorization': 'Bearer {0}'.format(access_token)}
        ).json()

    def get_user_details(self, response):

        User = get_user_model()
        username = response[self.ID_KEY]

        mapping = {}
        set_mapping(mapping, 'username', response, self.ID_KEY)
        set_mapping(mapping, 'name', response, 'nome')
        set_mapping(mapping, 'social_name', response, 'nome_social')
        set_mapping(mapping, 'email', response, 'email')
        set_mapping(mapping, 'scholar_email', response, 'email_google_classroom')
        set_mapping(mapping, 'academic_email', response, 'email_academico')
        set_mapping(mapping, 'campus', response, 'campus')
        mapping['is_active'] = True

        user = User.objects.filter(username=username).first()
        if user is None:
            if self.AUTO_CREATE:
                mapping['is_staff'] = self.AUTO_CREATE_AS_STAFF
                if User.objects.count() == 0:
                    mapping['is_superuser'] = True
                    mapping['is_staff'] = True
                user = User.objects.create(**mapping)
            else:
                raise Exception(_("Usuário não cadastrado."))
        LoginHistory.objects.create(user=user, ip=get_client_ip(self.strategy.request))
        return mapping
