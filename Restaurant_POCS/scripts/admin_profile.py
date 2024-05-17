import os 
import sys 
import django

from django.db import transaction

sys.path.append('./')

if  __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config_poc.settings')
    django.setup()


from control_panel.models import AdminProfile


class CreateAdminProfile:
    
    def handle(self):
        
        AdminProfile.objects.create(
            full_name = "Admin",
            email_address = "example@gmail.com",
            phone_number  = "9856654478"
        )

if __name__ == "__main__":
    CreateAdminProfile().handle()