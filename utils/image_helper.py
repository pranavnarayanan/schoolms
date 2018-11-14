from properties.image_properties import ImageType, ImageConstants

class ImageHelper:

    def __init__(self, type):
        self.type = type

    def getFullPath(self, imageName=None):
        if imageName == None:
            if self.type == ImageType.ORGANIZATION_GROUP:
                return ImageConstants.PATH+"def_org_group.png"
            elif self.type == ImageType.ORGANIZATION:
                return ImageConstants.PATH+"def_org.png"
            elif self.type == ImageType.USER:
                return ImageConstants.PATH+"def_user.png"
            else:
                return ImageConstants.PATH + imageName

