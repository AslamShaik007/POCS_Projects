
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import (category, 
                     booking_details, 
                     items, cms, contactUs, 
                     all_settings, specialoffers, 
                     AllTables, BookTheTable,
                     booking_contact,
                     AdminProfile,
                     OrderDetails)  # Importing model Users and etc...

from .form import *

from urllib import request
from django.http import JsonResponse

from django.http import JsonResponse
from django.core.mail import send_mail

from itertools import zip_longest
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse  
from control_panel.utils import email_render_to_string, timezone_now, hrs_to_mins, mins_to_hrs,WhatsappMessage, Mesg
# from twilio.rest import Client
from config_poc.settings import twilio_account_sid, twilio_auth_token
from datetime import datetime, timedelta 





@csrf_exempt
def Login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        print("username,password",username,password)

        user = authenticate(username=username,password=password)
        print("User",user)
        if user is not None:
            ud = category.objects.all().values().order_by('display_order').filter(is_deleted = False)
            udData = {
                'activefor':'ud_category',
                'page_title':'Category',
                'MEDIA_URL':settings.MEDIA_URL,
                'listings':ud
            }
            login(request,user)
            return render(request,'controlPanel/category/list-category.html',udData)
        else:
            context = {"data":"Invalid Username or Password"}
            return render(request, 'controlPanel/login/login.html',context)        
    return render(request, 'controlPanel/login/login.html')

def LogoutUser(request):
    logout(request)
    return redirect("admin_login")


# @login_required(login_url="login")
def dashboard(request):
    return render(request, 'controlPanel/category/list-category.html')

########################### Admin Profile ###############################

#@login_required(login_url="login")   
def AdminProfileDetails(request):
    
    allData  = AdminProfile.objects.filter(is_deleted = False)
    
    udData = {
        'activefor':'ud_profile',
        'page_title':'Admin Profile Details',
        'listings':allData,
        'MEDIA_URL':settings.MEDIA_URL
    }
    return render(request, 'controlPanel/admin_details/admin_profile.html',udData)

#####################################   Category Details ##############################

#@login_required(login_url="login")
def listCategory(request):
    ud = category.objects.all().values().order_by('display_order').filter(is_deleted = False)
    udData = {
        'activefor':'ud_category',
        'page_title':'Category',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':ud
    }
    return render(request, 'controlPanel/category/list-category.html',udData)


#@login_required(login_url="login")
def addCategory(request):
    
    if request.POST.get('category_name') :
        allData = request.POST
        allFiles = request.FILES
        form = CategoryForm(data=allData, files=allFiles)
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            errors = form.errors.as_json()
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.','errors': errors}
        
        return JsonResponse(msg, safe=False)
    else:
        udData = {
            'activefor':'ud_category',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Category'
        }
        return render(request, 'controlPanel/category/add-category.html',udData)


#@login_required(login_url="login")
def updateCategory(request, baseId):
    
    if baseId and request.method == 'POST':
        
        obj = category.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
        form = CategoryForm(data=allData, files=allFiles, instance=obj)
        if form.is_valid():
            form.save()
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        ud = category.objects.filter(id=baseId, is_deleted = False).first()
        udData = {
            'data':ud,
            'activefor':'ud_category',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Category'
        }
        return render(request, 'controlPanel/category/update-category.html',udData)   

#@login_required(login_url="login")
def deleteCategory(request):
        
    if request.method == "POST":
        
        allPostData = request.POST.items()
        # data = category.objects.get(id=request.POST.get('baseId'))
        # if data.delete():
        savedData = category.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if savedData:
            msg = {'response': 'success', 'msg': 'Your Data Has Been Successfully Deleted.'}
        else:
            msg = {'response': 'notdeleted', 'msg': 'Your Data Has Not Been Deleted.'}
        
        return JsonResponse(msg, safe=False)         
    
