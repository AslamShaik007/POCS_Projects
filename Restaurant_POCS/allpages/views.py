from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import HttpResponse

from control_panel.models import (category, 
                                  AllTables,
                                  BookTheTable,
                                  AdminProfile,
                                  specialoffers,
                                  cms,
                                  items,
                                  specialoffers,
                                  contactUs,
                                  gallery,
                                  subscription,
                                  AddToCartItems,
                                  SubItems,
                                  OrderDetails)
from allpages.models import CustomUser

from django.http import JsonResponse
from datetime import datetime
from django.conf import settings
from control_panel.utils import get_ip, timezone_now, calculate_total_price, Mesg, WhatsappMessage, convert_to_list
from django.template.loader import render_to_string

from .forms import RegisterForm

from django.contrib.auth import login
from .forms import LoginForm
                                  

# Create your views here.


def index(request):
    menu_list = items.objects.filter(status=1, is_deleted=False).order_by("display_order_for_our_menu")
    special_offers = specialoffers.objects.filter(status=1,is_deleted=False).order_by("display_order")
    return render(request, "home/index.html",{"menu_list":menu_list,"offers":special_offers,'MEDIA_URL':settings.MEDIA_URL,})

def subscribe_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        ip_address = get_ip(request)
        submission_date = timezone_now().date()
        date_time = timezone_now()
        subscription(
            email = email
        ).save()
        email_context = {
            "name" : email,
            "ip_address" : ip_address,
            "submission_date" : submission_date,
            "date_time" : date_time,
            "ip_address" : ip_address
        }
        admin_email =  AdminProfile.objects.first()
        ######## Send Mail to User ##########
        body = render_to_string(
            template_name="contactus/contactus-email.html", 
            context = email_context
        )
        data={
            "subject":"Thankyou for Subscribe",
            "body":body,
            "to_email":admin_email.email_address
        }
        try:
            Mesg.send_email(data,is_content_html=True)
        except Exception as e:
            print(f"Error while sending Email notificaton : {e}")
        
        ########  Send Email to Admin #######
        if admin_email:
            body2 = render_to_string(
                template_name="mails/subscribe-email.html", 
                context = email_context
            ) 
            data2={
                "subject":"Thankyou for Subscribe",
                "body":body2,
                "to_email":admin_email.email_address
            }
            try:
                Mesg.send_email(data2,is_content_html=True)
            except Exception as e:
                print(f"Error while sending Email notificaton : {e}")
            
        return redirect('thankyou')
        

def index_burgers(request):
    return render(request, "home/index-burgers.html")

def index_sliders(request):
    return render(request, "home/index-slider.html")

def index_video(request):
    return render(request, "home/index-video.html")

def about_us(request):
    about_data = cms.objects.filter(id=1,status=1,is_deleted=False).first()
    return render(request, "about/about.html", {"data":about_data, 'MEDIA_URL':settings.MEDIA_URL,})

def gallery_listing(request):
    gallerylisting = gallery.objects.filter(status=1,is_deleted=False).values().order_by("display_order")    
    return render(request, 'gallery/gallery.html', {'gallerylisting': gallerylisting,'MEDIA_URL': settings.MEDIA_URL})

