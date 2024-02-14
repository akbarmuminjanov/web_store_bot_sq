from .models import Product
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings

@receiver(pre_save, sender=Product)
def upload_image(sender, instance: Product, *args, **kwargs):
    image = instance.image.url

    image_url = str(settings.BASE_DIR) + "\\" + image

    
