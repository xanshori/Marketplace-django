from django.utils.text import slugify
from django.db import models

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=50,unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cat_image = models.ImageField(upload_to='photos/categories',blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.category_name

    def save(self):
        self.slug = slugify(self.category_name)
        super(Category,self).save()