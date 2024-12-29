from django.db import models

# Create your models here.
class ContactUs(models.Model):
    name=models.CharField(max_length=25)
    email=models.EmailField()
    phonenumber=models.CharField(max_length=10,default="phone")
    description=models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name
    
class Offer(models.Model):
    Offer_name=models.CharField(max_length=100)
    Offer=models.CharField(max_length=50)
    img=models.ImageField(upload_to='images')

    def __str__(self):
        return self.Offer_name
    
    class AboutMe(models.Model):
        name=models.CharField(max_length=60)
        objective=models.TextField()
        img2 = models.ImageField(upload_to='images')
    
        def __str__(self):
            return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json =  models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)    
    oid=models.CharField(max_length=150,blank=True)
    amountpaid=models.CharField(max_length=500,blank=True,null=True)
    paymentstatus=models.CharField(max_length=20,blank=True)
    phone = models.CharField(max_length=100,default="")
    def __str__(self):
        return self.name