from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, **extra_args):
        from .models import User

        password = extra_args.pop('password', None)
        if password is None:
            raise Exception("Password is required!")
        user = User(**extra_args)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, **extra_kwargs):
        if email is None:
            raise Exception("email is required!")
        extra_kwargs['is_active'] = True
        extra_kwargs['is_staff'] = True
        extra_kwargs['is_superuser'] = True
        extra_kwargs['email'] = email

        if extra_kwargs.get('is_active') is False:
            raise Exception("is_active should be true for superuser")
        if extra_kwargs.get('is_staff') is False:
            raise Exception("is_staff should be true for superuser")
        if extra_kwargs.get('is_superuser') is False:
            raise Exception("is_superuser should be true for superuser")
        
        return self.create_user(**extra_kwargs)
