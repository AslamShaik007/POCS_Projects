# yourapp/context_processors.py

def common_data_ud(request):
    # Your common logic here
    common_value = "This is a common value"

    # Return a dictionary with the data you want to make available to templates
    return {'common_value_ud': common_value, 'all_setting_ud':'This is all setting data from setting.'}