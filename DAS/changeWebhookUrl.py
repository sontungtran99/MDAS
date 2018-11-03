import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,\
StaleElementReferenceException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains


LINK_HOME = 'https://connect.speedsms.vn/#/home'
LINK_WEBHOOK_SETTINGS = 'https://connect.speedsms.vn/#/settings/webhook'

XPATH_EMAIL_INPUT_BOX = '//div[@class="modal-body"]//input[@type="email"]'
XPATH_PASSWORD_INPUT_BOX = '//div[@class="modal-body"]//input[@type="password"]'
XPATH_LOGIN_BUTTON = '//button[@class="btn btn-primary btn-block btn-flat pull-right clearfix ng-binding"]'
XPATH_EDIT_HOOK_BUTTON = '//a[@ng-click="editHook(item)"]'
XPATH_ACTION_BOX = '//input[@placeholder="Your url to handle message"]'
XPATH_DONE_EDITING_BUTTON = '//button[text()="Ok"]'
XPATH_EVENT_LIST = '//div[@class="input-group-btn"]/button'
XPATH_INCOMING_SMS_CHOICE = '//ul[@class="dropdown-menu"]//a[text()="Incoming SMS"]'
XPATH_ADD_NEW_BUTTON = '//button[@ng-click="addNewHook()"]'
XPATH_DELETE_INCOMING_SMS_BUTTON = '//td[text()="Incoming sms"]/parent::tr//a[@ng-click="removeHook(item)"]'
XPATH_CONFIRM_DELETE = '//div[@class="sa-confirm-button-container"]/button'
XPATH_SECRET_BOX = '//input[@name="secret"]'

EMAIL = 'XXX@gmail.com'
PASSWORD = 'XXX'
SECRET = 'XXX'


def changeWebhookUrl(url):
    ''' Login and change credentials '''
    # Start Selenium
    driver = webdriver.Firefox()
    action = ActionChains(driver)

    # Login
    get_link_safe(LINK_HOME)
    write_input(XPATH_EMAIL_INPUT_BOX, EMAIL)
    write_input(XPATH_PASSWORD_INPUT_BOX, PASSWORD)

    # Change webhook url
    time.sleep(1)
    get_link_safe(LINK_WEBHOOK_SETTINGS)
    #editWebhookUrlDirectly(url)
    editWebhookUrlIndirectly(url)
    driver.close()


def editWebhookUrlIndirectly(url):
    # Delete previous webhook
    click_safe(find_element_safe(XPATH_DELETE_INCOMING_SMS_BUTTON))
    time.sleep(1)
    click_safe(find_element_safe(XPATH_CONFIRM_DELETE))
    time.sleep(1)
    click_safe(find_element_safe(XPATH_CONFIRM_DELETE))
    time.sleep(1)

    # Add new hook
    click_safe(find_element_safe(XPATH_ADD_NEW_BUTTON))
    time.sleep(1)
    click_safe(find_element_safe(XPATH_EVENT_LIST))
    time.sleep(1)
    click_safe(find_element_safe(XPATH_INCOMING_SMS_CHOICE))
    time.sleep(1)
    send_keys_safe(find_element_safe(XPATH_SECRET_BOX), SECRET)
    write_input(XPATH_ACTION_BOX, url)
    time.sleep(1)

def editWebhookUrlDirectly(url):
    # Just use the edit function of the web
    click_safe(find_element_safe(XPATH_EDIT_HOOK_BUTTON))
    input()
    click_safe(find_element_safe(XPATH_EVENT_LIST))
    input()
    click_safe(find_element_safe(XPATH_INCOMING_SMS_CHOICE))
    input()
    clear_safe(find_element_safe(XPATH_ACTION_BOX))
    input()
    write_input(XPATH_ACTION_BOX, url)
    input()

def get_link_safe(link):
    while True:
        try:
            driver.get(link)
        except BrokenPipeError:
            pass
        except Exception as e:
            print(e)
        else:
            break
        time.sleep(1)

def find_element_safe(xpath):
    while True:
        try:
            elem = driver.find_element(By.XPATH, xpath)
        except BrokenPipeError:
            continue
        except Exception as e:
            print(e)
        else:
            break
    return elem

def send_keys_safe(elem, keys):
    while True:
        try:
            elem.send_keys(keys)
        except BrokenPipeError:
            pass
        except Exception as e:
            print(e)
        else:
            break
        time.sleep(1)

def click_safe(elem):
    while True:
        try:
            elem.click()
        except BrokenPipeError:
            pass
        except Exception as e:
            print(e)
        else:
            break
        time.sleep(1)

def write_input(xpath, text):
    elem = find_element_safe(xpath)
    send_keys_safe(elem, text)
    send_keys_safe(elem, Keys.ENTER)

def clear_safe(elem):
    while True:
        try:
            elem.clear()
        except BrokenPipeError:
            pass
        except Exception as e:
            print(e)
        else:
            break
        time.sleep(1)

