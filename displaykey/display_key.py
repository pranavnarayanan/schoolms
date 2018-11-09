from displaykey.english import English_DK

class DisplayKey():

    @staticmethod
    def get(key):
        return English_DK.lang.get(key)