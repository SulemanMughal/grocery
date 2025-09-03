from django.core.management.base import BaseCommand
from neomodel import db

class Command(BaseCommand):
    help = "Test Neo4j connection"

    def handle(self, *args, **options):
        try:
            # Simple Cypher query
            result, meta = db.cypher_query("RETURN 'Hello from Neo4j!' AS message")
            self.stdout.write(self.style.SUCCESS(f"✅ Connected! Got: {result[0][0]}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Connection failed: {e}"))
