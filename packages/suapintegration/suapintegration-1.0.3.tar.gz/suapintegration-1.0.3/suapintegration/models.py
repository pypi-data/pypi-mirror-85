from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from django.apps import apps as django_apps
from django.conf import settings
from django.dispatch import receiver
from django.db.models import Model, CharField, EmailField, BooleanField, DateTimeField, ForeignKey, CASCADE, TextChoices
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from social_django.models import UserSocialAuth


class AbstractSuapUser(AbstractUser):

    class Tipo(TextChoices):
        INDETERMINADO = 'Indeterminado', _('Indeterminado')
        ALUNO = 'Aluno', _('Aluno')
        SERVIDOR = 'Servidor', _('Servidor')
        TERCEIRO = 'Terceiro', _('Terceiro')

    class Categoria(TextChoices):
        NAO_SE_APLICA = 'Não se aplica', _('Não se aplica')
        INDETERMINADO = 'Indeterminado', _('Indeterminado')
        DOCENTE = 'Docente', _('Docente')
        TECNICO = 'Técnico Administrativo', _('Técnico Administrativo')
        ESTAGIARIO = 'Estagiário', _('Estagiário')

    username = CharField(_('username'), max_length=150, unique=True)
    password = CharField(_('password'), max_length=128, null=True, blank=True)
    name = CharField(_('name'), max_length=255, null=True, blank=True)
    social_name = CharField(_('social name'), max_length=255, null=True, blank=True)
    email = EmailField(_('email address'), null=True, blank=True)
    scholar_email = EmailField(_('scholar email address'), null=True, blank=True)
    academic_email = EmailField(_('academic email address'), null=True, blank=True)
    campus = CharField(_('campus'), max_length=255, null=True, blank=True)
    is_staff = BooleanField(_('staff status'), default=False, help_text=_('Can user the admin site?'),)
    is_active = BooleanField(_('active'), default=True)
    created_at = DateTimeField(_('date created'), auto_now_add=True)
    changed_at = DateTimeField(_('date changed'), auto_now=True)
    tipo = CharField(_('Tipo de usuário'), max_length=255, default=Tipo.INDETERMINADO, choices=Tipo.choices)
    categoria = CharField(_(
        'Categoria do servidor'), max_length=255, default=Categoria.NAO_SE_APLICA,
        choices=Categoria.choices
    )
    ano_ingresso = CharField(_('Ano de ingresso'), max_length=4, null=True, blank=True)
    periodo_ingresso = CharField(_('Período de ingresso'), max_length=1, null=True, blank=True)
    codigo_curso = CharField(_('Código do curso'), max_length=10, null=True, blank=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name']

    class Meta:
        ordering = ['name']
        abstract = True

    def __str__(self):
        return f'{self.name} ({self.username}) [{self.tipo}]'

    @property
    def is_aluno(self):
        return self.tipo == AbstractSuapUser.Tipo.ALUNO

    @property
    def is_servidor(self):
        return self.tipo == AbstractSuapUser.Tipo.SERVIDOR

    @property
    def is_terceiro(self):
        return self.tipo == AbstractSuapUser.Tipo.TERCEIRO

    @property
    def is_docente(self):
        return self.categoria == AbstractSuapUser.Categoria.DOCENTE

    @property
    def is_tecnico(self):
        return self.categoria == AbstractSuapUser.Categoria.TECNICO

    @property
    def is_estagiario(self):
        return self.categoria == AbstractSuapUser.Categoria.ESTAGIARIO

    @property
    def curso(self):
        try:
            Curso = django_apps.get_model(settings.SUAP_CURSO_MODEL, require_ready=False)
            return Curso.objects.filter(codigo=self.codigo_curso).first()
        except ValueError:
            raise ImproperlyConfigured("SUAP_CURSO_MODEL must be of the form 'app_label.model_name'")
        except LookupError:
            raise ImproperlyConfigured(
                "SUAP_CURSO_MODEL refers to model '%s' that has not been installed" %
                settings.SUAP_CURSO_MODEL
            )

    def _split_name(self):
        if self.name:
            splitted_name = self.name.split()
            self.first_name = ' '.join(splitted_name[:-1])
            self.last_name = splitted_name[-1] if len(splitted_name) > 1 else '.'

    def _discove_user_type(self, *args, **kwargs):
        update_fields = []
        if 'update_fields' in kwargs:
            update_fields = kwargs['update_fields'] + ['tipo', 'categoria']

        if not self.username.isdigit():
            self.tipo = AbstractSuapUser.Tipo.INDETERMINADO
            self.categoria = AbstractSuapUser.Categoria.NAO_SE_APLICA
            return

        if len(self.username) == 11:
            self.tipo = AbstractSuapUser.Tipo.TERCEIRO
            self.categoria = AbstractSuapUser.Categoria.NAO_SE_APLICA
        elif len(self.username) > 11:
            matricula = self.username
            self.tipo = AbstractSuapUser.Tipo.ALUNO
            self.categoria = AbstractSuapUser.Categoria.NAO_SE_APLICA
            self.ano_ingresso = matricula[0:4]
            self.periodo_ingresso = matricula[4:5]
            self.codigo_curso = matricula[5:-4]
            update_fields = []
            if 'update_fields' in kwargs:
                update_fields = update_fields + ['tipo', 'categoria']
        else:
            # TODO: Aguardar que o SUAP passe a dar esta infomração para então implementar aqui
            self.tipo = AbstractSuapUser.Tipo.SERVIDOR
            self.categoria = AbstractSuapUser.Categoria.INDETERMINADO
        return update_fields

    def save(self, *args, **kwargs):
        self._split_name()
        update_fields = self._discove_user_type(*args, **kwargs)
        if 'update_fields' in kwargs:
            kwargs['update_fields'] = update_fields
        super().save(*args, **kwargs)


class SuapUser(AbstractSuapUser):

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['name']
        abstract = False


class LoginHistory(Model):
    user = ForeignKey(get_user_model(), on_delete=CASCADE)
    login_at = DateTimeField(_('login at'), auto_now_add=True)
    ip = CharField(_('IP'), max_length=255)

    class Meta:
        verbose_name = _('User login history')
        verbose_name_plural = _('User logins history')
        ordering = ['-login_at']


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_socialauth_suap_user(sender, instance=None, created=False, **kwargs):
    if instance:
        UserSocialAuth.objects.update_or_create(user=instance, defaults={'provider': 'suap', 'uid': instance.username})
