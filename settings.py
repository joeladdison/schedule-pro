# Django Settings - used for templates
import os
from django.conf import settings 

TIME_ZONE = "UTC"

# Use blank app to set root application directory for Django
INSTALLED_APPS=('nothing')

# Set up template directory path
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
TEMPLATE_DIRS=(templates_path)

# Another method of setting template directory
#settings.TEMPLATE_LOADERS = (('mvctemplateloader.MvcTemplateLoader', 
#            templates_path), 'django.template.loaders.filesystem.Loader', 
#            'django.template.loaders.app_directories.Loader')