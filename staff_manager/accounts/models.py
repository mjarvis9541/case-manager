from django.db import models
from django.utils import timezone
# from django.utils.http import urlquote
from django.utils.translation import gettext_lazy as _
# from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from staff_manager.productivity.models import Department

from django.db.models import ExpressionWrapper, F, Func, Q, Sum
from django.db.models.functions import Coalesce, Round, ExtractYear, ExtractWeek



class UserStats(models.QuerySet):
    today = timezone.now()
    week_number = timezone.now().isocalendar()[1]

    # gets the total mins the user has producted today
    def total_mins_today(self):
        return self.filter(user_case__date=self.today).aggregate(total=Coalesce(Sum('user_case__case_type__minutes'),0))['total']

    # gets the total mins the user has producted this week
    def total_mins_week(self):
        return self.filter(user_case__date__week=self.week_number).aggregate(total=Coalesce(Sum('user_case__case_type__minutes'),0))['total']

    def total_mins(self):
        return self.aggregate(total=Coalesce(Sum('user_case__case_type__minutes'),0))['total']

    def total_pct(self):
        return round(self.total_mins() / 450 * 100, 1)


    def mins(self):
        return self.annotate(
            mins=F('user_case__case_type__minutes').aggregate(total=Sum('mins'))['total']
        )



class UserManager(BaseUserManager):
    def _create_user(self, username, password, is_staff, is_superuser):
        """
        Creates and saves a user with the given username and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The username must be set')
        user = self.model(
            username=username,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None):
        return self._create_user(username, password, False, False)

    def create_superuser(self, username, password):
        return self._create_user(username, password, True, True)


class User(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """

    username = models.CharField(_('username'), max_length=30, unique=True)
    email = models.EmailField(_('email'), max_length=255, unique=True, null=True, blank=True) # 254 / 255?
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin ' 'site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as '
            'active. Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    
    objects = UserManager()
    query = UserStats.as_manager()
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    # def get_absolute_url(self):
    #     return '/users/%s/' % urlquote(self.email)

    @property
    def total_mins_today(self):
        return self.query.total_mins()


    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        'Returns the short name for the user.'
        return self.first_name

    # def email_user(self, subject, message, from_email=None):
    #     """
    #     Sends an email to this User.
    #     """
    #     send_mail(subject, message, from_email, [self.email])