#####################################   Order Details ##############################    
#@login_required(login_url="login")
def listOrder(request):
    # data = OrderDetails.objects.filter(is_deleted = False).order_by("-id").values(
    #     "item_id__item_name","total_price","name","surname","street_number","city","phone_number","email","created_at"
    # )
    # response_data = {
    #     'activefor':'ud_order',
    #     'page_title':'Order',
    #     'MEDIA_URL':settings.MEDIA_URL,
    #     'listings':data,
    # }   
    # return render(request, 'controlPanel/order/list-order-details.html', response_data)  
    order_details_with_subitem_titles = OrderDetails.objects.select_related('item_id').prefetch_related('subitem_id').order_by("-id")
    order_details_list = []
    for order_detail in order_details_with_subitem_titles:
        order_detail_dict = {
            "item_name": order_detail.item_id.item_name,
            "quantity" : order_detail.quantity,
            "total_price": order_detail.total_price,
            "name": order_detail.name,
            "surname": order_detail.surname,
            "street_number": order_detail.street_number,
            "city": order_detail.city,
            "phone_number": order_detail.phone_number,
            "email": order_detail.email,
            "created_at":order_detail.created_at,
            "sub_items": [subitem.sub_item_title for subitem in order_detail.subitem_id.all()]
        }
        order_details_list.append(order_detail_dict)
    response_data = {
        'activefor':'ud_order',
        'page_title':'Order',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':order_details_list,
    }   
    return render(request, 'controlPanel/order/list-order-details.html', response_data)  
   

#@login_required(login_url="login")
def listOrderDetails(request, baseId):
    ud = booking_details.objects.all().values().filter(inserted_id=baseId)
    total_price = sum(float(item['total']) for item in ud)

    udData = {
        'activefor':'ud_order',
        'page_title':'Order',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':ud,
        'subtotal':total_price
    }
    return render(request, 'controlPanel/order/list-order-details.html', udData)     

#####################################   Item Details ##############################


def get_category_name(category_id):
    # Your logic to retrieve the category name goes here
    categorys = category.objects.filter(id=category_id).first()
    return categorys.category_name    

#@login_required(login_url="login")   
def listItem(request):
    all_items  = items.objects.all().values(
        'id','category_id__category_name','item_name','item_desc','price','image','popular','status',
        'display_order','display_order_for_special_item','status_for_special_item','created_at'
    ).order_by('display_order').filter(is_deleted = False)
    # print("allData",all_items)
    item_data = []
    for item in all_items:
        subitems = SubItems.objects.filter(item_id=item['id']).values()  # Fetch subitems related to the item
        item_data.append({
            'item': item,
            'subitems': subitems
        })
    udData = {
        'activefor':'ud_item',
        'page_title':'Item',
        'listings':item_data,
        'MEDIA_URL':settings.MEDIA_URL,
        'ud':item_data
    }
    return render(request, 'controlPanel/item/list-item.html',udData)

#@login_required(login_url="login")
def addItemBkp(request):
    
    if request.POST.get('category_id') :
        
        category_id         = request.POST.get('category_id')
        item_name           = request.POST.get('item_name')
        item_desc           = request.POST.get('item_desc')
        price               = request.POST.get('price')
        popular             = request.POST.get('popular')
        status              = request.POST.get('status')
        display_order       = request.POST.get('display_order')
        image               = request.FILES.get('image')
        
        # insert_data = items(category_name=category_name, category_desc=category_desc, status=status, display_order=display_order)
        # insert_data.save()
        savedData = items.objects.create(category_id=category_id, item_name=item_name, item_desc=item_desc, price=price, popular=popular, status=status, image=image, display_order=display_order)
        if savedData:
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        catData = category.objects.all().values().order_by('display_order').filter(is_deleted = False)
        udData = {
            'activefor':'ud_item',
            'catData':catData,
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Item'
        }
        return render(request, 'controlPanel/item/add-item.html',udData)

#@login_required(login_url="login")
def addItem(request):
    if request.POST.get('category_id') :

        allData = request.POST
        allFiles = request.FILES
        print("ALL DATA",allData)
        # allData.display_order = request.POST.get('displayOrder')
                
        form = ItemForm(data=allData, files=allFiles)

        if form.is_valid():
            form.save()
            data = form.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            errors = form.errors.as_json()
            msg = {
                'response': 'notSaved',
                'title': 'Not Saved!',
                'icon': 'error',
                'msg': 'Your data has not been saved. Please try again.',
                'errors': errors
            }
        
        
        return JsonResponse(msg, safe=False)
    else:
        catData = category.objects.all().values().order_by('display_order').filter(is_deleted = False)
        udData = {
            'activefor':'ud_item',
            'catData':catData,
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Item'
        }
        return render(request, 'controlPanel/item/add-item.html',udData)

