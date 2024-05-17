import ast
from django.template import loader

from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
import pytz
import datetime

from rest_framework.response import Response
from config_poc.settings import DEFAULT_FROM_EMAIL
import requests
import pyshorteners


# Send Email Function
class Mesg:
    @staticmethod
    def send_email(data, multiple=False, is_content_html=False):
        to_email=[data["to_email"]]
        if multiple:
            to_email=data["to_email"]
        cc = data.get('cc',[])
        email = EmailMessage(
            subject=data["subject"],
            body=data["body"],
            from_email=DEFAULT_FROM_EMAIL,
            to=to_email,
            cc=cc
        )
        if is_content_html:
            email.content_subtype = 'html'
        email.send()

def email_render_to_string(template_name, context=None, strip=False):
    """
    Render given template and context to string.

    If strip = True, replace \n and \r

    """

    message = loader.render_to_string(template_name=template_name, context=context)

    if strip:
        message = message.replace("\r", "").replace("\n", "")

    return message

def get_ip(request):
    try:
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
    except:
        ip = " "
    return ip


def localize_dt(dt, tz=None):
    """
    Localize a datetime object

    If no tz name is supplied, it will default to whatever the settings
    is set to.

    If a datetime object with a timezone is supplied, the object will be
    converted to use the new timezone

    AJAY, 28.01.2023
    """
    if tz is None:
        tz = settings.TIME_ZONE
    tz_obj = pytz.timezone(tz)

    return dt.astimezone(tz_obj) if dt.tzinfo else tz_obj.localize(dt)


def timezone_now(tz=settings.TIME_ZONE):
    """
    timezone.now() function with localized timezone

    """
    now = timezone.now()
    return localize_dt(now, tz)


def hrs_to_mins(hours=0, minutes=0):
    """
    utility to convert hours to minutes
    """
    if not hours and not minutes:
        return 0

    if isinstance(hours, str):
        hours = int(hours)

    if isinstance(minutes, str):
        minutes = int(minutes)

    return (hours * 60) + minutes


def mins_to_hrs(minutes: int = 0):
    """
    utility to convert minutes to hours
    """
    hours, _minutes = divmod(minutes, 60)

    return f"{hours}:{_minutes}"


def get_formatted_time(dt_input: datetime.datetime, tz=settings.TIME_ZONE, format: str = "%I:%M %p") -> str:
    """
    This function takes a datetime object and returns a formatted string representing the time in
    12-hour format with AM/PM indicator.
    """
    return localize_dt(dt_input, tz=tz).strftime("%I:%M %p")



def format_api_response(data, message, error_code):
    response_data = {
        "results": data,
        "message": message,
        "error_code": error_code
    }
    return Response(response_data, status=error_code)


def calculate_total_price(item_price, subitem_prices):
    try:
        # Convert item_price to float
        item_price_float = float(item_price)
    except ValueError:
        # Handle the case where item_price cannot be converted to float
        # You can choose to return a default value, raise an exception, or handle it differently based on your requirements
        return None
    
    # Convert subitem_prices to floats, handling any errors
    subitem_prices_float = []
    for price in subitem_prices:
        try:
            subitem_prices_float.append(float(price))
        except ValueError:
            # Handle the case where a subitem price cannot be converted to float
            # You can choose to skip this subitem, raise an exception, or handle it differently based on your requirements
            pass
    print("subitem_prices_float",subitem_prices_float)
    # Calculate total subitem price by summing up valid subitem prices
    total_subitem_price = sum(subitem_prices_float)
    
    # Calculate total price by adding item price and total subitem price
    total_price = item_price_float + total_subitem_price
    
    return total_price

class WhatsappMessage:
              
    @staticmethod    
    def whatsapp_message(data):
        url = 'https://db.vitelsms.com/whatsapp/templates/send_utility_template'
        header_text = data.get('subject')
        body_text1 = data.get('body_text1')
        body_text2 = data.get('body_text2')
        body_text3 = data.get('body_text3')
        phone_number = '91'+ data.get('phone_number')
        #convert url to short url
        type_tiny = pyshorteners.Shortener()
        # short_url = type_tiny.tinyurl.short(body_text3)
        
        payload = {
            'phone_numbers': phone_number,
            'template_name': 'restauran_default_template',
            'username': 'support@varundigitalmedia.com',
            'token_no': 'EAAKTIe6RYuMBAOMQ8pvOIlxj6LOjUYB8Fq0JaYPcnwq4eM6hfEwJAXL7bQZCDoopfZB1kvIRZCKcAFQ81z1z7LnRuMXqoFsfa8TANvLvzr89YbWvralvqZAtnodDPuUHRZCoDhSWbfd5OeAO7OACUlD9ECDOpqojTKodyFjlZBoeBfh6V3fNlI',
            'header_text': header_text,
            'body_text1': body_text1,
            'body_text2': body_text2,
            'body_text3': body_text3,
        }
        try:
            response = requests.post(url, data=payload)
            print(f"Whatsapp Message Sent Successfully, Subject:{header_text}, Mobile:{phone_number}, response:{response.text}")
            # logger.info(f"Whatsapp Message Sent Successfully, Subject:{header_text}, Mobile:{phone_number}, response:{response.text}")
        except Exception as e:
            print(f"Error while sending Whatsapp notificatons: {e}")
            # logger.warning(f"Error while sending Whatsapp notificatons: {e}")
            
def convert_to_list(string):
    # Check if the input string is a string representation of a list
    if string.startswith("[") and string.endswith("]"):
        # Convert the string representation of the list to an actual list
        try:
            string = ast.literal_eval(string)
        except ValueError:
            return "Invalid input"
    
    # If the input string is not a list, convert it to a list of integers
    if isinstance(string, str):
        try:
            string = [int(char) for char in string]
        except ValueError:
            return "Invalid input"  
    
    return string