from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    color = models.CharField(max_length=7, default='#525252', blank=True, null=True)
    def __str__(self): return f'{self.name}'
    class Meta(): verbose_name_plural = 'Categories'

class Item(models.Model):
    ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50); desc = models.TextField()
    price = models.FloatField()
    category = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self): return f'{self.ID} : {self.price}'
    @property
    def images(self): return self.itemimage_set.all()

class ItemImage(models.Model):
    ID = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    img = models.ImageField(default='items_app/ItemImage/default.png', upload_to='items_app/ItemImage')