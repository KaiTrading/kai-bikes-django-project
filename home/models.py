from django.db import models
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.safestring import mark_safe

# Create your models here.

class Site_Profile(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    logo = CloudinaryField('logo', folder = "logo")
    keywords = models.CharField(max_length=255,blank=True)
    description = models.CharField(max_length=255,blank=True)
    url = models.CharField(max_length=255,blank=True)
    company = models.CharField(max_length=50,blank=True)
    address = models.CharField(blank=True,max_length=100)
    addressLocality = models.CharField(blank=True,max_length=100)
    addressRegion = models.CharField(blank=True,max_length=100)
    postalCode = models.CharField(blank=True,max_length=100)
    addressCountry = models.CharField(blank=True,max_length=100)
    telephone = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=500)
    favicon = CloudinaryField('favicon',folder = "favicon",blank=True)
    facebook = models.CharField(blank=True,max_length=500)
    instagram = models.CharField(blank=True,max_length=500)
    linkedin = models.CharField(blank=True,max_length=500)
    twitter = models.CharField(blank=True,max_length=50)
    owner_name = models.CharField(max_length=150,blank=True)
    owner_facebook = models.CharField(max_length=150,blank=True)
    owner_instagram = models.CharField(max_length=150,blank=True)
    owner_twiter = models.CharField(max_length=150,blank=True)
    pixels = models.CharField(max_length=150,blank=True)
    status=models.CharField(max_length=10,choices=STATUS)
    aboutus = RichTextUploadingField()
    privacy_policy = RichTextUploadingField()
    return_policy = RichTextUploadingField()
    shipping_policy = RichTextUploadingField()
    terms_conditions = RichTextUploadingField()
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Slider(models.Model):
    name = models.CharField(max_length=180)
    image = CloudinaryField('image',folder = "slider")
    mobimage = CloudinaryField('mob-image',folder = "slider")
    link = models.CharField(max_length=180)

    def __str__(self):
        return self.name

class Banner(models.Model):
    name = models.CharField(max_length=180)
    fisimage = CloudinaryField('fis-image',folder = "banner")
    secimage = CloudinaryField('sec-image',folder = "banner")

    def __str__(self):
        return self.name

class Top_Nav(models.Model):
    link_text = models.CharField(max_length=20)
    link = models.CharField(max_length=180)

    def __str__(self):
        return self.link_text

class Foot1_Nav(models.Model):
    link_text = models.CharField(max_length=20)
    link = models.CharField(max_length=180)

    def __str__(self):
        return self.link_text



