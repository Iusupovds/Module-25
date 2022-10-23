from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def driver():
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_petfriends25(driver):

    driver.get('https://petfriends.skillfactory.ru/')
    driver.implicitly_wait(10)

    btn_newuser = driver.find_element('xpath', "//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    btn_exist_acc = driver.find_element('xpath', "/html/body/div/div/form/div[4]/a")
    btn_exist_acc.click()

    field_email = driver.find_element('id', "email")
    field_email.clear()
    field_email.send_keys('random12345@mail.ru')

    field_pass = driver.find_element('id', "pass")
    field_pass.clear()
    field_pass.send_keys('random12345')

    btn_submit = driver.find_element('xpath', "//button[@type='submit']")
    btn_submit.click()
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', '//*[@id="navbarNav"]/ul/li[1]/a')))
    btn_mypets = driver.find_element('xpath', "//*[@id='navbarNav']/ul/li[1]/a")
    btn_mypets.click()

    pet_cards = driver.find_elements('tag name', 'tr')
    my_pets_data = driver.find_element('class name', '\.col-sm-4.left')
    pets_string_1 = my_pets_data.text.split(" ")
    pets_string_2 = pets_string_1[1]
    pets_string_3 = pets_string_2.split("\n")
    pets_counter = int(pets_string_3[0])

    assert len(pet_cards) - 1 == pets_counter

    pet_photos = driver.find_elements('xpath', '//*[@id="all_my_pets"]/table/tbody/tr/th/img')

    assert len(pet_photos) >= pets_counter / 2

    pet_names = driver.find_elements('xpath', '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')
    pet_breeds = driver.find_elements('xpath', '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')
    pet_ages = driver.find_elements('xpath', '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')

    for i in range(len(pet_names)):
        assert pet_names[i].text != ''

    for i in range(len(pet_breeds)):
        assert pet_breeds[i].text != ''

    for i in range(len(pet_ages)):
        assert pet_ages[i].text != ''

    assert pets_counter == len(pet_names) and pets_counter == len(pet_breeds) and pets_counter == len(pet_ages)

    assert len(set(pet_names)) == len(pet_names)

    # Для сложной задачи я слишком тупой
    # python -m pytest -v --driver Chrome --driver-path C:\chromedriver.exe tests\test_selenium_petfriends.py