def book_a_table(request):
    
    if request.method == "POST":
        from datetime import time
        tables_data = AllTables.objects.filter(id=request.POST.get('table_name'),no_of_seats = int(request.POST.get("attendents"))).first()
        name    = request.POST.get('name')
        email_address   = request.POST.get('email')
        phone_number = request.POST.get("phone")
        date = request.POST.get("date")
        timings = request.POST.get("timings")
        total_members = request.POST.get("attendents")
        
        #  Sorry table with seating capacity 5 is not available currently
        if not tables_data:
            return render(request, "allpages/book-a-table.html", {'msg': f"Sorry table with seating capacity {request.POST.get('attendents')} is not available currently."})
        table_seats = tables_data.no_of_seats
        from_time = tables_data.from_time
        to_time = tables_data.to_time
        hours, minutes = map(int, timings.split(':'))
        booking_time = time(hours, minutes)
        if not (from_time <= booking_time <= to_time):
            return render(request, "allpages/book-a-table.html",{'msg': "Your booking for the table is unavailable at this time. Please check again."})
            # return JsonResponse(
            #     {
            #     'response': 'notSaved', 
            #     'title':'Warning!', 
            #     'icon':'error', 
            #     'msg': "Your booking for the table is unavailable at this time. Please check again."
            #     }, 
            #     safe=False
            # )

        if (int(table_seats) < int(total_members)):
            return render(request, "allpages/book-a-table.html",{'msg': "Your selected number exceeds the seating capacity. Please check."})
            # return JsonResponse(
            #     {
            #     'response': 'notSaved', 
            #     'title':'Warning!', 
            #     'icon':'error', 
            #     'msg': "Your selected number exceeds the seating capacity. Please check."
            #     }, 
            #     safe=False
            # )
        _created = BookTheTable.objects.create(
            table_id=tables_data,
            name=name, 
            phone_number = phone_number, 
            email_address = email_address, 
            total_members = total_members,
            date=date,
            timings = timings
            )
        tables_data.status="Booked"
        tables_data.save()
        time_data = datetime.strptime(timings, '%H:%M')
        converted_time = time_data.strftime('%I:%M %p')
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d-%m-%Y")
        
        if _created:
            print("Coming Here")
            try:
                ################# Send Email & Whatsapp message to the User ################
                body1=f'Hello {name},\n\nWe are pleased to inform you that your table booking has been successfully confirmed. Below are the details:\n\nTotal Members : {total_members}\nDate : {formatted_date}\nTimings : {converted_time} \n\nIf you have any questions or need further assistance, please feel free to contact us.\n\nThanks & Regards,\nRestaurent POC'  
                data={
                    'subject':'Table Booking Conformation',
                    'body':body1,
                    'to_email':email_address
                }
                try:
                    Mesg.send_email(data)
                except Exception as e:
                    print(f"Error while sending Email notificaton : {e}")
                try:
                    whatsapp_data = {
                                    'phone_number': phone_number,
                                    'subject': 'Table Booking',
                                    "body_text1":"We are pleased to inform you that your table booking has been successfully confirmed. Below are the details:",
                                    "body_text2":f"Table Name : {tables_data.table_name}, Total Members: {total_members}",
                                    "body_text3": f"Date : {formatted_date}, Time : {converted_time}",
                                    }
                    WhatsappMessage.whatsapp_message(whatsapp_data)
                except Exception as e:
                    print(f"Error while sending Whatsapp notificaton")
                    #logger.warning(f"Error while sending Whatsapp notificaton to {instance.employee.user.username} in notifications about check in: {e}")
                ################ Send Email & Whatsapp message to the Admin ################
                admin_data = AdminProfile.objects.first()
                if admin_data:
                    body2=f'Hello Admin,\n\nThis is to inform you that {name} has successfully booked a table. Please find the details below:\n\nPhone Number : {phone_number}\nEmail : {email_address}\nTotal Members : {total_members}\nDate : {formatted_date}\nTimings : {converted_time} \n\nThanks & Regards,\nRestaurent POC'  
                    data={
                        'subject':'Table Booked',
                        'body':body2,
                        'to_email':admin_data.email_address
                    }
                    try:
                        Mesg.send_email(data)
                    except Exception as e:
                        print(f"Error while sending Email notificaton : {e}")
                    try:
                        whatsapp_data = {
                                        'phone_number': admin_data.phone_number,
                                        'subject': 'Table Booking',
                                        "body_text1":f"This is to inform you that {name} has successfully booked a table. Please find the details below:",
                                        "body_text2":f"Table Name : {tables_data.table_name}, Total Members: {total_members}",
                                        "body_text3": f"Date : {formatted_date}, Time : {converted_time}",
                                        }
                        WhatsappMessage.whatsapp_message(whatsapp_data)
                    except Exception as e:
                        print(f"Error while sending Whatsapp notificaton")

            except Exception as e:
                print(f"Exception in sending Email {str(e)}")
            return redirect('thankyou')   
        else:
            return render(request, "allpages/book-a-table.html",{'msg': "Somthing Went Wrong PLease try after Sometime"})
    
    else:
        data = AllTables.objects.filter(status__in=['Available'])    
        return render(request, "allpages/book-a-table.html",{"data":data})

def faq(request):
    return render(request, "allpages/faq.html")

def offers(request):
    offers_data = specialoffers.objects.filter(status=1,is_deleted=False).values().order_by("display_order")
    return render(request, "allpages/offers.html",{"data":offers_data, 'MEDIA_URL':settings.MEDIA_URL,})

