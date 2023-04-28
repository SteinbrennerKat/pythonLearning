from linkedin_api import Linkedin
from os import environ

api = Linkedin(environ.get('LINKEDIN_USR'), environ.get('LINKEDIN_PWD'))
searchResult = api.search_people('Mark Zilber')
print(searchResult)


