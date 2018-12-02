from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Email:

    def sendEmail(self, template, subject, template_data, recipient_list, attachments = None):
        email_from = settings.EMAIL_HOST_USER
        if recipient_list == None:
            raise Exception("No Recipient Found")
        template = 'email_templates/'+template
        message = render_to_string(template, template_data)
        msg = EmailMultiAlternatives(subject, message, email_from, recipient_list)

        if attachments != None:
            for attachment in attachments:
                msg.attach_file(attachment)

        msg.attach_alternative(message, "text/html")
        msg.send()