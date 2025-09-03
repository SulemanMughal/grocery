from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from apps.users.infrastructure.models import UserNode

class Command(BaseCommand):
    help = "Create or update a Super Admin user in Neo4j"

    def add_arguments(self, parser):
        parser.add_argument(
            "--name", type=str, default="Super Admin",
            help="Name of the super admin"
        )
        parser.add_argument(
            "--email", type=str, default="admin@example.com",
            help="Email of the super admin"
        )
        parser.add_argument(
            "--password", type=str, default="Admin@123",
            help="Password for the super admin"
        )

    def handle(self, *args, **options):
        name = options["name"].strip()
        email = options["email"].lower().strip()
        password = make_password(options["password"])

        existing = UserNode.nodes.first_or_none(email=email)

        if existing:
            existing.name = name
            existing.password = password
            existing.role = "ADMIN"
            existing.is_active = True
            existing.touch()
            existing.save()
            self.stdout.write(
                self.style.SUCCESS(f"Updated existing admin: {email}")
            )
        else:
            u = UserNode(
                name=name,
                email=email,
                password=password,
                role="ADMIN",
                is_active=True,
            )
            u.touch()
            u.save()
            self.stdout.write(
                self.style.SUCCESS(f"Created new admin: {email}")
            )
