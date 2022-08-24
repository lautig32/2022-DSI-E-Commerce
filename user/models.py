from django.contrib.auth.models import User, AbstractUser
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.db import models
# from django_upload_path.upload_path import auto_cleaned_path_stripped_uuid4


class UserProfile(AbstractUser):
    email = models.EmailField(_('email address'), blank=False, null=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=150, blank=False)
    document_number = models.CharField(verbose_name="documento", max_length=30, null=True, blank=True)
    #profile_picture = models.ImageField(_('foto de perfil'), upload_to=auto_cleaned_path_stripped_uuid4, null=True,
    #                                   blank=True)
    description = models.TextField(_("descripción"), blank=True)

    SUBSCRIBER = 'Subscriber'
    LECTURER = 'Lecturer'
    EVALUATOR = 'Evaluator'
    COLLABORATOR = 'Collaborator'
    ORGANIZER = 'Organizer'

    USER_TYPE_CHOICES_COLLABORATOR = (
        (SUBSCRIBER, 'Suscriptor'),
        (LECTURER, 'Disertante'),
        (EVALUATOR, 'Evaluador'),
    )

    USER_TYPE_CHOICES_ORGANIZER = (
        (SUBSCRIBER, 'Suscriptor'),
        (LECTURER, 'Disertante'),
        (COLLABORATOR, 'Colaborador'),
        (EVALUATOR, 'Evaluador'),
    )

    USER_TYPE_CHOICES = (
        (SUBSCRIBER, 'Suscriptor'),
        (LECTURER, 'Disertante'),
        (COLLABORATOR, 'Colaborador'),
        (ORGANIZER, 'Organizador'),
        (EVALUATOR, 'Evaluador'),
    )

    user_type = models.CharField(_('tipo'), max_length=15, choices=USER_TYPE_CHOICES, default=LECTURER)

    is_staff = models.BooleanField(
        _("staff status"),
        default=True,
        help_text=_("Designates whether the user can log into this admin site."),
    )

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def profile_picture_short_tag(self):
        if self.profile_picture:
            url_image = self.profile_picture.url
            return format_html("""<img src='{}' width='40'"/>""", url_image)
        return "-"
    profile_picture_short_tag.short_description = _('foto de perfil')
    profile_picture_short_tag.allow_tags = True

    def profile_picture_medium_tag(self):
        if self.profile_picture:
            url_image = self.profile_picture.url
            return format_html("""<img src='{}' height='160'"/>""", url_image)
        return "-"
    profile_picture_medium_tag.short_description = _('foto de perfil')
    profile_picture_medium_tag.allow_tags = True

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        if not self.password:
            self.set_password(str(self.document_number))
        super(UserProfile, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.is_active:
            self.is_active = False
            self.save()
        else:
            super(UserProfile, self).delete(using, keep_parents)

    def __str__(self):
        if self.document_number:
            return "%s - %s" % (self.get_full_name(), self.document_number)
        else:
            return self.get_full_name()
