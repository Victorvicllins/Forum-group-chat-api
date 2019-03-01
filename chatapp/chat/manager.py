from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, first_name, last_name, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Email is required')
        if not first_name:
            raise ValueError('User must fill in name')
        if not last_name:
            raise ValueError('User must fill in last name')
        if not password:
            raise ValueError('Enter password.')
        user_obj = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True
        )

        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_admin = True
        )

        return user

