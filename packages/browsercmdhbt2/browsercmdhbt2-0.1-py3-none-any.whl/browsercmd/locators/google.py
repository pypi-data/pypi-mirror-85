from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    LANG_CHOOSE_BUTTON=(By.XPATH,"//div[@id=\"lang-chooser\"]")
    LANG_IT = (By.XPATH, "//*[@id=\"lang-chooser\"]/div[2]/div[@data-value=\"it\"]")
    LANG_EN = (By.XPATH, "//*[@id=\"lang-chooser\"]/div[2]/div[@data-value=\"en\"]")
    EMAIL_LOGIN = (By.ID,"identifierId")
    PASS_WORD_LOGIN = (By.NAME,"password")
    RECO_EMAIL_BUTTON = (By.XPATH, "//form//div[contains(text(),\"Confirm your recovery email\")]")
    EMAIL_RECO = (By.ID,"knowledge-preregistered-email-response")
    EMAIL_RECO2 = (By.ID, "identifierId")
    PROFILE_INDENTIFIER=(By.XPATH,"//div[@id=\"profileIdentifier\" and contains(@data-email,\"@\")]")
    DONE_BUTTON = (By.XPATH,"//div[@role=\"button\" and contains(text(),\"Done\")]")
    CONFIRM_BUTTON = (By.XPATH, "//div[@role=\"button\" and contains(text(),\"Done\")]")

class AboutMeLocators(object):
    FIRST_NAME = (By.XPATH,"//input[@aria-label=\"First\"]")
    LAST_NAME = (By.XPATH, "//input[@aria-label=\"Last\"]")
    SUR_NAME = (By.XPATH, "//input[@aria-label=\"Surname\"]")
    FULL_NAME = (By.XPATH, "//input[@aria-label=\"Name\"]")

    FIRST_NAME_ROLE = (By.XPATH, "(//*[@role=\"dialog\"]//input)[1]")
    LAST_NAME_ROLE = (By.XPATH, "(//*[@role=\"dialog\"]//input)[2]")

    OK_BUTTON = (By.XPATH,"(//*[@role=\"dialog\"]//div[@role=\"button\"])[4]")
    CONFIRM_BUTTON = (By.XPATH,"(//*[@role=\"dialog\"]//div[@role=\"button\"])[4]")