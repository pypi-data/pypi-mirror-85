from django.utils.translation import gettext as _
from django.contrib.admin import register, ModelAdmin, TabularInline
from django.contrib.auth import get_user_model
from suapintegration.models import LoginHistory


@register(LoginHistory)
class LoginHistoryAdmin(ModelAdmin):
    list_display = ('login_at', 'user', 'ip')
    search_fields = ('user__name', 'login_at')
    ordering = ('-login_at',)
    date_hierarchy = 'login_at'


class LoginHistoryInline(TabularInline):
    model = LoginHistory
    fields = ['login_at', 'ip']
    ordering = ['-login_at']
    readonly_fields = ['login_at', 'ip']
    extra = 0


class SuapUserMixinAdmin:
    list_display = ('username', 'name', 'email', 'campus', 'get_groups')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'campus', 'groups')
    search_fields = ('username', 'name', 'email')
    ordering = ['name']
    readonly_fields = [
        'name', 'social_name',
        'email', 'academic_email', 'scholar_email',
        'created_at', 'changed_at', 'last_login',
        'campus', 'tipo', 'categoria', 'ano_ingresso', 'periodo_ingresso', 'codigo_curso'
    ]

    class Names:
        fields = {'fields': ['username', 'name', 'social_name']}
        title = _('Nomes')

    class Vinculo:
        fields = {'fields': ['campus', 'tipo', 'categoria', 'ano_ingresso', 'periodo_ingresso', 'codigo_curso']}
        title = _('Vínculo')

    class Emails:
        fields = {'fields': ['email', 'academic_email', 'scholar_email']}
        title = _('E-Mails')

    class Permissoes:
        fields = {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups']}
        title = _('Permissões')

    class Datas:
        fields = {'fields': ['created_at', 'changed_at', 'last_login']}
        title = _('Datas')

    def get_groups(self, instance):
        result = ', '.join([x.name for x in instance.groups.all()])
        return f'{result}'


try:
    from tabbed_admin import TabbedModelAdmin
    @register(get_user_model())
    class SuapUserAdmin(SuapUserMixinAdmin, TabbedModelAdmin):
        tabs = [
            (SuapUserMixinAdmin.Names.title, [(None, SuapUserMixinAdmin.Names.fields)]),
            (SuapUserMixinAdmin.Vinculo.title, [(None, SuapUserMixinAdmin.Vinculo.fields)]),
            (SuapUserMixinAdmin.Emails.title, [(None, SuapUserMixinAdmin.Emails.fields)]),
            (SuapUserMixinAdmin.Permissoes.title, [(None, SuapUserMixinAdmin.Permissoes.fields)]),
            (SuapUserMixinAdmin.Datas.title, [(None, SuapUserMixinAdmin.Datas.fields), LoginHistoryInline]),
        ]
except ImportError:
    @register(get_user_model())
    class SuapUserAdmin(ModelAdmin):
        inlines = [LoginHistoryInline]

        fieldsets = [
            (None, SuapUserMixinAdmin.Names.fields),
            (SuapUserMixinAdmin.Vinculo.title, SuapUserMixinAdmin.Vinculo.fields),
            (SuapUserMixinAdmin.Emails.title, SuapUserMixinAdmin.Emails.fields),
            (SuapUserMixinAdmin.Permissoes.title, SuapUserMixinAdmin.Permissoes.fields),
            (SuapUserMixinAdmin.Datas.title, SuapUserMixinAdmin.Datas.fields),
        ]
