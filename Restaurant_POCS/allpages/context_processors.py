# yourapp/context_processors.py
from control_panel.models import cms,all_settings,testimonial,category ,AllTables, AddToCartItems, OrderDetails# Importing model Users and etc...
from allpages.models import CustomUser
from django.conf import settings
from django.contrib.auth.models import AnonymousUser 

def get_common_data(request):
    
    user = request.user
    # print("User",user)
    # print("UserID",user.id)
    # Check if the user is authenticated
    if isinstance(user, AnonymousUser):
        cart_items = [] 
        order_history = []
    else:
        cart_items = AddToCartItems.objects.filter(user_id=user.id).order_by("-id")
        order_history = OrderDetails.objects.filter(user_id=user.id).order_by("-id")
        
    # Fetch all records from the database
    session_id = request.session.session_key
    aboutUs = cms.objects.filter(id = 1,status='1').first()
    allsettings = all_settings.objects.filter(id = 1).first()
    alltestimonial = testimonial.objects.all().values().order_by('display_order').filter(is_deleted = False,status='1')
    ordernow = cms.objects.filter(id = 5,status='1').first()
    gallerytext = cms.objects.filter(id = 6,status='1').first()
    special_offer = cms.objects.filter(id = 3,status='1').first()
    ourmenu = cms.objects.filter(id = 7,status='1').first()
    contactus = cms.objects.filter(id = 8,status='1').first()
    indexdetails = cms.objects.filter(id = 4,status='1').first()
    ourmenucategories = category.objects.order_by('display_order').filter(status=1,show_on_our_menu='1')
    Book_Table = AllTables.objects.filter(status__in=["Available"],is_deleted=False).order_by("-id")
    #aboutUs = cms.objects.filter(id = 1,status='1').first()
    # order_history = OrderDetails.objects.filter(user_id = 1)
    order_output = []
    set_ids = set()
    finaltotal=0
    for item in order_history:
        if item.id not in set_ids:
            subitem_list = [subitem.sub_item_title for subitem in item.subitem_id.all()]
            subitem_price = [subitem.price for subitem in item.subitem_id.all()]
            items_data = {
                "id": item.id,
                "item_id" : item.item_id.id,
                "item_name": item.item_id.item_name,
                "itemprice": item.item_id.price,
                "subitems": subitem_list,
                "subitems_price": subitem_price,   
                "quantity": item.quantity,
                "total_price": item.total_price,
                "special_instructions": item.special_instructions,
                "item_image":item.item_id.image,
                "created_at":item.created_at,
                'MEDIA_URL':settings.MEDIA_URL,

            }
            finaltotal+=int(item.total_price)
            order_output.append(items_data)
    
    # cart_items = AddToCartItems.objects.filter(user_id = 1)
    output = []
    seen_ids = set()
    grandtotal=0
    for item in cart_items:
        if item.id not in seen_ids:
            subitems_list = [subitem.sub_item_title for subitem in item.subitem_id.all()]
            subitems_price = [subitem.price for subitem in item.subitem_id.all()]
            item_data = {
                "id": item.id,
                "item_id" : item.item_id.id,
                "item_name": item.item_id.item_name,
                "itemprice": item.item_id.price,
                "subitems": subitems_list,
                "subitems_price": subitems_price,   
                "quantity": item.quantity,
                "total_price": item.total_price,
                "special_instructions": item.special_instructions,
                "item_image":item.item_id.image,
                'MEDIA_URL':settings.MEDIA_URL,

            }
            grandtotal+=item.total_price
            output.append(item_data)

    allData = {
        'commonAbout' : aboutUs,
        'commonSetting' : allsettings,
        'alltestimonial' : alltestimonial,
        'ordernow' : ordernow,
        'gallerytext' : gallerytext,
        'special_offer' : special_offer,
        'ourmenu' : ourmenu,
        'contactus' : contactus,
        'indexdetails' : indexdetails,
        'aboutUs' : aboutUs,
        'ourmenucategories' : ourmenucategories,
        'Book_Table' : Book_Table,
        "cart_items":output,
        "grandtotal":grandtotal,
        'MEDIA_URL':settings.MEDIA_URL,
        "order_history":order_output,
        "finaltotal" : finaltotal

    }

    return allData

