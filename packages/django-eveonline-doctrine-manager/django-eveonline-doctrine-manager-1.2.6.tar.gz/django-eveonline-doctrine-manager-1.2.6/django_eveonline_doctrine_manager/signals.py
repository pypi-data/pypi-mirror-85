from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import EveFitting
from .tasks import populate_fitting_fields

@receiver(post_save, sender=EveFitting)
def populate_low_priority_fitting_fields(sender, **kwargs):
    if 'update_fields' in kwargs and kwargs.get('update_fields'):
        skip_fields = ['parsed_format_raw', 'market_format_raw']
        for skip_field in skip_fields:
            if skip_field in kwargs.get('update_fields'):
                return 
    
    fitting = kwargs.get('instance')
    populate_fitting_fields.apply_async(args=[fitting.pk])
