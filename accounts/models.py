from django.db import models
from django.core.exceptions import ValidationError
import uuid

# Create your models here.
class User(models.Model):
    '''Superlist user'''
    email = models.EmailField(primary_key=True, blank=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

#    def clean(self):
#        print(f'clean: "{self.email}"')
#        if self.email == '':
#            raise ValidationError('Empty email')
#
#    def save(self, *args, **kwargs):
#        self.full_clean()
#        return super(User, self).save(*args, **kwargs)

class Token(models.Model):
    '''auth token'''
    email = models.EmailField()
    uid = models.CharField(default=uuid.uuid4, max_length=40)
