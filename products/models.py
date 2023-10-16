import uuid
from django.db import models
from django.db.models.fields import related
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class Product_Model(models.Model):
    status_options = [("Sale","Sale"),("New","New"),("Out of Stock","Out of Stock"),("Not Available","Not Available")]
    name = models.CharField(max_length=110, blank=True, null=True)
    image = models.ImageField(upload_to="products", default="def_product.jpg")
    image1 = models.ImageField(upload_to="products", default="def_product.jpg")
    image2 = models.ImageField(upload_to="products", default="def_product.jpg")
    image3 = models.ImageField(upload_to="products", blank=True, null=True)
    
    priority = models.IntegerField(blank=True,null=True,default=1)
    ratings = models.IntegerField(blank=True,null=True,default=1)
    count = models.IntegerField(blank=True,null=True,default=1)
    status = models.CharField(max_length=100,choices= status_options,default="New",blank=True,null=True)
    country = models.CharField(max_length=110, blank=True, null=True)
    metal = models.CharField(max_length=110, blank=True, null=True)
    back_finding = models.CharField(max_length=110, blank=True, null=True)
    weight = models.CharField(max_length=110, blank=True, null=True)
    lustre = models.CharField(max_length=110, blank=True, null=True)
    weight = models.CharField(max_length=110, blank=True, null=True)
    rusting = models.CharField(max_length=110, blank=True, null=True)
    stone = models.CharField(max_length=110, blank=True, null=True)
    occasion = models.CharField(max_length=110, blank=True, null=True)
    
    bio = models.TextField(blank=True, null=True)
    price = models.FloatField(help_text="in rupees", blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True,related_name="product_author")

    def __str__(self):
        return self.name

class wishlist(models.Model):
    name = models.CharField(max_length=100,default="",blank=True, null=True)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product_Model,on_delete=models.CASCADE, blank=True,null=True,related_name="wishlist_prd")
    created = models.DateTimeField(default=timezone.now)

    def save(self,*args,**kwargs):
        self.name = self.product.name
        super(wishlist,self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class featured(models.Model):
    name = models.CharField(max_length=100,default="",blank=True, null=True)
    
    product = models.ForeignKey(Product_Model,on_delete=models.CASCADE, blank=True,null=True,related_name="featured_prd")
    created = models.DateTimeField(default=timezone.now)


    def save(self,*args,**kwargs):
        self.name = self.product.name
        super(featured,self).save(*args,**kwargs)

    def __str__(self):
        return self.name






class product_comment(models.Model):
    body = models.CharField(max_length=200, blank=True, null=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="prd_com")
    created = models.DateTimeField(default=timezone.now)
    com_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.com_id)+str(self.author)


class cart_model(models.Model):
    quantity = models.IntegerField(blank=True, null=True)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="br")
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name='slr')
    net_price = models.FloatField(blank=True, null=True)
    name = models.ForeignKey(
        Product_Model, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="cart", default="def_product.jpg")

    def __str__(self):
        return str(self.seller)+" "+str(self.name)+" "+str(self.net_price)


class order_model(models.Model):
    quantity = models.IntegerField(blank=True, null=True)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="buyer")
    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="seller")
    net_price = models.FloatField(blank=True, null=True)
    name = models.ForeignKey(
        Product_Model, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="cart", default="def_product.jpg")

    def __str__(self):
        return str(self.seller)+" "+str(self.name)+" "+str(self.net_price)


class sales_list(models.Model):

    status_opt = [("Order Placed","Order Placed"),("Preparing your order","Preparing your order"),("Dispatched","Dispatched"),("Delivered","Delivered")]

    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    net_price = models.FloatField(blank=True, null=True)
    costumer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="sale_costumer")
    salesman = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="sale_owner")
    products = models.ManyToManyField(
        order_model, blank=True)
    created = models.DateField(default=timezone.now)
    time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=50,choices=status_opt,default="Order Placed")
    name = models.CharField(default="pragya",max_length=100,blank=True,null=True)
    number = models.IntegerField(default="9437326713",blank=True,null=True)
    adress= models.TextField(default="sukhna",blank=True,null=True)
    def save(self, *args, **kwargs):
        if self.transaction_id == None:
            self.transaction_id = str(
                uuid.uuid4()).replace("-", "")[:10].upper()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.transaction_id)


class cancel_orders(models.Model):

    status_opt = [("Order Placed","Order Placed"),("Preparing your order","Preparing your order"),("Dispatched","Dispatched"),("Delivered","Delivered")]

    transaction_id = models.CharField(max_length=20, blank=True, null=True)
    net_price = models.FloatField(blank=True, null=True)
    costumer = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="can_order_costumer1")
    salesman = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="can_order_owner1")
    products = models.ManyToManyField(
        order_model, blank=True)
    created = models.DateField(default=timezone.now)
    status = models.CharField(max_length=50,choices=status_opt,default="Order Placed")
    name = models.CharField(max_length=100,blank=True,null=True)
    number = models.IntegerField(blank=True,null=True)
    adress= models.TextField(blank=True,null=True)
    
    

    def __str__(self):
        return str(self.salesman)


