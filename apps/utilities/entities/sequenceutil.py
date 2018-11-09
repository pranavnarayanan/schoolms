from django.db import models

class EN_SequenceUtil(models.Model):
    code  = models.CharField(max_length=25, unique=True, null=False)
    value = models.IntegerField(default=1,unique=False)

    class Meta:
        db_table = "en_sequence_util"

    @staticmethod
    def next(_code, _value=1):
        if not EN_SequenceUtil.objects.filter(code=_code).exists():
            obj = EN_SequenceUtil()
            obj.code = _code
            obj.value = _value
            obj.save()
            return _value
        else:
            obj = EN_SequenceUtil.objects.get(code=_code)
            obj.value = (obj.value + 1)
            obj.save()
            return obj.value

    @staticmethod
    def genProductIdForUser():
        return "MY"+format(EN_SequenceUtil.next("user_product_id", 10001000))

    @staticmethod
    def genProductIdForOrganization():
        return "MYOR"+format(EN_SequenceUtil.next("org_product_id", 100100))

    @staticmethod
    def genProductIdForOrganizationGroup():
        return "MYGP"+format(EN_SequenceUtil.next("org_grp_product_id", 100100))

    @staticmethod
    def genTokenForNewUserRegistration():
        return "TOKEN"+format(EN_SequenceUtil.next("user_reg_token", 1))
