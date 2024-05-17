import os 
import sys 
import django

from django.db import transaction

sys.path.append('./')

if  __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config_poc.settings')
    django.setup()


from control_panel.models import cms


class CreateAdminProfile:
    
    def handle(self):
        
        cms.objects.create(
            page_title = "About Us",
            short_description = "Add Your short description here",
            long_description  = "Add your long description here",
            status = 1
        )

if __name__ == "__main__":
    CreateAdminProfile().handle()