#@login_required(login_url="login")  
def updateItemBkp(request, baseId):
    
    if baseId and request.method == 'POST':
        
        category_id         = request.POST.get('category_id')
        item_name           = request.POST.get('item_name')
        item_desc           = request.POST.get('item_desc')
        price               = request.POST.get('price')
        popular             = request.POST.get('popular')
        status              = request.POST.get('status')
        display_order       = request.POST.get('display_order')
        image               = request.FILES["image"]
                
        # items.objects.filter(id=baseId).count()
        # if email and items.objects.filter(email=email).exclude(id=baseId).count() < 1:
        # insert_data.save()
        
        savedData = items.objects.filter(id=baseId).update(category_id=category_id, item_name=item_name, item_desc=item_desc, price=price, popular=popular, status=status, image=image, display_order=display_order)
        if savedData:
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        ud      = items.objects.filter(id=baseId, is_deleted = False).first()
        catData = category.objects.all().values().order_by('display_order').filter(is_deleted = False)
        udData = {
            'data':ud,
            'catData':catData,
            'activefor':'ud_item',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Item'
        }
        return render(request, 'controlPanel/item/update-item.html',udData)   

#@login_required(login_url="login")   
def updateItem(request, baseId):
    
    if baseId and request.method == 'POST':
        
        updateData = items.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
                
        # allData.display_order = request.POST.get('displayOrder')
                
        # savedData = ItemForm(data=allData, files=allFiles, instance=updateData)
        savedData = ItemForm(data=allData, files=allFiles, instance=updateData)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            errorsUd = ItemForm()
            errorUd = {
                'allFormErrors':errorsUd
            }
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.', 'errors':errorUd}
        
        return JsonResponse(msg, safe=False)
    else:
        ud      = items.objects.filter(id=baseId, is_deleted = False).first()
        catData = category.objects.all().values().order_by('display_order').filter(is_deleted = False)
        udData = {
            'data':ud,
            'catData':catData,
            'activefor':'ud_item',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Item'
        }
        return render(request, 'controlPanel/item/update-item.html',udData)

#@login_required(login_url="login")    #http://127.0.0.1:8000/cpanel/list-order/  
def deleteItem(request):
        
    if request.method == "POST":
        
        allPostData = request.POST.items()
        # data = items.objects.get(id=request.POST.get('baseId'))
        # if data.delete():
        savedData = items.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if savedData:
            msg = {'response': 'success', 'msg': 'Your Data Has Been Successfully Deleted.'}
        else:
            msg = {'response': 'notdeleted', 'msg': 'Your Data Has Not Been Deleted.'}
        
        return JsonResponse(msg, safe=False)         

#@login_required(login_url="login")  
def listSubItem(request):
    query  = SubItems.objects.filter(status = 1, is_deleted = False).values(
        "id","item_id__item_name","sub_item_title","price","short_description","status","created_at","updated_at"
    ).order_by("-item_id")
    udData = {
        'activefor':'ud_subitem',
        'page_title':'SubItem',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':query
    }
    return render(request, 'controlPanel/subitems/list-sub-item.html',udData)

#@login_required(login_url="login")  
def addSubItem(request):
    if request.POST.get('item_id'):
        allData = request.POST
        form = SubItemForm(data=allData)
        
        if form.is_valid():
            form.save()
            data = form.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        
        else:
            errorsUd = form.errors.as_json()
            errorUd = {
                'allFormErrors':errorsUd
            }
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.', 'errors':errorUd}
        return JsonResponse(msg, safe=False)
    else:
        subitemData = items.objects.filter(is_deleted = False,status=1)
        udData = {
            'activefor':'ud_subitem',
            'subData':subitemData,
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Item'
        }
        return render(request, 'controlPanel/subitems/add-sub-item.html', udData)

#@login_required(login_url="login")     
def updateSubItem(request, baseId):
    
    if baseId and request.method == 'POST':
        updateData = SubItems.objects.get(id=baseId)
        allData = request.POST
        savedData = SubItemForm(data=allData,instance=updateData)
        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            errorsUd = savedData.errors.as_json()
            errorUd = {
                'allFormErrors':errorsUd
            }
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.', 'errors':errorUd}
        return JsonResponse(msg, safe=False)
    else:
        itemData = items.objects.filter(is_deleted = False,status=1)
        subdata = SubItems.objects.filter(id=baseId, is_deleted = False).first()
        udData = {
            'data':subdata,
            'activefor':'ud_subitem',
            'subData':itemData,
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'SubItem'
        }
        return render(request, 'controlPanel/subitems/update-sub-item.html', udData)


