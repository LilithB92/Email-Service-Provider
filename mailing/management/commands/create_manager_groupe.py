from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a "Manager" group with specific permissions'

    def handle(self, *args, **options):
        # Create or get group and define permissions
        group, created = Group.objects.get_or_create(name="Manager")

        # Example permissions: user management and log viewing
        permissions = ["view_mailing", "view_recipient", "view_customuser", "can_disable_mailing", "can_block_user"]

        for codename in permissions:
            try:
                permission = Permission.objects.get(codename=codename)
                group.permissions.add(permission)
            except Permission.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Permission {codename} not found"))

        self.stdout.write(self.style.SUCCESS("Manager group processed."))
