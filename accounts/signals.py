from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_user_group(sender, instance, created, **kwargs):
    if created:
        # Gruppo base "user"
        user_group, _ = Group.objects.get_or_create(name='user')
        instance.groups.add(user_group)

        # Se l'utente è anche moderatore
        if instance.groups.filter(name='moderator').exists():
            moderator_group, _ = Group.objects.get_or_create(name='moderator')
            instance.groups.add(moderator_group)

        # Se l'utente è anche product_manager
        if instance.groups.filter(name='product_manager').exists():
            pm_group, _ = Group.objects.get_or_create(name='product_manager')
            instance.groups.add(pm_group)
