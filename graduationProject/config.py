# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

db_config = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'grad',
        'USER':'root',
        'PASSWORD':'sari12345',
        'HOST':'localhost',
        'PORT':'3306',
    }
}

allowed_hosts_config = ['*']