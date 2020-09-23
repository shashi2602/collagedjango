from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from embed_video.fields import EmbedVideoField
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.utils import timezone

LIST_YEARS=(
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
)
LIST_SEM=(
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
    ("6","6"),
    ("7","7"),
    ("8","8"),
)
LIST_GROUP=(
    ("CSE","CSE"),
    ("MEC","MEC"),
    ("EEE","EEE"),
    ("ECE","ECE"),
    ("CIVIL","CIVIL"),




)

class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    isfaculty=models.BooleanField(default=False)
    def __str__(self):
        return self.name.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(name=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Years(models.Model):
    year=models.CharField(max_length=100)
     
    def __str__(self):
        return self.year

class Sem(models.Model):
    sem=models.CharField(max_length=100)
     
    def __str__(self):
        return self.sem

class Dept(models.Model):
    name=models.CharField(max_length=200)
    shortname=models.CharField(max_length=100)
    def __str__(self):
        return self.name



class Student(models.Model):
    name=models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    year=models.CharField(choices=LIST_YEARS,default=1,max_length=100)
    sem=models.CharField(choices=LIST_SEM,default=4,max_length=100)
    dept=models.CharField(choices=LIST_GROUP,default="CSE",max_length=100)
    def __str__(self):
        return self.name.name.username

class Faculty(models.Model):
    name=models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    group=models.CharField(choices=LIST_GROUP,default=1,max_length=100)
    def __str__(self):
        return self.name.name.username

class Subjects(models.Model):
    dept=models.ForeignKey(Dept,on_delete=models.CASCADE,null=True)
    sub_name=models.CharField(max_length=500,default="")
    short_name=models.CharField(max_length=200,default="")
    year=models.CharField(choices=LIST_YEARS,default=1,max_length=100)
    notes_pdf_url=models.FileField(upload_to="subject")
    def __str__(self):
        return self.sub_name
    

class Notes(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    Subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    year=models.CharField(choices=LIST_YEARS,default=1,max_length=100)
    sem=models.CharField(choices=LIST_SEM,default=4,max_length=100)
    dept=models.ForeignKey(Dept,on_delete=models.CASCADE)
    chapter_name=models.CharField(max_length=1000)
    topic_name=models.CharField(max_length=1000)
    video_clip_url=EmbedVideoField(blank=True,default="")
    PDF_url=models.FileField(upload_to="notes",blank=True)
    date=models.DateTimeField(default=timezone.now)
    slug_c = models.SlugField(null=True, blank=True)
    slug_t = models.SlugField(null=True, blank=True)
    notes=RichTextUploadingField(null=True,blank=True)

    def __str__(self):
        return self.Subject.short_name

    def save(self, *args, **kwargs):
        if self.slug_c==None and self.slug_t==None:
            slug1 = slugify(self.chapter_name)
            slug2=slugify(self.topic_name)
            has_slug = Notes.objects.filter(slug_c=slug1,slug_t=slug2).exists()
            count = 1
            while has_slug:
                count += 1
                slug1 = slugify(self.chapter_name) + '-' + str(count)
                slug2 = slugify(self.topic_name) + '-' + str(count) 
                has_slug = Notes.objects.filter(slug_c=slug1,slug_t=slug2).exists()
            self.slug_c = slug1
            self.slug_t =slug2

        super().save(*args, **kwargs)
			

    def get_absolute_url(self):
        return reverse("dashboard")



class Questions(models.Model):
    question=models.CharField(max_length=1000)
    year=models.CharField(choices=LIST_YEARS,default=1,max_length=100)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    dept=models.ForeignKey(Dept,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)
    question_by=models.ForeignKey(User,on_delete=models.CASCADE)
    slug_q=models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.question
    
    def save(self, *args, **kwargs):
        if self.slug_q==None:
            slug1 = slugify(self.question)
            has_slug = Questions.objects.filter(slug_q=slug1).exists()
            count = 1
            while has_slug:
                count += 1
                slug1 = slugify(self.question) + '-' + str(count)
                has_slug =  Questions.objects.filter(slug_q=slug1).exists()
            self.slug_q = slug1
        super().save(*args, **kwargs)

class Answers(models.Model):
    question=models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer=RichTextUploadingField(null=True,blank=True)
    answer_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.answer_by.username

class Assignment(models.Model):
    by=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=10000,null=True,blank=True)
    questions=RichTextUploadingField(null=True,blank=True)
    year=models.CharField(choices=LIST_YEARS,default=1,max_length=100)
    subject=models.ForeignKey(Subjects,on_delete=models.CASCADE)
    dept=models.ForeignKey(Dept,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)

    slug_q=models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.slug_q==None:
            slug1 = slugify(self.title)
            has_slug = Questions.objects.filter(slug_q=slug1).exists()
            count = 1
            while has_slug:
                count += 1
                slug1 = slugify(self.title) + '-' + str(count)
                has_slug =  Questions.objects.filter(slug_q=slug1).exists()
            self.slug_q = slug1
        super().save(*args, **kwargs)

class SubmitAssignment(models.Model):
    assignment=models.ForeignKey(Assignment, on_delete=models.CASCADE)
    Link=models.CharField(max_length=1000,default="")
    submit_by=models.ForeignKey(User,on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.submit_by.username