#@login_required(login_url="login")    #http://127.0.0.1:8000/cpanel/list-order/  
def deleteSubItem(request):
        
    if request.method == "POST":
        print("ID",request.POST.get('baseId'))
        savedData = SubItems.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if savedData:
            msg = {'response': 'success', 'msg': 'Your Data Has Been Successfully Deleted.'}
        else:
            msg = {'response': 'notdeleted', 'msg': 'Your Data Has Not Been Deleted.'}
        
        return JsonResponse(msg, safe=False)    

#####################################   Gallery Details ##############################  

#@login_required(login_url="login")   
def listGallery(request): #http://127.0.0.1:8000/cpanel/list-gallery/
    
    allData  = gallery.objects.all().values().order_by('display_order').filter(is_deleted = False)
            
    udData = {
        'activefor':'ud_gallery',
        'page_title':'Gallery',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':allData
    }
    return render(request, 'controlPanel/gallery/list-gallery.html',udData)

#@login_required(login_url="login")
def addGallery(request):
    
    if request.method == 'POST' :
        
        allData = request.POST
        allFiles = request.FILES
        
        print(allFiles)
                        
        form = GalleryForm(data=allData, files=allFiles)

        if form.is_valid():
            form.save()
            data = form.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        udData = {
            'activefor':'ud_gallery',
            'page_title':'Gallery',
            'MEDIA_URL':settings.MEDIA_URL
        }
        return render(request, 'controlPanel/gallery/add-gallery.html',udData)

#@login_required(login_url="login")        
def updateGallery(request, baseId):
    
    if baseId and request.method == 'POST':
        
        updateData = gallery.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
                                
        savedData = GalleryForm(data=allData, files=allFiles, instance=updateData)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        ud      = gallery.objects.filter(id=baseId, is_deleted = False).first()
        udData = {
            'data':ud,
            'activefor':'ud_gallery',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Gallery'
        }
        return render(request, 'controlPanel/gallery/update-gallery.html',udData)

#@login_required(login_url="login")    
def deleteGallery(request):
        
    if request.method == "POST":
        
        savedData = gallery.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if savedData:
            msg = {'response': 'success', 'msg': 'Your Data Has Been Successfully Deleted.'}
        else:
            msg = {'response': 'notdeleted', 'msg': 'Your Data Has Not Been Deleted.'}
        
        return JsonResponse(msg, safe=False)         

#####################################   Content Details ##############################  

#@login_required(login_url="login")   
def listContent(request):
    
    allData  = cms.objects.all().values().filter(is_deleted = False)

    # all = cms.objects.filter(status=1).first()
    
    udData = {
        'activefor':'ud_content',
        'page_title':'Content Page',
        'listings':allData,
        'MEDIA_URL':settings.MEDIA_URL
    }
    return render(request, 'controlPanel/contents/list-contents.html',udData)

#@login_required(login_url="login")
def addContent(request):
    
    if request.method == 'POST' :
        
        allData = request.POST
        allFiles = request.FILES
                        
        savedData = ContentForm(data=allData, files=allFiles)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        udData = {
            'activefor':'ud_content',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Content Page'
        }
        return render(request, 'controlPanel/contents/add-contents.html',udData)

#@login_required(login_url="login")     
def updateContent(request, baseId):
    
    if baseId and request.method == 'POST':
        
        updateData = cms.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
                                
        savedData = ContentForm(data=allData, files=allFiles, instance=updateData)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        ud      = cms.objects.filter(id=baseId, is_deleted = False).first()
        udData = {
            'data':ud,
            'activefor':'ud_content',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Content Page'
        }
        return render(request, 'controlPanel/contents/update-contents.html',udData)

#@login_required(login_url="login")  
def deleteContent(request):
        
    if request.method == "POST":
                
        savedData = cms.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if savedData:
            msg = {'response': 'success', 'msg': 'Your Data Has Been Successfully Deleted.'}
        else:
            msg = {'response': 'notdeleted', 'msg': 'Your Data Has Not Been Deleted.'}
        
        return JsonResponse(msg, safe=False)         

