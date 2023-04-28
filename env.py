from os import environ

environ['ENV'] = 'dev'
environ['LINKEDIN_USR'] = 'abandoned1991@gmail.com'
environ['LINKEDIN_PWD'] = 'qb4nJh12je!>'
env_var = environ.get('ENV')
print(f"Linkedin MS currently working in {env_var} environment, User: {environ.get('LINKEDIN_USR')} and password is: {environ.get('LINKEDIN_PWD')}")