def order(request):
    
    categories = category.objects.filter(status=1,show_on_our_menu='1',is_deleted=False)
    category_data = []
    
    for cat in categories:
        items_data = []
        items = cat.items_set.filter(status=1,is_deleted=False)
        
        for item in items:
            subitems_data = []
            subitems = item.subitems_set.filter(status=1,is_deleted=False)
            
            for subitem in subitems:
                subitems_data.append({
                    'subitem_id':subitem.id,
                    'sub_item_title': subitem.sub_item_title,
                    'price': subitem.price,
                    'short_description': subitem.short_description,
                    'status': subitem.status,
                    'is_deleted': subitem.is_deleted,
                    'created_at': subitem.created_at,
                    'updated_at': subitem.updated_at,
                })
            
            items_data.append({
                'item_id':item.id,
                'item_name': item.item_name,
                'item_desc': item.item_desc,
                'price': item.price,
                'image': item.image.url if item.image else None,
                'popular': item.popular,
                'status': item.status,
                'display_order': item.display_order,
                'display_order_for_special_item': item.display_order_for_special_item,
                'status_for_special_item': item.status_for_special_item,
                'discount_description_for_special_item': item.discount_description_for_special_item,
                'description_for_special_item': item.description_for_special_item,
                'display_order_for_our_menu': item.display_order_for_our_menu,
                'status_for_our_menu': item.status_for_our_menu,
                'selection_type': item.selection_type,
                'is_deleted': item.is_deleted,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'subitems': subitems_data,
            })
        
        category_data.append({
            'category_id':cat.id,
            'category_name': cat.category_name,
            'slug':cat.slug,
            'category_desc': cat.category_desc,
            'image': cat.image.url if cat.image else None,
            'status': cat.status,
            'display_order': cat.display_order,
            'show_on_our_menu': cat.show_on_our_menu,
            'is_deleted': cat.is_deleted,
            'created_at': cat.created_at,
            'updated_at': cat.updated_at,
            'items': items_data,
        })
    return render(request, "allpages/order.html", {"data":category_data})

def order_category(request, category_id):
    if not category_id:
         return redirect('/order')
    else:
        categories = category.objects.filter(status=1,show_on_our_menu='1',is_deleted=False)    
    category_data = []
    
    for cat in categories:
        items_data = []
        items = cat.items_set.filter(status=1,is_deleted=False)
        
        for item in items:
            subitems_data = []
            subitems = item.subitems_set.filter(status=1,is_deleted=False)
            
            for subitem in subitems:
                subitems_data.append({
                    'subitem_id':subitem.id,
                    'sub_item_title': subitem.sub_item_title,
                    'price': subitem.price,
                    'short_description': subitem.short_description,
                    'status': subitem.status,
                    'is_deleted': subitem.is_deleted,
                    'created_at': subitem.created_at,
                    'updated_at': subitem.updated_at,
                })
            
            items_data.append({
                'item_id':item.id,
                'item_name': item.item_name,
                'item_desc': item.item_desc,
                'price': item.price,
                'image': item.image.url if item.image else None,
                'popular': item.popular,
                'status': item.status,
                'display_order': item.display_order,
                'display_order_for_special_item': item.display_order_for_special_item,
                'status_for_special_item': item.status_for_special_item,
                'discount_description_for_special_item': item.discount_description_for_special_item,
                'description_for_special_item': item.description_for_special_item,
                'display_order_for_our_menu': item.display_order_for_our_menu,
                'status_for_our_menu': item.status_for_our_menu,
                'is_deleted': item.is_deleted,
                'created_at': item.created_at,
                'updated_at': item.updated_at,
                'subitems': subitems_data,
            })
        
        category_data.append({
            'requestid': category_id,
            'category_id':cat.id,
            'category_id':cat.id,
            'category_name': cat.category_name,
            'category_desc': cat.category_desc,
            'image': cat.image.url if cat.image else None,
            'status': cat.status,
            'display_order': cat.display_order,
            'show_on_our_menu': cat.show_on_our_menu,
            'is_deleted': cat.is_deleted,
            'created_at': cat.created_at,
            'updated_at': cat.updated_at,
            'items': items_data,
        })
    return render(request, "allpages/order.html", {"data":category_data})

