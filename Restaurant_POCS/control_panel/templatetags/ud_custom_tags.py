from django import template
from control_panel.models import cms, gallery, all_settings

register = template.Library()

@register.simple_tag
def my_function(value, secondValue):
  if value is None:
    value = 0
 
  # Perform logic using value
  aboutus = cms.objects.all().values().filter(id=1).first()
  result = (value*4)
  result2 = (value*5)
  context = {
    'firstValue' : result,
    'secondValue':result2,
    'aboutUsUd':aboutus
  }
  return context