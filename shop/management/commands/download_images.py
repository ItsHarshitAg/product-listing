"""
Download sample product images for the application.
"""
import os
import urllib.request
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Download sample product images'

    def handle(self, *args, **options):
        # Create the media/products directory if it doesn't exist
        products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(products_dir, exist_ok=True)
        
        # Define the image URLs and filenames
        images = {
            'digital_camera.webp': 'https://raw.githubusercontent.com/ItsHarshitAg/product-listing/master/media/products/digital_camera.webp',
            'laptop.jpeg': 'https://raw.githubusercontent.com/ItsHarshitAg/product-listing/master/media/products/laptop.jpeg',
            'smartphone.jpeg': 'https://raw.githubusercontent.com/ItsHarshitAg/product-listing/master/media/products/smartphone.jpeg',
            'smartwatch.webp': 'https://raw.githubusercontent.com/ItsHarshitAg/product-listing/master/media/products/smartwatch.webp',
            'speaker.png': 'https://raw.githubusercontent.com/ItsHarshitAg/product-listing/master/media/products/speaker.png',
            'wireless_headphone.webp': 'https://raw.githubusercontent.com/ItsHarshitAg/product-listing/master/media/products/wireless_headphone.webp',
        }
        
        # Download each image
        for filename, url in images.items():
            file_path = os.path.join(products_dir, filename)
            
            if not os.path.exists(file_path):
                try:
                    self.stdout.write(f'Downloading {filename}...')
                    urllib.request.urlretrieve(url, file_path)
                    self.stdout.write(self.style.SUCCESS(f'Successfully downloaded {filename}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error downloading {filename}: {e}'))
            else:
                self.stdout.write(f'{filename} already exists, skipping')
