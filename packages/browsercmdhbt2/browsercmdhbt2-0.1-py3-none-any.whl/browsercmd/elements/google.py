from . import BasePageElement
from browsercmd.locators.google import *


class EmailLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_LOGIN
class PassWordLoginElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.PASS_WORD_LOGIN
class EmailRecoElement(BasePageElement):
    delay = 5
    locator=LoginPageLocators.EMAIL_RECO

class EmailRecoElement2(BasePageElement):
    delay = 5
    locator = LoginPageLocators.EMAIL_RECO2

