from django.db import models
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.validators import RegexValidator
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _


from .auth import generate_verify_email_token
from .validators import validate_gb_phone_number
from .MailFilter import filtered_send_mail
from django.core import signing
from datetime import timedelta

# remove username from the default django user model. (Creating a custom user model based on the original django model)
# email is used as the unique account 'username'
import logging
logger = logging.getLogger(__name__)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password,
                     is_staff, is_superuser, is_guest=False, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        email = self.normalize_email(email)
        try:
            user = self.model.objects.get(email=email, is_guest=True)

            user.update(is_staff=is_staff, is_active=True,
              is_superuser=is_superuser,
              is_guest=is_guest,
              date_joined=now,
              is_email_verified=False, **extra_fields)

        except self.model.DoesNotExist:
            user = self.model(email=email,
                              is_staff=is_staff,
                              is_active=True,
                              is_guest=is_guest,
                              is_superuser=is_superuser,
                              date_joined=now,
                              is_email_verified=False, **extra_fields)
        if password is None:
            password = self.make_random_password()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, is_guest=False, **extra_fields):
        return self._create_user(email, password, False, False, is_guest=is_guest,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(
        null=True,
        max_length=20,
        validators=[validate_gb_phone_number],
        blank=True
    )
    profile_pic = models.ImageField(blank=True, null=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    is_guest = models.BooleanField(_('guest'), default=False,
                                    help_text=_('Designates whether this user should be treated as '
                                                'Guest. Guest accounts are created for users who don\'t '
                                                'want to or can\'t create an account so it is created for them'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_email_verified = models.BooleanField(_('email verified'), default=False,
                                            help_text=_('Designates whether email has been verified '))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def _get_base_sg_context(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

    def send_verification_email(self, request=None):

        #safeguard if guest
        if self.is_guest:
            return

        preview = ''
        passkey = ''

        if request:
            if settings.ENABLE_PREVIEW and request.session.get('preview', None) is not None:
                preview = '&preview'

            signer = signing.TimestampSigner()

            for key in settings.PRIVATE_URL_ACCESS_KEYS:
                if key in request.COOKIES:
                    try:
                        signer.unsign(
                            request.COOKIES[key], max_age=timedelta(hours=settings.PRIVATE_URL_ACCESS_TIME))
                        passkey = f'&pass={key}'
                    except signing.BadSignature:
                        pass

        token = generate_verify_email_token(self.id, self.email)

        sg_context = {
            'first_name': self.first_name,
            'email': self.email,
            'last_name': self.last_name,
            'verify_url': f"{settings.SITE_URL}/account/verify?token={token}{preview}{passkey}"
        }

        return filtered_send_mail(
            '_',
            '_',
            '',
            [self.email],
            html_message='_',
            sg_template_id=settings.SG_TL_EMAIL_VERIFICATION,
            sg_context=sg_context
        )

    def send_password_reset_email(self):

        # safeguard if guest
        if self.is_guest:
            return

        uidb64 = urlsafe_base64_encode(force_bytes(self.pk))
        
        token = default_token_generator.make_token(self)

        url = f"{settings.SITE_URL}/account/reset-password-confirm"
        url += f"?uidb64={uidb64}&token={token}"

        sg_context = {
            'first_name': self.first_name,
            'url': url
        }

        filtered_send_mail(
            '_',
            '_',
            'support@rippleenergy.com',
            [self.email],
            html_message='_',
            sg_template_id=settings.SG_TL_RESET_PASSWORD,
            sg_context=sg_context
        )

    def send_password_changed_confirmed_email(self):
        # sends a confirmation to someone that their password has been changed
        # TODO red

        sg_context = {
            **self._get_base_sg_context()
        }
       
        return filtered_send_mail(
            '_',
            '_',
            '',
            [self.email],
            html_message='_',
            sg_template_id=settings.SG_TL_PASSWORD_CHANGED_CONFIRMED,
            sg_context=sg_context
        )

    def send_email_changed_email(self, old_email_address):
        """
        Sends email to a user's old email address 
        to notify that their email has been changed.
        """
        return
        sg_context = {
            'old_email': old_email_address,
            **self._get_base_sg_context()
        }

        return filtered_send_mail(
            '_',
            '_',
            '',
            [old_email_address],
            html_message='_',
            sg_template_id=settings.SG_TL_EMAIL_CHANGED_NOTIFY,
            sg_context=sg_context
        )


class RippleBase(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AssetBase(RippleBase):

    class Meta:
        abstract = True

    assetid = models.CharField(max_length=200, db_index=True)
    module = models.CharField(
        max_length=200, blank=True, default="", db_index=True)
    version = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.assetid


class TextAsset(AssetBase):

    text = models.CharField(max_length=1000, blank=True, default="")


class RichTextAsset(AssetBase):

    text = models.TextField(blank=True, default="")


class ImageAsset(AssetBase):

    target = models.CharField(max_length=200, default="", db_index=True)
    image = models.ImageField()


class Article(AssetBase):

    layout = models.CharField(
        max_length=200, blank=True, default="", db_index=True)
    image = models.ForeignKey(ImageAsset, on_delete=models.CASCADE)
    text = models.ForeignKey(RichTextAsset, on_delete=models.CASCADE)
    title = models.ForeignKey(TextAsset, on_delete=models.CASCADE)


class ArticleCollection(AssetBase):

    layout = models.CharField(
        max_length=200, blank=True, default="", db_index=True)

    image = models.ForeignKey(ImageAsset, on_delete=models.CASCADE)
    text = models.ForeignKey(RichTextAsset, on_delete=models.CASCADE)
    title = models.ForeignKey(TextAsset, on_delete=models.CASCADE)

    articles = models.ManyToManyField(Article, through='ArticleOrder')
    article_collections = models.ManyToManyField('ArticleCollection', through='ArticleCollectionOrder',
                                                 through_fields=('container_article_collection', 'article_collection'))


class ArticleOrder(models.Model):

    article_collection = models.ForeignKey(
        ArticleCollection, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    order = models.IntegerField()


class ArticleCollectionOrder(models.Model):

    container_article_collection = models.ForeignKey(
        ArticleCollection, related_name="container_articles", on_delete=models.CASCADE)
    article_collection = models.ForeignKey(
        ArticleCollection, related_name="contained_articles", on_delete=models.CASCADE)
    order = models.IntegerField()


class FeatureOption(RippleBase):

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank=True, default='')
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class FeatureUrl(RippleBase):

    description = models.CharField(max_length=200, blank=True, default='')
    feature = models.ForeignKey(
        FeatureOption, related_name='urls', on_delete=models.CASCADE)
    regex = models.TextField(max_length=800)

    def __str__(self):
        return "{} {}".format(self.feature.name, self.regex[:20])
