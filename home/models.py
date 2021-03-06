from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .validators import validate_file_size

User = get_user_model()


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Request(models.Model):

    SICK_LEAVE = 'Sick Leave'
    COMPASSIONATE_LEAVE = 'Compassionate Leave'
    DEPENDANT_LEAVE = 'Dependant Leave'
    PARENTAL_LEAVE = 'Parental Leave'
    STUDY_LEAVE = 'Study Leave'
    OTHER_PAID_LEAVE = 'Other paid leave'
    OTHER_UNPAID_LEAVE = 'Other unpaid leave'
    SABBATICAL_LEAVE = 'Sabbatical Leave'

    LEAVE_TYPE = (
        (SICK_LEAVE, 'Sick Leave'),
        (COMPASSIONATE_LEAVE, 'Compassionate Leave'),
        (DEPENDANT_LEAVE, 'Dependant Leave'),
        (PARENTAL_LEAVE, 'Parental Leave'),
        (STUDY_LEAVE, 'Study Leave'),
        (OTHER_PAID_LEAVE, 'Other paid leave'),
        (OTHER_UNPAID_LEAVE, 'Other unpaid leave'),
        (SABBATICAL_LEAVE, 'Sabbatical Leave'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    leave_type = models.CharField(max_length=40, choices=LEAVE_TYPE, default=SICK_LEAVE)
    start = models.DateField()
    end = models.DateField()
    reason = models.TextField(max_length=500)
    status = models.CharField(max_length=10, default='Pending')
    attachment = models.FileField(upload_to=user_directory_path, null=True, validators=[validate_file_size])
    comment = models.TextField(max_length=250, default="")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % self.attachment

    def get_extension(self):
        return self.__str__().split('.').pop()

    def get_status(self):
        return '%s' % self.status

    def get_attachment(self):
        return '%s' % self.attachment

    def get_leave_type(self):
        return '%s' % self.leave_type

    def get_updated_at(self):
        return '%s' % self.updated_at


class RequesterManager(models.Manager):
    def get_authorisers(self):
        queryset = list(User.objects.filter(user_role='Authoriser').values_list('id', 'username'))

        return queryset


class Template(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    template_name = models.CharField(max_length=40)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    leave_type = models.CharField(max_length=20)
    start = models.CharField(max_length=20)
    end = models.CharField(max_length=20)
    reason = models.TextField(max_length=500)
    comment = models.TextField(max_length=250, default="")
    attachment = models.FileField(upload_to=user_directory_path, null=True, validators=[validate_file_size])

    def __str__(self):
        return '%s' % self.template_name

    def get_attachment(self):
        return '%s' % self.attachment


class Authoriser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % self.user


class Requester(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assigned_authoriser = models.ForeignKey(Authoriser, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '%s' % self.user


class Restriction(models.Model):
    user = models.ForeignKey(Requester, on_delete=models.CASCADE, null=True, blank=True)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField(max_length=250)

    def __str__(self):
        return '%s' % self.id

    def get_from_date(self):
        return '%s' % self.from_date

    def get_to_date(self):
        return '%s' % self.to_date


class Event(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    organizer = models.CharField(max_length=100)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    def get_id(self):
        return '%s' % self.id


# creates a requester model object if created user's role is 'Requester'
@receiver(post_save, sender=User)
def create_requester(sender, instance, created, **kwargs):
    if created and instance.user_role == 'Requester':
        Requester.objects.create(user=instance)


# creates an authoriser model object if created user's role is 'Authoriser'
@receiver(post_save, sender=User)
def create_authoriser(sender, instance, created, **kwargs):
    if created and instance.user_role == 'Authoriser':
        Authoriser.objects.create(user=instance)


post_save.connect(create_authoriser, sender=User)
post_save.connect(create_requester, sender=User)
