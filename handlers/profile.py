import webapp2
import jinja2
from google.appengine.ext import db
from google.appengine.api import users
from monsterrules.common import Monster, Profile
import handlers.base
import configuration.site

class ProfileHandler(handlers.base.LoggedInRequestHandler):
  """Renders a profile page
  
  Given the ID of a profile to view, query for that profile and display it
  using the standard monster template. If not profile provided, show the 
  current user.
  
  Templates used: profile.html"""
  
  def get(self, profile_id=None):
    """HTML GET handler.
    
    Check the query parameters for the ID of the profile to be displayed.
    If found, display the user. Otherwise display current user"""
    
    template_values = self.build_template_values()
    
    if profile_id:
      template_values['viewed_profile'] = Profile.get_by_id(int(profile_id))
      template_values['monsters'] = Monster.all().filter("creator = ",template_values['viewed_profile']).order('-creation_time').fetch(10)
    elif template_values[handlers.base.USER_KEY]:
      template_values['viewed_profile'] = template_values[handlers.base.PROFILE_KEY]
      template_values['monsters'] = Monster.all().filter("creator = ",template_values[handlers.base.PROFILE_KEY]).order('-creation_time').fetch(10)
    template = configuration.site.jinja_environment.get_template('profile.html')
    return self.response.write(template.render(template_values))
      
      