################################ ADD TO CART FUNCTIONALITY #################################

def add_to_cart(request):
    if request.method == "POST":
        user_id = request.user
        session_id = request.session.session_key
        category_id = request.POST.get('categoryid')
        item_id = request.POST.get('itemid')
        item_price = request.POST.get('itemprice')
        itemtitle = request.POST.get('itemtitle')
        item_desc = request.POST.get('item_desc')
        itemimage = request.POST.get('itemimage')
        special_instructions = request.POST.get("special_instructions")
        quantity = 1
        if "quantity" in request.POST:
            quantity = request.POST.get("quantity")
        # subitem_ids = request.POST.get("subitem_id")
        subitemidcheck = request.POST.get('subitemidcheck')
        if subitemidcheck== "1":
            subitem_ids = [request.POST.get('subitemid')]         
            
        else:
            subitem_ids = request.POST.getlist('subitem_id[]', [])
        
        
        # user = CustomUser.objects.get(id=1)
        
        item_instance = items.objects.get(id=item_id)
        subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
        # Check if cart item already exists for this session and item
        cart_item = AddToCartItems.objects.filter(
            user_id = user_id,
            item_id=item_instance,
            subitem_id__in= subitem_instances
        ).first()
        
        if cart_item:
            # Cart item exists, update quantity and total price
            cart_item.quantity += int(quantity)
            cart_item.total_price = item_instance.price * cart_item.quantity
            cart_item.special_instructions = special_instructions
            
            cart_item.subitem_id.clear()

            # Add selected subitems to existing cart item
            # subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
            if subitem_instances:
                for i in subitem_instances:
                    cart_item.total_price += i.price *cart_item.quantity
            cart_item.subitem_id.add(*subitem_instances)

            cart_item.save()
        else:
            # subitems = SubItems.objects.filter(pk__in=subitem_ids)
            
            total_price = item_instance.price * int(quantity)
            # Calculate total price
            if subitem_ids:
                for subitem in subitem_instances:
                    total_price += subitem.price * int(quantity)
            # Create AddToCartItems instance
            cart_item = AddToCartItems.objects.create(
                session_id = session_id,
                user_id = user_id,
                item_id=item_instance,
                quantity=quantity,
                total_price=total_price,
                special_instructions=special_instructions
            )
            # subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
            cart_item.subitem_id.set(subitem_instances)
            cart_item.save()
        
        msg = {'response': 'success', 'msg': 'Your Item Has Been Successfully Added.'}
        #if savedData:
            #msg = {'response': 'success', 'msg': 'Your Item Has Been Successfully Added.'}
        #else:
            #msg = {'response': 'notdeleted', 'msg': 'Your Item Has Not Been Added.'}
        
        return JsonResponse(msg, safe=False)    

        #return render(request, "allpages/checkout.html", {"data" : cart_item})

