from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, phone=None, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Email is required")
        
        # if not password:
        #     raise ValueError("Password is required")
        
        user = self.model(
            # username=username,
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            phone = phone
        )
        user.set_password(password)
        user.active = is_active
        user.staff = is_staff
        user.admin = is_admin

        user.save(using=self._db)

        return user
    
    def create_staffuser(self, email, first_name=None, last_name=None, phone=None, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            # username=username,
            password = password,
            is_staff = True
        )

        return user
    
    def create_superuser(self, email, first_name=None, last_name=None, phone=None, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            # username=username,
            password = password,
            is_staff = True,
            is_admin = True
        )

        return user

class User(AbstractBaseUser):
    # username = models.CharField(unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email or ''
    
    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name or ''
    
    @property
    def is_staff(self):
        return self.staff
    
    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active
    
    def has_perm(self, perm, obj=None):
        return self.admin
    
    def has_module_perms(self, app_label):
        return True
    
    # def get_by_natural_key(self, email):
    #     return self.get(email=email)

    def get_by_natural_key(self, email):
        return self.get(email=email)
    

class Photo(models.Model):
    image = models.ImageField(upload_to='task_photos')

    def __str__(self):
        return f'Photo {self.pk}'

    
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    photos = models.ManyToManyField(Photo, blank=True)

    PRIORITY_CHOICES = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
