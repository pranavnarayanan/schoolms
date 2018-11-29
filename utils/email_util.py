from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Email:

    def sendEmail(self):
        subject = 'Email Subject'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['aravindrpillai1992@gmail.com']

        template = 'email_templates/myshishya_welcome.html'
        template_data = {
           'name': "Aravind R Pillai",
           'product_id': "MY0010234543"
        }
        message = render_to_string(template, template_data)
        msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)
        msg.attach_file("C:/Users/aravi/Downloads/ITR1_Viwer.pdf")
        msg.attach_alternative(message, "text/html")
        msg.send()