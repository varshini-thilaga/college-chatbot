import os
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Verify project setup and configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Checking SECE Chatbot Setup...\n'))

        # Check DATA_FILE exists
        data_file = settings.DATA_FILE
        if Path(data_file).exists():
            self.stdout.write(self.style.SUCCESS(f'✓ Data file found: {data_file}'))
        else:
            self.stdout.write(self.style.ERROR(f'✗ Data file missing: {data_file}'))

        # Check MEDIA_ROOT exists
        if Path(settings.MEDIA_ROOT).exists():
            self.stdout.write(self.style.SUCCESS(f'✓ Media directory: {settings.MEDIA_ROOT}'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠ Media directory will be created: {settings.MEDIA_ROOT}'))

        # Check environment variables
        if os.environ.get('DJANGO_SECRET_KEY'):
            self.stdout.write(self.style.SUCCESS('✓ DJANGO_SECRET_KEY set from environment'))
        else:
            self.stdout.write(self.style.WARNING('⚠ Using default SECRET_KEY (not recommended for production)'))

        # Check DEBUG setting
        if settings.DEBUG:
            self.stdout.write(self.style.WARNING('⚠ DEBUG=True (disable for production)'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ DEBUG=False'))

        # Check dependencies
        try:
            import langdetect
            import googletrans
            from gtts import gTTS
            from sentence_transformers import SentenceTransformer
            self.stdout.write(self.style.SUCCESS('✓ All dependencies installed'))
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'✗ Missing dependency: {e}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Setup check complete!'))