#####################################   Contact Us Details ##############################  

#@login_required(login_url="login")   
def listContactUs(request):
    
    allData  = contactUs.objects.all().values().filter(is_deleted = False)
    
    udData = {
        'activefor':'ud_contactus',
        'page_title':'Contact Us Details',
        'listings':allData,
        'MEDIA_URL':settings.MEDIA_URL
    }
    return render(request, 'controlPanel/contact-us/list-contact-us.html',udData)

#####################################   All Setting Details ##############################  

#@login_required(login_url="login")   
def updateAllSetting(request, baseId):
    
    if baseId and request.method == 'POST':
        
        updateData = all_settings.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
                                
        savedData = AllSettingForm(data=allData, files=allFiles, instance=updateData)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        ud = all_settings.objects.filter(id=baseId).first()
        udData = {
            'data':ud,
            'activefor':'ud_allsetting',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'All Setting'
        }
        return render(request, 'controlPanel/all-setting/update-all-setting.html',udData)
    
#####################################   Testimonial Details ##############################  

#@login_required(login_url="login")
def listTestimonial(request): #http://127.0.0.1:8000/cpanel/list-testimonial/
    
    allData  = testimonial.objects.all().values().order_by('display_order').filter(is_deleted = False)
            
    udData = {
        'activefor':'ud_testimonial',
        'page_title':'Testimonial',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':allData
    }
    return render(request, 'controlPanel/testimonial/list-testimonial.html',udData)

#@login_required(login_url="login")
def addTestimonial(request):
    
    if request.method == 'POST' :
        
        allData = request.POST
        allFiles = request.FILES
        
        print(allFiles)
                        
        form = TestimonialForm(data=allData, files=allFiles)

        if form.is_valid():
            form.save()
            data = form.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        udData = {
            'activefor':'ud_testimonial',
            'page_title':'Testimonial',
            'MEDIA_URL':settings.MEDIA_URL
        }
        return render(request, 'controlPanel/testimonial/add-testimonial.html',udData)

#@login_required(login_url="login")        
def updateTestimonial(request, baseId):
    
    if baseId and request.method == 'POST':
        
        updateData = testimonial.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
                                
        savedData = TestimonialForm(data=allData, files=allFiles, instance=updateData)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        ud      = testimonial.objects.filter(id=baseId, is_deleted = False).first()
        udData = {
            'data':ud,
            'activefor':'ud_testimonial',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Testimonial'
        }
        return render(request, 'controlPanel/testimonial/update-testimonial.html',udData)

#@login_required(login_url="login")    
def deleteTestimonial(request):
        
    if request.method == "POST":
        
        savedData = testimonial.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if savedData:
            msg = {'response': 'success', 'msg': 'Your Data Has Been Successfully Deleted.'}
        else:
            msg = {'response': 'notdeleted', 'msg': 'Your Data Has Not Been Deleted.'}
        
        return JsonResponse(msg, safe=False)         


#####################################   Special Details ##############################  

#@login_required(login_url="login")    
def listSpecial(request):
    
    allData  = specialoffers.objects.all().values().order_by('display_order').filter(is_deleted = False)
            
    udData = {
        'activefor':'ud_special',
        'page_title':'Special Details Page',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':allData
    }
    return render(request, 'controlPanel/special/list-special.html',udData)

#@login_required(login_url="login")
def addSpecial(request):
    
    if request.method == 'POST' :
        
        allData = request.POST
        allFiles = request.FILES
                                
        form = SpecialForm(data=allData, files=allFiles)

        if form.is_valid():
            form.save()
            data = form.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            errorsUd = SpecialForm()
            errorUd = {
                'allFormErrors':errorsUd
            }
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.', 'errors':errorUd}
        
        return JsonResponse(msg, safe=False)
    else:
        udData = {
            'activefor':'ud_special',
            'page_title':'Special Details Page',
            'MEDIA_URL':settings.MEDIA_URL
        }
        return render(request, 'controlPanel/special/add-special.html',udData)