"""
def add_to_cart(request):
    if request.method == "POST":
        # try:
        #     session_id = request.session.session_key
        #     if not session_id:
        #         request.session.save()  # This will create a new session ID
        #         session_id = request.session.session_key
        #     # Your code here
        #     print(f"Session ID: {session_id}")
        # except Exception as e:
        #     # Handle the exception
        #     print(f"An error occurred: {str(e)}")





        session_id = request.session.session_key
        category_id = request.POST.get('categoryid')
        item_id = request.POST.get('itemid')
        item_price = request.POST.get('itemprice')
        itemtitle = request.POST.get('itemtitle')
        item_desc = request.POST.get('item_desc')
        itemimage = request.POST.get('itemimage')


        user = request.user
        # form = LoginForm()
        # if isinstance(user, AnonymousUser):
        #     print("COMIN HERE")
        #     # form = LoginForm(request.POST)
        #     return render(request, 'registration/user-login.html', {'form': form})

        subitemidcheck = request.POST.get('subitemidcheck')
        subtotal=float()
        subitetitle=[]
        if subitemidcheck== "1":
            subitem_ids = request.POST.get('subitemid')           
            subitems = SubItems.objects.filter(id=subitem_ids,status=1,is_deleted=False).first()   
            if subitems:           
                subitetitle.append(subitems.sub_item_title)
                subtotal =(float(subitems.price))

            #subitetitle = request.POST.get('subitetitle')
            #subitetitle.append(request.POST.get('subitetitle'))
            #subitem_prices = float(request.POST.get('subiteprice'))
            #subtotal=subitem_prices
        else:
            subitem_ids = request.POST.getlist('subitem_id[]', [])
            #subitetitle = request.POST.getlist('subitetitle[]', [])
            #subitem_prices = request.POST.getlist('subiteprice[]', [])            
                                
            for subitemid in subitem_ids :
                subitems = SubItems.objects.filter(id=subitemid,status=1,is_deleted=False).first()                
                subitetitle.append(subitems.sub_item_title)
                subtotal +=(float(subitems.price))
                                
        totalitemprice=subtotal+float(item_price) 
        
        cart_item=[]
        response_data = []
        
        print("Item_Id",item_id)
        print("SubItem_Ids",subitem_ids)
        print("Session_ID",session_id)
        # print("User ID",user.id)
        user = CustomUser.objects.get(id=1)
        item_instance = items.objects.get(id=item_id)        
        order_details = AddToCartItems.objects.create(
            session_id = session_id,
            user_id = user,
            item_id = item_instance,
            total_price = totalitemprice,
            quantity = 1
        )
        subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
        order_details.subitem_id.set(subitem_instances)
        order_details.save()

        cart_item = {
                    "item_id": item_id,
                    "item_name": itemtitle,
                    "price": float(item_price),
                    "image": itemimage,
                    "item_desc": item_desc,
                    "subitem_ids": subitem_ids,
                    "subitetitle": subitetitle,
                    "subtotal": subtotal,
                    "totalitemprice": totalitemprice 
                }
        
        response_data.append({"data": cart_item})   
        msg = {'response': 'success', 'msg': 'Your Item Has Been Successfully Added.'}
        #if savedData:
            #msg = {'response': 'success', 'msg': 'Your Item Has Been Successfully Added.'}
        #else:
            #msg = {'response': 'notdeleted', 'msg': 'Your Item Has Not Been Added.'}
        
        return JsonResponse(msg, safe=False)    

        #return render(request, "allpages/checkout.html", {"data" : cart_item})

"""


def edit_to_cart(request):
    
    if request.method == "POST":
        session_id = request.session.session_key
        cart_id = request.POST.get('cart_id')
        item_id = request.POST.get('item_id')
        quantity = request.POST.get("quantity")        
        total_price = request.POST.get("total_price")
        
        cart_data = AddToCartItems.objects.filter(id=cart_id).first() 
        item_price = cart_data.item_id.price
        subitem_instances = cart_data.subitem_id.all()
        subitems_price = 0
        for i in subitem_instances:
            subitemlo = SubItems.objects.get(id = i.id)
            subitems_price += subitemlo.price
            
        total = item_price +  subitems_price     
        cart_data.quantity = quantity
        cart_data.total_price = total * int(cart_data.quantity)
        cart_data.save() 

        msg = {'response': 'success', 'msg': 'Your Item Has Been Updated.'}
        
        return JsonResponse(msg, safe=False)    
        


def delete_to_cart(request):    
    if request.method == "POST":      
        cart_id = request.POST.get('cart_id')
        cart_data = AddToCartItems.objects.filter(id=cart_id)
        cart_data.delete()
        msg = {'response': 'success', 'msg': 'Your Item Has Been Deleted.'} 
        return JsonResponse(msg, safe=False) 

    
def edit_cart_details(request,id):
    
    if request.method == "POST":
        session_id = request.session.session_key
        item_id = request.POST.get('itemid')
        quantity = request.POST.get("quantity")
        subitem_ids = request.POST.get("")
        
        item_instance = items.objects.get(id=item_id)
        cart_data = AddToCartItems.objects.filter(session_id = session_id,id=id,item_id = item_instance).first()
        cart_data.subitem_id.clear()
        cart_data.quantity = quantity
        subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
        cart_data.subitem_id.set(subitem_instances)
        cart_data.save() 
        return render(request, "allpages/checkout.html")
    
    else:
        return render(request, "allpages/checkout.html")


