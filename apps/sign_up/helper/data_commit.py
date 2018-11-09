import datetime
from apps.users.models import EN_AddressBook
from apps.users.models import EN_Contacts
from apps.login.models import EN_LoginCredentials
from apps.users.models import EN_Users
from apps.users.models import TL_AccountStatus
from apps.utilities.models import EN_SequenceUtil

class SaveRecord():

    def save(self, user_reg_instance):

        # Contact Details
        enContact = EN_Contacts()
        enContact.mobile_country_code = user_reg_instance.mobile_country_code
        enContact.mobile_number = user_reg_instance.mobile_number
        enContact.secondary_number = user_reg_instance.secondary_number
        enContact.is_landline_number = user_reg_instance.is_landline_number
        enContact.email_id = user_reg_instance.email_id
        enContact.website = user_reg_instance.website
        enContact.publish_your_site = user_reg_instance.publish_your_site
        enContact.save()

        # User Basic Details
        enUser = EN_Users()
        enUser.product_id = EN_SequenceUtil.genProductIdForUser()
        enUser.name = user_reg_instance.name
        enUser.date_of_birth = user_reg_instance.date_of_birth
        enUser.gender = user_reg_instance.gender
        enUser.display_picture = None
        enUser.account_status = TL_AccountStatus.objects.get(code="inactive")
        enUser.contact = enContact
        enUser.newsletter_subscribe = user_reg_instance.subscribe_for_news_letter
        enUser.save()

        # Login Credential Details
        enCredentials = EN_LoginCredentials()
        enCredentials.username = user_reg_instance.username
        enCredentials.password = user_reg_instance.password
        enCredentials.last_logged_in_time = datetime.datetime.now()
        enCredentials.user = enUser
        enCredentials.save()

        # Permanent Address Details
        enPermanentAddress = EN_AddressBook()
        enPermanentAddress.house_name = user_reg_instance.permanent_house_name
        enPermanentAddress.street = user_reg_instance.permanent_street
        enPermanentAddress.landmark = user_reg_instance.permanent_landmark
        enPermanentAddress.zipcode = user_reg_instance.permanent_zipcode
        enPermanentAddress.is_current_address = user_reg_instance.is_current_address
        enPermanentAddress.is_permanent_address = True
        enPermanentAddress.user = enUser
        enPermanentAddress.save()

        # Current Address Details
        if not enPermanentAddress.is_current_address:
            enCurrentAddress = EN_AddressBook()
            enCurrentAddress.house_name = user_reg_instance.current_house_name
            enCurrentAddress.street = user_reg_instance.current_street
            enCurrentAddress.landmark = user_reg_instance.current_landmark
            enCurrentAddress.zipcode = user_reg_instance.current_zipcode
            enCurrentAddress.is_current_address = True
            enPermanentAddress.is_permanent_address = False
            enCurrentAddress.user = enUser
            enCurrentAddress.save()