#@login_required(login_url="login")       
def updateSpecial(request, baseId):
    
    if baseId and request.method == 'POST':
        
        updateData = specialoffers.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
                                        
        savedData = SpecialForm(data=allData, files=allFiles, instance=updateData)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            
            errorsUd = SpecialForm()
            args = {
                'allFormErrors':errorsUd
            }
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.', 'errors':args}
        
        return JsonResponse(msg, safe=False)
    else:
        ud      = specialoffers.objects.filter(id=baseId, is_deleted = False).first()
        udData = {
            'data':ud,
            'activefor':'ud_special',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Special Details Page'
        }
        return render(request, 'controlPanel/special/update-special.html',udData)

#@login_required(login_url="login")   
def deleteSpecial(request):
        
    if request.method == "POST":
        
        savedData = specialoffers.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if savedData:
            msg = {'response': 'success', 'msg': 'Your Data Has Been Successfully Deleted.'}
        else:
            msg = {'response': 'notdeleted', 'msg': 'Your Data Has Not Been Deleted.'}
        
        return JsonResponse(msg, safe=False)         


############################### Admin ADD Tables ################################## 

#@login_required(login_url="login") 
def AdminAllTablesAddView(request):
    
    if request.POST.get('table_name') :
        table_name = request.POST.get('table_name')
        no_of_seats = request.POST.get('no_of_seats')
        status = request.POST.get('status')
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')
        all_tables = AllTables.objects.filter(table_name=table_name,is_deleted=False).first()
        if all_tables:
            return JsonResponse(
                {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': "The Table name must be Unique"
                }, 
                safe=False
            )
        _created = AllTables.objects.create(
            table_name=table_name, 
            no_of_seats=no_of_seats, 
            status=status, 
            from_time=from_time, 
            to_time=to_time)
        if _created:
            msg = {
                'response': 'success', 
                'title':'Data Saved!', 
                'icon':'success',  
                'msg': 'Your data has been successfully saved.'
            }
        else:
            msg = {
                'response': 'notSaved', 
                'title':'Not Saved!', 
                'icon':'error', 
                'msg': 'Your data has not been saved. Please try again.'
            }
        return JsonResponse(
            msg, safe=False
        )
    else:
        context = {
            'activefor':'ud_tables',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Tables'
        }
        return render(request, 'controlPanel/add_tables/add_table.html',context)



#@login_required(login_url="login") 
def ListTablesView(request):
    data = AllTables.objects.all().values().order_by('-id').filter(is_deleted = False)
    context = {
        'activefor':'ud_tables',
        'page_title':'Tables',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':data
    }
    return render(request, 'controlPanel/add_tables/list_table.html',context)

#@login_required(login_url="login") 
def UpdateTablesView(request,baseId):
        
    if baseId and request.method == 'POST':
        table_name = request.POST.get('table_name')
        no_of_seats = request.POST.get('no_of_seats')
        status = request.POST.get('status')
        from_time = request.POST.get('from_time')
        to_time = request.POST.get('to_time')

        all_tables = AllTables.objects.filter(table_name=table_name,is_deleted=False).exclude(id=baseId).first()
        if all_tables:
            return JsonResponse(
                {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': "The Table name must be Unique"
                }, 
                safe=False
            )

        created = AllTables.objects.filter(id=baseId).update(
            table_name=table_name, 
            no_of_seats=no_of_seats, 
            status=status,
            from_time=from_time, 
            to_time=to_time
        )
        if created:
            msg = {
                'response': 'success', 
                'title':'Data Saved!', 
                'icon':'success',  
                'msg': 'Your data has been successfully saved.'
            }
        else:
            msg = {
                'response': 'notSaved', 
                'title':'Not Saved!', 
                'icon':'error', 
                'msg': 'Your data has not been saved. Please try again.'
            }
        return JsonResponse(
            msg, safe=False
        )
    else:
        data = AllTables.objects.filter(id=baseId, is_deleted = False).first()
        context = {
            'data':data,
            'activefor':'ud_tables',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Category'
        }
        return render(request, 'controlPanel/add_tables/update_table.html',context) 

