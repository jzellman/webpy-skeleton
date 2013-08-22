import hashlib
from datetime import datetime

import peewee as pw
from playhouse.signals import Model, pre_save

import config

DoesNotExist = pw.DoesNotExist
SelectQuery = pw.SelectQuery


def better_get(self, **kwargs):
    if kwargs:
        return self.filter(**kwargs).get()
    clone = self.paginate(1, 1)
    try:
        return clone.execute().next()
    except StopIteration:
        raise self.model_class.DoesNotExist(
            'instance matching query does not exist:\nSQL: %s\nPARAMS: %s' % (
                self.sql()))

pw.SelectQuery.get = better_get


class BaseModel(Model):
    created_at = pw.DateTimeField(default="now()")

    class Meta:
        database = config.db

    def update_fields(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)
        return self.save()


class User(BaseModel):
    email = pw.CharField(max_length=200, null=False)
    crypted_password = pw.CharField(max_length=40, null=False)
    salt = pw.CharField(max_length=40, null=False)
    remember_token = pw.CharField(max_length=64, null=True)

    def authenticate(self, password):
        return self.crypted_password == crypt_password(password,
                                                       self.salt)

    def __unicode__(self):
        return unicode(self.email)


def create_salt(email):
    return hashlib.md5("--%s--%s--" % (datetime.now(),
                                       email)).hexdigest()


def crypt_password(password, salt):
    return hashlib.md5("--%s--%s--" % (salt, password)).hexdigest()


# Fix reloading during development :-/
try:
    pre_save.disconnect(name='crypt_password_before_save')
except:
    pass


@pre_save(sender=User)
def crypt_password_before_save(model_class, instance, created):
    if not instance.password:
        return
    if not instance.salt:
        instance.salt = create_salt(instance.email)
    instance.crypted_password = crypt_password(instance.password,
                                               instance.salt)