def delete_cart_details(request,id):
    
    if request.method == "POST":
        session_id = request.session.session_key
        item_id = request.POST.get('itemid')
        cart_data = AddToCartItems.objects.filter(user_id = 1,id=id)
        cart_data.delete()
        
        cart_items = AddToCartItems.objects.filter(user_id = 1)
        output = []
        seen_ids = set()
        for item in cart_items:
            if item.id not in seen_ids:
                subitems_list = [subitem.sub_item_title for subitem in item.subitem_id.all()]

                item_data = {
                    "id": item.id,
                    "item_id" : item.item_id.id,
                    "item_name": item.item_id.item_name,
                    "subitems": subitems_list,
                    "quantity": item.quantity,
                    "total_price": item.total_price,
                    "special_instructions": item.special_instructions
                }
                output.append(item_data)
        print("output,",output)
        return render(request, "allpages/checkout.html", {"cart_items" : output})
    else:
        cart_items = AddToCartItems.objects.filter(user_id = 1).values()
        return render(request, "allpages/checkout.html", {"cart_items" : cart_items})
#################################################################################################3        
def view_cart(request):            
    return render(request, "allpages/view_cart.html")       

def my_orders(request):
    return render(request, "allpages/my-orders.html")
      
##############################################################################################
from django.contrib.auth.models import AnonymousUser 

def checkout(request):
    
    if request.method == "POST":  
        ip_address = get_ip(request)
        user_id = request.user
        name = request.POST.get("fname")
        street_number = request.POST.get("street_number")
        city = request.POST.get("city")
        phone_number = request.POST.get("phone_number")
        email_address = request.POST.get("email_adress")
        
        session_id = request.session.session_key
        if not session_id:
            request.session.save()  # Create a new session if not available
            session_id = request.session.session_key
        
        # Retrieve all cart items for the current session
        cart_items = AddToCartItems.objects.filter(user_id = user_id)
        
        if not cart_items.exists():
                return render(request, "allpages/checkout.html", {"error": "No items found in the cart"},)
            
        # Create OrderDetails instances for each cart item
        order_details_list = []
        total_order_price = 0.0
        all_items = []
        
        for cart_item in cart_items:
            # Retrieve subitem instances for the current cart item
            subitem_instances = cart_item.subitem_id.all()
            
            item_id = cart_item.item_id
            quantity = cart_item.quantity
            special_instructions = cart_item.special_instructions
            item_name = cart_item.item_id.item_name
            
            # Calculate total price for the current cart item
            total_price = cart_item.total_price
            total_order_price += total_price
            
            # Create OrderDetails instance
            order_details = OrderDetails.objects.create(
                user_id=user_id,
                item_id=item_id,
                quantity=quantity,
                total_price=total_price,
                special_instructions=special_instructions,
                name=name,
                street_number=street_number,
                city=city,
                phone_number=phone_number,
                email=email_address,
            )
            
            # Assign subitem instances to the OrderDetails instance
            order_details.subitem_id.set(subitem_instances)
            order_details_list.append(order_details)
            all_items.append(item_name)
            
            # Clear cart items after successful checkout
            cart_items.delete()
        try:
            admin_email =  AdminProfile.objects.first()
            email_context = {
                'name': name,
                'street_number': street_number,
                "city" : city,
                'email': email_address,
                'phone': phone_number,
                'item_name': all_items,
                'total_price': total_order_price,
                "admin_name" : admin_email.full_name,
                "ip_address" : ip_address 
            }
            ######## Send Mail to User ##########
            body = render_to_string(
                template_name="mails/order_email_template.html",
                context = email_context
            )
            data={
                "subject":"Your Order",
                "body":body,
                "to_email":email_address
            }
            Mesg.send_email(data,is_content_html=True)
        except Exception as e:
            print(f"Error while sending Email notificaton : {e}")
        
        try:
            whatsapp_data = {
                            'phone_number': phone_number,
                            'subject': 'Order Details',
                            "body_text1":"We are delighted to inform you that your order has been placed Successfully. Here are the details of the order:",
                            "body_text2":f"Item Name : {all_items}, Total Price: ${total_order_price}",
                            "body_text3": " "
                            }
            WhatsappMessage.whatsapp_message(whatsapp_data)
        except Exception as e:
            print(f"Error while sending Whatsapp notificaton")
        ########  Send Email to Admin #######
        if admin_email:
            body2 = render_to_string(
                template_name="mails/order_email_template_admin.html", 
                context = email_context
            ) 
            data2={
                "subject":"New Order",
                "body":body2,
                "to_email":admin_email.email_address
            }
            try:
                Mesg.send_email(data2,is_content_html=True)
            except Exception as e:
                print(f"Error while sending Email notificaton : {e}")
            try:
                whatsapp_data = {
                                'phone_number': admin_email.phone_number,
                                'subject': 'New Order Details',
                                "body_text1":"We are delighted to inform you that a new order has been placed through our online ordering system. Here are the details of the order:",
                                "body_text2":f"Item Name : {all_items}, Total Price: ${total_order_price}",
                                "body_text3": f"Customer Details >>  Name : {name}, Phone Number : {phone_number}, Street number : {street_number}, City : {city}",
                                }
                WhatsappMessage.whatsapp_message(whatsapp_data)
            except Exception as e:
                print(f"Error while sending Whatsapp notificaton")
        return redirect('thankyou')

    else:
        return render(request, "allpages/checkout.html")


