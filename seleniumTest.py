"""
    Script to search through Gateway website, log path, and manipulate every
    setting. Pages are generally seen as either something to navigate or
    something to manipulate settings.
"""
import time
from functools import wraps
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        print(func.__name__ + ' was called.')
        return func(*args, **kwargs)
    return with_logging
    
def init_driver():
    ''' Create driver object for Selenium bindings. '''
    driver = webdriver.Firefox() # dealing with chromedriver can be annoying
    driver.implicitly_wait(5) # ensure AJAX items have loaded
    return driver

def login(driver):
    ''' Go to website and log in. '''
    driver.get('http://10.0.222.26:8080/Account/Login')
    assert 'Horizon Retail Solutions' in driver.title
    elem = driver.find_element_by_name('Username')
    elem.send_keys('Admin')
    elem = driver.find_element_by_name('Password')
    elem.send_keys('Gateway')
    elem.send_keys(Keys.RETURN)
    assert 'No results found.' not in driver.page_source

@logit
def navigate(driver):
    ''' Drill down through menu items. When out of menu buttons, call function
        to manipulate settings. Within settings there may be more main menu
        type buttons ==> call navigate again.
    '''
    buttons = driver.find_elements_by_css_selector(
        'a.btn.btn-primary.btn-lg.btn-block')
    for button in buttons:
        print(get_heading(driver))
        print('--> pressed "{0}"' .format(button.text))
        button.click()
        navigate(driver)
    else:
        manipulate(driver)
        navigate(driver)

@logit
def manipulate(driver):
    ''' Analyze page and manipulate settings accordingly. '''
    # determine page and call appropriate function (make smart)
    print(get_heading(driver))
    rows = get_rows(driver)
    buttons = determ_avail_btns(rows[0])

    # check div tag prior to main table to determine what all to do on page
    set_heading = determ_set_heading(driver) # not developed yet
    
    # logic to manipulate buttons
    # (? might wrap with try/except decorator instead of checking first ?)
    if 'Add to Store' in buttons:
        pass
    elif 'Edit Company Defaults' in buttons:
        pass
    elif 'Edit Company Defaults' in buttons:
        pass
        
    nav_dropdown(driver)

@logit
def nav_dropdown(driver):
    ''' Drill down through dropdown menu. '''
    select = Select(driver.find_element_by_id('SelectedCategoryID'))
    dropdown_list = select.options
    for option in dropdown_list[1:]:
        print(option.text)
        option.click()
        submit = driver.find_element_by_xpath(
            '//input[contains(@value,"Filter")]')
        submit.click()
        nav_settings(driver)

@logit
def nav_settings(driver):
    ''' (same as manip_settings but is inside nav_dropdown) '''
    pass

@logit
def manip_settings(driver):
    ''' Iterate through rows and manipulate each setting. '''
    table = driver.find_elements_by_xpath('//table[@class="table"]/tbody/tr')
    for i, row in enumerate(table[1:]):
        cols = table.find_elements_by_css_selector('td')
        print(cols[0])
        print(cols[1])
        print(cols[2])
        
def get_heading(driver):
    ''' Find and print heading of page just inside <div class=panel-heading>.
        (this may be h1-h4 tags, but usually h2) Return: string
    '''
    heading = driver.find_element_by_xpath('//div[@class="panel-heading"]/*')
    return(heading.text)

def get_rows(driver):
    ''' Search for table, get all rows except for first one, return list. '''
    table_rows = driver.find_elements_by_css_selector('tr')[2]
    '''
        
    '''
    '''  ### possibility ###
    list_of_lists = [[td.text
                  for td in tr.find_elements_by_css_selector('td')]
                  for tr in driver.find_elements_by_css_selector('tr')]
    list_of_dicts = [
        dict(zip(list_of_lists[0],row)) for row in list_of_lists[1:]]
    '''
    '''  ### possibility ###
    for row in table_rows[1:]:
        if not row.find_element_by_css_selector('td').text:
            break # because it is an empty table
        cols = row.find_elements_by_css_selector('td')
        property_id = cols[0].text
        co_default = cols[1].text
    '''
    
def determ_avail_btns(driver):
    ''' Get a row, check to see what buttons it contains,
        and return a list of button names. '''
    body = driver.find_element_by_class_name('panel-body')
    table = body.find_elements_by_css_selector('tr')
    row = table[1].find_elements_by_css_selector(
        'a.btn.btn-primary')
    return [link for link in row.text]


class RowSetting: # not sure if I should be doing this.
    ''' Creates an object out of a row on a settings page.
        Takes a name, default value, (possible other values), and
        a list of buttons.

        If I do this, I think I will need to inherit from driver
        so that I can target later settings. Very lost.
    '''
    def __init__(self, name, def_value, buttons):
        self.name = name
        self.def_value = def_value
        self.buttons = buttons # list of buttons available

    # def function that will click on its buttons,
    #   manipulate the setting inside,
    #   and return True?
       
    

if __name__ == '__main__':
    driver = init_driver()
    login(driver)
    navigate(driver)
    time.sleep(5)
    #driver.quit() # All Done!
    print('Success')