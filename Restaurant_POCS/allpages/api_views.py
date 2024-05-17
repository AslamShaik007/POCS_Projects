from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from control_panel.models import category, items, SubItems, AdminProfile, BookTheTable, AddToCartItems, OrderDetails

from control_panel.utils import email_render_to_string, timezone_now, hrs_to_mins, mins_to_hrs, Mesg, format_api_response, get_ip,WhatsappMessage
from django.template.loader import render_to_string
from twilio.rest import Client
from config_poc.settings import twilio_account_sid, twilio_auth_token
from allpages.models import CustomUser


class GetMenuItemsAndSubItemsAPIView(APIView):
    
    model = category
    
    def get(self, request, *args, **kwargs):
        
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
                        'selection_type': subitem.selection_type,
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
        
        return Response(
            {
                "data":category_data,
                'message': 'data fetched Successfully'
            },
            status=status.HTTP_200_OK
            )
        
        
class UserTableBookingAPIView(APIView):
    """
    API endpoint for handling table bookings by users.

    This endpoint allows users to book tables in the system.

    Also Send Email to the restaurent Admin And User
    """
    model = BookTheTable

    def is_update_allowed(booked_time, updating_time, grace_period_minutes=5):
        # Convert time strings to datetime objects
        booked_time_obj = booked_time
        updating_time_obj = updating_time

        # Calculate time difference
        time_difference = updating_time_obj - booked_time_obj

        # Calculate difference in minutes
        difference_in_minutes = time_difference.total_seconds() / 60

        # Check if updating is allowed based on the grace period
        return difference_in_minutes <= grace_period_minutes
    
    def get(self, request, *args, **kwargs):
        params = request.query_params
        data = self.model.objects.filter(is_deleted = False).values().order_by("-id")
        return Response(
            {"data":data},
            status=status.HTTP_200_OK
            )
    
    def post(self, request, *args, **kwargs):
        data = request.data
        try:
            _created = self.model.objects.create(**data)
            if _created:
                try:
                    try:
                        client = Client(twilio_account_sid, twilio_auth_token) 
                    except:
                        pass
                    # Send mail to User
                    name = data.get("name").title()
                    user_email = data.get("email_address")
                    phone_number = data.get("phone_number")
                    total_members = data.get("total_members")
                    timings = data.get("timings")

                    body1=f'Hello {name},\n\nWe are pleased to inform you that your table booking has been successfully confirmed. Below are the details:\n\n*Total Members : {total_members}\n*Timings : {timings} \n\nIf you have any questions or need further assistance, please feel free to contact us.\n\nThanks & Regards,\nRestaurent POC'  
                    data={
                        'subject':'Table Booking Conformation',
                        'body':body1,
                        'to_email':data.get("email_address")
                    }
                    Mesg.send_email(data)
                    # Send Email to the Admin
                    body2=f'Hello Admin,\n\nThis is to inform you that {name} has successfully booked a table. Please find the details below:\n\n*Phone Number : {phone_number}\n*Email : {user_email}\n*Total Members : {total_members}\n*Timings : {timings} \n\nThanks & Regards,\nRestaurent POC'  
                    data={
                        'subject':'Table Booked',
                        'body':body2,
                        'to_email':"suresh.k@pranathiss.com"
                    }
                    Mesg.send_email(data)
                    # ext = '+91'
                    # phone = "9502241772"
                    # to_number = f"whatsapp:{ext+phone}"
                    # # send whatsapp messages
                    # message = client.messages.create(
                    #     to=f"whatsapp:{ext+'8142206727'}",
                    #     from_='whatsapp:+14155238886',
                    #     body=body1
                    # )
                    # # send text messages
                    # text_message = client.messages.create(
                    # to='+918142206727',
                    # from_='+12403396750',
                    # body=body1
                    # )

                except Exception as e:
                    print(f"Exception in sending Email {str(e)}") 
                return Response(
                    {"msg": "Successfully Booked the Table"},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"data":f"Excpetion at {str(e)}",},
                status=status.HTTP_404_NOT_FOUND
            )
    def patch(self, request, *args, **kwargs):
        data = request.data
        try:
            from datetime import time
            current_datetime = timezone_now().time()
            updating_time = current_datetime.strftime("%H:%M")
            up_hours,up_minutes = map(int, updating_time.split(':'))
            updating_time = hrs_to_mins(up_hours,up_minutes)
            obj = self.model.objects.get(id=data.get("id"))
            order_time = obj.created_at
            order_time = order_time.strftime("%H:%M")
            or_hours, or_minutes = map(int, order_time.split(':'))
            order_time = hrs_to_mins(or_hours, or_minutes)
            time_difference = updating_time - order_time

            if time_difference < 66:
                return Response(
                    {"msg":"Object doesnot exist"}
                )
            
            # print("ORDER,",order_time)

            if not obj:
                return Response(
                    {"msg":"Object doesnot exist"}
                )
            return Response(
                {"msg":"Successlly Updated the Table"},
                status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"data":f"Excpetion at {str(e)}",},
                status=status.HTTP_404_NOT_FOUND
            )
        

class AddItemWithSubitemAPIView(APIView):

    model = items
    
    def post(self, request, *args, **kwargs):
        data = request.data
        category_id = data.pop("category_id")  # Assuming category_id is passed in request data
        try:
            category_instance = category.objects.get(id=category_id)
        except category.DoesNotExist:
            return Response({"error": "Category does not exist"}, status=status.HTTP_404_NOT_FOUND)

        sub_items = data.pop("sum_items", [])

        # Now, create the Items instance using the retrieved category_instance
        obj = items.objects.create(category_id=category_instance,**data)
        if sub_items:
            for item in sub_items:
                sub_obj = SubItems.objects.create(item_id_id = obj.id,**item)
            
        return Response(
            {
                "data","Success"
            }
        )


