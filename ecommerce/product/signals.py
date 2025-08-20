# implement signals
# TODO: CREATE A SIGNAL TO SEND NOTIFICATION WHEN A NEW PRODUCT IS CREATED
# TODO: CREATE A CUSTOM SIGNAL FOR WHEN A PRODUCT PRICE DROPS BELOW $50
# TODO: WRITE A SIGNAL TO UPDATE THE STOCK FIELD OF PRODUCT WHEN AN ORDER IS CREATED

from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from .models import Product

# TODO: CREATE A CUSTOM SIGNAL FOR WHEN A PRODUCT PRICE DROPS BELOW $50

price_dropped = Signal()

@receiver(price_dropped, sender=Product)
def notify_when_price_dropped(sender, instance, **kwargs):
    print(f"price dropped alert: {instance.name} is now ${instance.price}")


@receiver(post_save, sender=Product)
def check_price_drop(sender, instance, created, **kwargs):
    if not created and instance.price < 50:
        price_dropped.send(sender=Product, instance=instance)