from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from embed_video.fields import EmbedVideoField


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):


    username = models.CharField(max_length=150, unique=True)
    email = models.CharField(max_length=100)
    regNo = models.CharField(max_length=50, unique=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'regNo']



class Book(models.Model):

    book_category = models.CharField(max_length=20)
    book_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    number_of_books = models.IntegerField()
    book_type = models.CharField(max_length=50, null=False)
    document =models.FileField(upload_to = 'files/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.book_name
    

class Borrowing(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowing_date = models.DateField()
    returning_date = models.DateField(null=True, blank=True)
    is_borrowed = models.BooleanField(default=False)
    DisplayFields = ['student', 'book','borrowing_date', 'returning_date', 'fine']

    def save(self, *args, **kwargs):

        if self.is_borrowed == True:
            # Call the superclass's save method to perform the actual save operation
            super().save(*args, **kwargs)

            # Reduce the number of available copies of the borrowed book by 1
            self.book.number_of_books -= 1
            self.book.save()
        elif self.is_borrowed == False:
            # Call the superclass's save method to perform the actual save operation
            super().save(*args, **kwargs)

            # increase the number of available copies of the borrowed book by 1
            self.book.number_of_books += 1
            self.book.save()
        else:
            raise ValueError('is_borrowed must be either True or False')

    @property
    def fine(self):
        due_fine = 0.00  # Initialize due_fine to 0.00
        if self.is_borrowed and self.returning_date and self.returning_date < timezone.now().date():
            # Calculate the number of days overdue
            days_overdue = (timezone.now().date() - self.returning_date).days
            # Check if the student is a staff member
            if self.student.username.startswith("staff"):
                # Update due_fine for staff (20 bob per day)
                due_fine = days_overdue * 20
            else:
                # Update due_fine for students (10 bob per day)
                due_fine = days_overdue * 10
            return "Ksh {:.2f}".format(due_fine)
        else:
            return "Ksh {:.2f}".format(due_fine)

    def __str__(self):
        return f"{self.student.username} borrowed '{self.book.book_name}'"

    


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class supplier(models.Model):
    company_name = models.CharField(max_length=70)
    book_tittle = models.CharField(max_length=50)
    number_of_books = models.IntegerField()
    delivery_date = models.DateField()
    contact = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.company_name
    
class Reaches(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70)
    message = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    company_name = models.CharField(max_length=70)
    book_tittle = models.CharField(max_length=50)
    num_books = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.company_name
    

class Video(models.Model):
    video_name = models.CharField(max_length=40)
    category = models.CharField(max_length=20)
    video = EmbedVideoField()  # same like models.URLField()

    def __str__(self):
        return self.video_name
    