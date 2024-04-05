# Set the email address to be used as the sender for outgoing emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = "tl.fahimeh@gmail.com"
# EMAIL_HOST_PASSWORD = 'fahimeh1234567'     # Your Gmail password or app-specific password
OTP_LENGTH = 6
OTP_EXPIRATION_TIME = 3  # min

EMAIL_HOST = 'smtp.mailersend.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
# jfrog-ignore
EMAIL_HOST_USER = ""
# jfrog-ignore
EMAIL_HOST_PASSWORD = ''
