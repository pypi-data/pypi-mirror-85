from . import BasePageElement
from browsercmd.locators.youtube import *


class UploadElement(BasePageElement):
    locator=UploadPageLocators.INPUT
    is_find_hide=True
class TitleUploadElement(BasePageElement):
    locator=UploadPageLocators.TITLE
    is_clear_text = True
    is_actionchane = False
    is_click = True
class DescriptionUploadElement(BasePageElement):
    locator = UploadPageLocators.DESCRIPTION
    is_clear_text = True
    is_actionchane = False
    is_click = True
class TagUploadElement(BasePageElement):
    locator = UploadPageLocators.TAG
class ThumbnailUploadElement(BasePageElement):
    locator = UploadPageLocators.CUSTOM_THUMB
    is_find_hide = True
class VideoLinkUploadElement(BasePageElement):
    locator = UploadPageLocators.VIDEO_LINK