class AddAdminProfile(APIView):

    model = AdminProfile

    def get(self, request, *args, **kwargs):

        data = request.data
        admin_details = AdminProfile.objects.filter().values().first()
        return Response(
            {"data":admin_details},
            status=status.HTTP_200_OK
            )
    
    def patch(self, request, *args, **kwargs):
        
        data = request.data
        obj = AdminProfile.objects.filter(id=data.get("id")).update(**data)
        if obj:
            return Response(
                {"data":"success"},
                status=status.HTTP_200_OK
            )
            
            
class AddToCartAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            # Initialize or retrieve session key
            session_id = request.session.session_key
            if not session_id:
                request.session.save()  # Create a new session if not available
                session_id = request.session.session_key
            
            print("SESSION ID:", session_id)
            item_id = data.get('itemid')
            quantity = data.get("quantity")
            subitem_ids = data.get("subitem_ids")
            special_instructions = data.get("special_instructions")
            
            item_instance = items.objects.get(id=item_id)
            
            # Check if cart item already exists for this session and item
            cart_item = AddToCartItems.objects.filter(
                user_id = 1,
                item_id=item_instance
            ).first()
            
            if cart_item:
                # Cart item exists, update quantity and total price
                cart_item.quantity += int(quantity)
                cart_item.total_price = item_instance.price * cart_item.quantity
                cart_item.special_instructions = special_instructions
                
                cart_item.subitem_id.clear()

                # Add selected subitems to existing cart item
                subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
                if subitem_instances:
                    for i in subitem_instances:
                        cart_item.total_price += i.price
                cart_item.subitem_id.add(*subitem_instances)

                cart_item.save()
            else:
                subitems = SubItems.objects.filter(pk__in=subitem_ids)
                
                total_price = item_instance.price * int(quantity)
                # Calculate total price
                if subitem_ids:
                    for subitem in subitems:
                        total_price += subitem.price
                user = CustomUser.objects.get(id=1)
                # Create AddToCartItems instance
                cart_item = AddToCartItems.objects.create(
                    session_id = session_id,
                    user_id = user,
                    item_id=item_instance,
                    quantity=quantity,
                    total_price=total_price,
                    special_instructions=special_instructions
                )
                subitem_instances = SubItems.objects.filter(pk__in=subitem_ids)
                cart_item.subitem_id.set(subitem_instances)
                cart_item.save()
            return Response(
                {"data":"Item added to cart successfully"},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"data":f"Exception {e}"},
                status=status.HTTP_400_BAD_REQUEST
            )


class CheckoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            ip_address = get_ip(request)
            # Retrieve user (assuming user is authenticated)
            user = CustomUser.objects.get(id=1)
            item_ids = data.get("item_ids")
            name = data.get("name")
            street_number = data.get("street_number")
            city = data.get("city")
            phone_number = data.get("phone_number")
            email_address = data.get("email_adress")
            # Retrieve session ID
            session_id = request.session.session_key
            if not session_id:
                request.session.save()  # Create a new session if not available
                session_id = request.session.session_key
            
            # Retrieve all cart items for the current session
            cart_items = AddToCartItems.objects.filter(user_id = user)
            
            if not cart_items.exists():
                    return Response({"error": "No items found in the cart"},)
                
            # Create OrderDetails instances for each cart item
            order_details_list = []
            total_order_price = 0
            all_items = []
            
            for cart_item in cart_items:
                item_name = cart_item.item_id.item_name
                item = cart_item.item_id
                subitem_instances = cart_item.subitem_id.all()
                print("SUB INST",subitem_instances)
                # subitem_instances = SubItems.objects.filter(item_id=item)
                
                # # Calculate total price for the order including subitems
                # # total_price = item_instance.price * quantity
                # # subitems_total_price = sum(subitem.price for subitem in subitem_instances)
                # # total_price += subitems_total_price
                total_price = cart_item.total_price
                total_order_price += total_price
                print("Total Price",total_price, total_order_price)
                print("GRAND TOTAL",total_order_price)   
                
                #Create OrderDetails instance
                order_details = OrderDetails.objects.create(
                    user_id=user,
                    item_id=cart_item.item_id,
                    # subitem_id=subitem_instances,
                    quantity=cart_item.quantity,
                    total_price=cart_item.total_price, 
                    special_instructions=cart_item.special_instructions,
                    name=name, 
                    street_number=street_number, 
                    city=city, 
                    phone_number=phone_number, 
                    email=email_address,
                )
                
                order_details.subitem_id.set(subitem_instances)
                
                order_details_list.append(order_details)
                all_items.append(item_name)
                
            
                
                # Clear cart items after successful checkout
                cart_items.delete()
            print("GRAND TOTAL",total_order_price)
            # print("ORDER Details",order_details)
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
            print("EMAIL Context",email_context)
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
            try:
                Mesg.send_email(data,is_content_html=True)
            except Exception as e:
                print(f"Error while sending Email notificaton {e}")
                
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
                    print(f"Error while sending Email notificaton {e}")
                
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
            
            return Response({"data": "Order placed successfully"}, status=status.HTTP_201_CREATED)
        
        except items.DoesNotExist:
            return Response({"error": "One or more items not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except SubItems.DoesNotExist:
            return Response({"error": "One or more subitems not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({"error": f"Exception: {e}"}, status=status.HTTP_400_BAD_REQUEST)
