from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # Here Product class is mentioned in double quotes because it is defined below Collection class
    # also related_name is set to '+' to avoid creating collection class in Product class 
    # because we are already creating it in Product class due to another relationship
    featured_product = models.ForeignKey("Product", on_delete=models.SET_NULL, null=True, related_name='+')

class Promotion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    discount = models.FloatField()    
    # since products and promotions have many to many rel, we will have a field here called product_set

class Product(models.Model):
    # CharField has one reqd field max_length
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    # DecimalField has two required attrs max_digits and decimal_places to sex max allowed value as 9999.99
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # here products and promotions have many to many relationship
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    email = models.EmailField(unique=True)
    # using regex pattern for validating phone nos to have 10 digits
    phone_regex = RegexValidator(
        regex = r'^\d{10}$',
        message = "Phone number must be in the format '1234567890'"
    ) 
    phone = models.CharField(validators=[phone_regex], max_length=10)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
    class Meta:
        indexes = [
            models.Index(fields=['last_name', 'first_name'])
        ]



class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'

    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed')
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)    

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()        


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=10, null=True)
    # here if customer field is added as primary key there will be only one address per customer.
    # if it is not mentioned as primary key, id will be PK and many addresses can be related with a customer
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