def checkout_old(request):
    if request.method == "POST":
        item_id = request.POST.get("itemid")
        subitem_id_data = request.POST.get("subitem_id")        
        subitem_ids = convert_to_list(subitem_id_data)
        total_price = request.POST.get("total_price")
        name = request.POST.get("name")
        # surname = request.POST.get("surname")
        street_number = request.POST.get("street_number")
        city = request.POST.get("city")
        phone_number = request.POST.get("phone_number")
        email_adress = request.POST.get("email_adress")
        ip_address = get_ip(request)
        submission_date = timezone_now().date()
        date_time = timezone_now()
        item_instance = items.objects.filter(id = item_id).first()
        subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
        user = CustomUser.objects.get(id=1)
        # if isinstance(user, AnonymousUser):
        #     form = LoginForm()
        #     return render(request, 'registration/user-login.html', {'form': form})
        # if user:
        #     userId = user
        # else:
        #     userId = None
        order_details = OrderDetails.objects.create(
            user_id = user,
            item_id = item_instance,
            total_price = total_price,
            name = name,
            street_number = street_number,
            city = city,
            phone_number = phone_number,
            email = email_adress
        )
        order_details.subitem_id.set(subitem_instances)
        order_details.save()
        
        admin_email =  AdminProfile.objects.first()
        email_context = {
            "name" : name,
            "street_number" : street_number,
            "city" : city,
            "email":email_adress,
            "phone_number" : phone_number,
            "item_name" : item_instance.item_name,
            "total_price" : total_price,
            "admin_name" : admin_email.full_name,
            "ip_address" : ip_address      
        }
        
        ######## Send Mail to User ##########
        body = render_to_string(
            template_name="mails/order_email_template.html",
            context = email_context
        )
        data={
            "subject":"Your Order",
            "body":body,
            "to_email":email_adress
        }
        Mesg.send_email(data,is_content_html=True)
        try:
            whatsapp_data = {
                            'phone_number': phone_number,
                            'subject': 'Order Details',
                            "body_text1":"We are delighted to inform you that your order has been placed Successfully. Here are the details of the order:",
                            "body_text2":f"Item Name : {item_instance.item_name}, Total Price: ${total_price}",
                            "body_text3": " "
                            }
            WhatsappMessage.whatsapp_message(whatsapp_data)
        except Exception as e:
            print(f"Error while sending Whatsapp notificaton")
        
        ########  Send Email to Admin #######
        if admin_email:
            body2 = render_to_string(
                template_name="mails/order_email_template_admin.html", 
                context = email_context
            ) 
            data2={
                "subject":"New Order",
                "body":body2,
                "to_email":admin_email.email_address
            }
            Mesg.send_email(data2,is_content_html=True)
            try:
                whatsapp_data = {
                                'phone_number': admin_email.phone_number,
                                'subject': 'New Order Details',
                                "body_text1":"We are delighted to inform you that a new order has been placed through our online ordering system. Here are the details of the order:",
                                "body_text2":f"Item Name : {item_instance.item_name}, Total Price: ${total_price}",
                                "body_text3": f"Customer Details >>  Name : {name}, Phone Number : {phone_number}, Street number : {street_number}, City : {city}",
                                }
                WhatsappMessage.whatsapp_message(whatsapp_data)
            except Exception as e:
                print(f"Error while sending Whatsapp notificaton")
        
        return redirect('thankyou')

def reviews(request):
    return render(request, "reviews.html")