#@login_required(login_url="login")     
def deleteTableView(request):
        
    if request.method == "POST":
        Booked_table = BookTheTable.objects.filter(table_id__id = request.POST.get('baseId') )
        if Booked_table.exists():
            msg = {
                'response': 'notdeleted', 
                'msg': 'This Table related with Book The Tables Please check.'
            }   
            return JsonResponse(msg, safe=False)  
        Data = AllTables.objects.filter(id=request.POST.get('baseId')).update(is_deleted=True)
        if Data:
            msg = {
                'response': 'success', 
                'msg': 'Your Data Has Been Successfully Deleted.'
            }
        else:
            msg = {
                'response': 'notdeleted',
                'msg': 'Your Data Has Not Been Deleted.'
            }
        return JsonResponse(msg, safe=False)  
    

############## Table Booking From Admin Side ##################

#@login_required(login_url="login")     
def BookedTablesListView(request):

    data = BookTheTable.objects.all().values(
        "id","table_id__table_name","name","phone_number","email_address","total_members","date","timings","created_at"
    ).order_by('-id').filter(is_deleted = False)
    contecx = {
        'activefor':'ud_bookedtables',
        'page_title':'Booked Tables',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':data
    }
    return render(request, 'controlPanel/book_tables/list_booked_table.html',contecx)


