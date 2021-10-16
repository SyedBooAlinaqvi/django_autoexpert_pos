from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    sale_rate = models.DecimalField(max_digits=10,decimal_places=2)
    purchase_rate = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    status = models.BooleanField(default=True)
    rate = models.DecimalField(max_digits=10,decimal_places=2)

class Person(models.Model):
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type = models.SmallIntegerField(default=1)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

class Stock(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='product')
    quantity = models.IntegerField()
    status = models.BooleanField(default=True)
    last_updated = models.DateField(auto_now_add=True)

class Sale(models.Model):
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    maintenance_cost = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    sale_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2)
    final_amount = models.DecimalField(max_digits=10,decimal_places=2)
    paid = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    customer_name = models.CharField(max_length=255,null=True)
    phone_no = models.CharField(max_length=255,null=True)
    vehicle_name = models.CharField(max_length=255,null=True)
    vehicle_model = models.CharField(max_length=255,null=True)
    vehicle_no = models.CharField(max_length=255,null=True)


class SaleDetails(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_sale',null=True)
    service = models.ForeignKey(Service,on_delete=models.CASCADE,related_name='product',null=True)
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE,related_name='sale')

class Purchase(models.Model):
    person = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='person_purchase')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10,decimal_places=2)
    status = models.BooleanField(default=True)
    date = models.DateField()

class PurchaseDetails(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_purchase')
    quantity = models.IntegerField()
    rate = models.DecimalField(max_digits=10,decimal_places=2)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,related_name='purchase')

class Payment(models.Model):
    customer_name = models.CharField(max_length=255,null=True,default=None)
    credit = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    debit = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    date = models.DateField()
    entry_date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    purchase = models.ForeignKey(Purchase,on_delete=models.CASCADE,related_name='purchase_payment',null=True)
    sale = models.ForeignKey(Sale,on_delete=models.CASCADE,related_name='payment_sale',null=True)
    person = models.ForeignKey(Person,on_delete=models.CASCADE,related_name='vendor',null=True)

class StockOutLog(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='product_stock')
    quantity = models.IntegerField()
    date = models.DateField(auto_now_add=True)