def services(request):
    return render(request, "allpages/services.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone")
        reason_contact = request.POST.get("reason_contact")
        message = request.POST.get("message")
        subscribe1 = request.POST.get("subscribe")
        ip_address = get_ip(request)
        submission_date = timezone_now().date()
        date_time = timezone_now()
        
        subscribe = "Yes"
        if subscribe1 is None:
            subscribe = "No"
        
        contactUs(
            name=name,
            email=email,
            phone=phone_number,
            message=message,
            reason_contact=reason_contact,
            subscribe=subscribe,
        ).save()
        
        email_context = {
            "name" : name,
            "email" : email,
            "phone_number" : phone_number,
            "reason_contact" : reason_contact,
            "message" : message,
            "subscription" : subscribe,
            "ip_address" : ip_address,
            "submission_date" : submission_date,
            "date_time" : date_time,
            "ip_address" : ip_address
        }
        
        admin_email =  AdminProfile.objects.first()
        ######## Send Mail to User ##########
        body = render_to_string(
            template_name="contactus/contactus-email.html", 
            context = email_context
        )
        data={
            "subject":"Contact-Us",
            "body":body,
            "to_email":email
        }
        try:
            Mesg.send_email(data,is_content_html=True)
        except Exception as e:
            print(f"Error while sending Email notificaton : {e}")
        
        ########  Send Email to Admin #######
        if admin_email:
            body2 = render_to_string(
                template_name="mails/contact_email.html", 
                context = email_context
            ) 
            data2={
                "subject":"Contact-Us",
                "body":body2,
                "to_email":admin_email.email_address
            }
            try:
                Mesg.send_email(data2,is_content_html=True)
            except Exception as e:
                print(f"Error while sending Email notificaton : {e}")
            
        return redirect('thankyou')
    else:
        return render(request, "contactus/contact.html")
    
    
def thankyou_page(request):
    return render(request, "thankyou/thank-you.html")

def index_main(request):
    menu_list = items.objects.filter(status=1, is_deleted=False).order_by("display_order_for_our_menu")
    special_offers = specialoffers.objects.filter(status=1,is_deleted=False).order_by("display_order")
    return render(request,"gourments/index-main.html",{"menu_list":menu_list,"offers":special_offers,'MEDIA_URL':settings.MEDIA_URL,})

########################### Registration and Login Systems ##########################

def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            print("User",user)
            # Perform any additional actions upon successful registration
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

from django.contrib.auth import authenticate

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        print("Details", username, password)

        if username and password:
            user = authenticate(username=username, password=password)
            print("USER", user)

            if not user:
                # If not authenticated with username, try with mobile number
                try:
                    user = CustomUser.objects.get(mobile=username)
                    user = authenticate(username=user.email, password=password)
                    print("Mobile User", user)
                except CustomUser.DoesNotExist:
                    user = None

                if user is None:
                    return render(request, 'gourments/index-main.html', {'error': "User Not Found"})
                else:
                    login(request, user)
                    print("LOGIN", user)
                    print("Session data after login:", request.session.items())
                    return render(request, 'gourments/index-main.html')
            else:
                login(request, user)
                print("LOGIN", user)
                print("Session data after login:", request.session.items())
                return render(request, 'gourments/index-main.html')
        else:
            return render(request, 'gourments/index-main.html', {'error': "Please provide both username and password"})

    # For non-POST requests, show the login page
    return render(request, 'gourments/index-main.html')
    
# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             # Redirect to a success URL or homepage upon successful login
#             return redirect('index')  # Replace 'home' with your desired URL name
#     else:
#         form = LoginForm()
#     return render(request, 'gourments/index-main.html', {'form': form})

def check_session_view(request):
    print("Session data on page load:", request.session.items())
    return render(request, 'gourments/index-main.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def get_image_url(item):
    return item.image.url if item.image else None
def category_detail(request, category_id):
    #category = get_object_or_404(category, pk=category_id)
    
    items_list = items.objects.filter(category_id=category_id, popular=0)

    item_list = [
        {
            'name': item.item_name,
            'price': item.price,
            'image': get_image_url(item),
            'item_desc': item.item_desc,
            'id': item.id
        }
        for item in items_list
    ]

    cat_list = category.objects.filter(id=category_id)
    cat_list = [{'name': cat.category_name} for cat in cat_list]

    response_data = {'items': item_list, 'cat': cat_list}
    
    return JsonResponse(response_data, safe=False)