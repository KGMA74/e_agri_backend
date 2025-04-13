from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field is required')

        extra_fields.setdefault('role', 'farmer')
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_staffuser(self, email, nickname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, nickname, password, **extra_fields)
    

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  
        return self.create_user(email, password, **extra_fields)