#@login_required(login_url="login") 
def BookTheNewTableView(request):

    if request.POST.get('name') :
        from datetime import time
        table_id = request.POST.get('table_name')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email_address = request.POST.get('email_address')
        total_members = request.POST.get('total_members')
        timings = request.POST.get('timings')
        date = request.POST.get('date')
        tables_data = AllTables.objects.filter(id=table_id,is_deleted=False).first()
        table_seats = tables_data.no_of_seats
        from_time = tables_data.from_time
        to_time = tables_data.to_time
        hours, minutes = map(int, timings.split(':'))
        booking_time = time(hours, minutes)
        if not (from_time <= booking_time <= to_time):
            return JsonResponse(
                {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': "Your booking for the table is unavailable at this time. Please check again."
                }, 
                safe=False
            )

        if (int(table_seats) < int(total_members)):
            return JsonResponse(
                {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': "Your selected number exceeds the seating capacity. Please check."
                }, 
                safe=False
            )
        _created = BookTheTable.objects.create(
            table_id_id=tables_data.id,
            name=name, 
            phone_number = phone_number, 
            email_address = email_address, 
            total_members = total_members,
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
                Mesg.send_email(data)
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
                ################ Send Email & Whatsapp message to the Admin ################
                admin_data = AdminProfile.objects.first()
                if admin_data:
                    body2=f'Hello Admin,\n\nThis is to inform you that {name} has successfully booked a table. Please find the details below:\n\nPhone Number : {phone_number}\nEmail : {email_address}\nTotal Members : {total_members}\nDate : {formatted_date}\nTimings : {converted_time} \n\nThanks & Regards,\nRestaurent POC'  
                    data={
                        'subject':'Table Booked',
                        'body':body2,
                        'to_email':admin_data.email_address
                    }
                    print("Sendinig the mail")
                    Mesg.send_email(data)
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
            msg = {
                'response': 'success', 
                'title':'Data Saved!', 
                'icon':'success',  
                'msg': 'Your data has been successfully saved.'
            }
        else:
            msg = {
                'response': 'notSaved', 
                'title':'Not Saved!', 
                'icon':'error', 
                'msg': 'Your data has not been saved. Please try again.'
            }
        return JsonResponse(
            msg, safe=False
        )
    else:
        data = AllTables.objects.filter(status__in=["Available"],is_deleted=False).order_by("-id")
        context = {
            'activefor':'ud_bookedtables',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Book Tables',
            'data':data
        }
        return render(request, 'controlPanel/book_tables/book_new_table.html',context)


#@login_required(login_url="login") 
def UpdateTheBookedTable(request, baseId):

    if baseId and request.method == 'POST':
        table_id = request.POST.get('table_name')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        email_address = request.POST.get('email_address')
        total_members = request.POST.get('total_members')
        timings = request.POST.get('timings')
        date = request.POST.get('date')

        # Check the Grace Period to Update The Table  
        # Current Updating time
        current_datetime = timezone_now().time()
        updating_time = current_datetime.strftime("%H:%M")
        up_hours,up_minutes = map(int, updating_time.split(':'))
        updating_time = hrs_to_mins(up_hours,up_minutes)
        # Table Booked time 
        obj = BookTheTable.objects.get(id=baseId)
        order_time = obj.created_at.time()
        order_time = order_time.strftime("%H:%M")
        or_hours, or_minutes = map(int, order_time.split(':'))
        order_time = hrs_to_mins(or_hours, or_minutes)
        # Time Defference 
        time_difference = updating_time - order_time
        if time_difference > 5:
            return JsonResponse(
                {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': "Your grace period for updating the booking details has expired."
                }, 
                safe=False
            )
        # Verify the table capacity against the total number of members.
        tables_data = AllTables.objects.filter(id=table_id,is_deleted=False).first()
        table_seats = tables_data.no_of_seats
        if (int(table_seats) < int(total_members)):
            return JsonResponse(
                {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': "Your selected number exceeds the seating capacity. Please check."
                }, 
                safe=False
            )

        created = BookTheTable.objects.filter(id=baseId).update(
            table_id_id=tables_data.id,
            name=name, 
            phone_number=phone_number, 
            email_address=email_address,
            total_members=total_members, 
            timings=timings,
            date=date
        )
        if created:
            msg = {
                'response': 'success', 
                'title':'Data Saved!', 
                'icon':'success',  
                'msg': 'Your data has been successfully saved.'
            }
        else:
            msg = {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': 'Your data has not been saved. Please try again.'
            }
        return JsonResponse(
            msg, safe=False
        )
    else:
        data = BookTheTable.objects.filter(id=baseId, is_deleted = False).first()
        context = {
            'data':data,
            'activefor':'ud_bookedtables',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Update Table'
        }
        return render(request, 'controlPanel/book_tables/update_booked_table.html',context) 
    


############### Admin Profile ################

#@login_required(login_url="login")
def GetAdminProfile(request):

    admin_details = AdminProfile.objects.filter().values().first()
    contecx = {
        'activefor':'ud_admindeatils',
        'page_title':'Admin Profile',
        'MEDIA_URL':settings.MEDIA_URL,
        'listings':admin_details
    }
    return render(request, 'controlPanel/admin_details/admin_profile.html',contecx)

#@login_required(login_url="login")
def UpdateAdminProfile(request, baseId):
    
    if baseId and request.method == "POST":
        full_name = request.POST.get("full_name")
        email_address = request.POST.get("email_address")
        phone_number = request.POST.get("phone_number")
        photo = request.POST.get("photo")

        obj = AdminProfile.objects.filter(id=baseId).update(
            full_name = full_name,
            email_address = email_address,
            phone_number = phone_number,
            photo = photo,
        )
        if obj:
            msg = {
                'response': 'success', 
                'title':'Data Saved!', 
                'icon':'success',  
                'msg': 'Your data has been successfully saved.'
            }
        else:
            msg = {
                'response': 'notSaved', 
                'title':'Warning!', 
                'icon':'error', 
                'msg': 'Your data has not been saved. Please try again.'
            }
        
        return JsonResponse(
            msg, safe=False
        )
    
    else:
        admin_details = AdminProfile.objects.filter().values().first()
        context = {
            'data':admin_details,
            'activefor':'ud_admindeatils',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Admin Profile'
        }
        return render(request, 'controlPanel/admin_details/admin_profile.html',context) 
    

############################## New Function To Update The Admin ###############################
    
def updateAdmin(request, baseId):
    
    if baseId and request.method == 'POST':
        
        updateData = AdminProfile.objects.get(id=baseId)
        allData = request.POST
        allFiles = request.FILES
                                
        savedData = AdminProfileForm(data=allData, files=allFiles, instance=updateData)

        if savedData.is_valid():
            savedData.save()
            data = savedData.instance
            msg = {'response': 'success', 'title':'Data Saved!', 'icon':'success',  'msg': 'Your data has been successfully saved.'}
        else:
            msg = {'response': 'notSaved', 'title':'Not Saved!', 'icon':'error', 'msg': 'Your data has not been saved. Please try again.'}
        
        return JsonResponse(msg, safe=False)
    else:
        ud      = AdminProfile.objects.filter(id=baseId, is_deleted = False).first()
        udData = {
            'data':ud,
            'activefor':'ud_profile',
            'MEDIA_URL':settings.MEDIA_URL,
            'page_title':'Admin Page'
        }
        return render(request, 'controlPanel/admin_details/update-admin.html',udData)