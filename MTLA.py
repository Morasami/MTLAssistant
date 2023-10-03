import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
from concurrent.futures import ThreadPoolExecutor

#logging
logging.basicConfig(filename='translation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

#input Selectors
selectors = {
    'google_translate_input_field': '.er8xn',
    'reverso_input_field': '.no-border',
    'papago_input_field': '#txtSource',
    'yandex_input_field': '#fakeArea',
    'bing_input_field': '#tta_input_ta',
}

#results Selectors
translation_selector = {
    'Google Translate': '.usGWQd',
    'Reverso': '.translation-input__result',
    'Papago': '#targetEditArea',
    'Yandex': '#translation',
    'Bing': '#tta_output_ta',
}

#MTL services
services = {
    'Google Translate': {
        'url': 'https://translate.google.com/',
        'input_selector': selectors['google_translate_input_field'],
    },
    'Reverso': {
        'url': 'https://www.reverso.net/text-translation#sl=kor&tl=eng',
        'input_selector': selectors['reverso_input_field'],
    },
    'Papago': {
        'url': 'https://papago.naver.com/?sk=auto&tk=en',
        'input_selector': selectors['papago_input_field'],
    },
    'Yandex': {
        'url': 'https://translate.yandex.com/?source_lang=ko&target_lang=en',
        'input_selector': selectors['yandex_input_field'],
    },
    'Bing': {
        'url': 'https://www.bing.com/translator',
        'input_selector': selectors['bing_input_field']
    },
}

#text file that will store translations from this session
file_name = input("Enter the name of the text file: ")
file_name += '.txt'

#Storing Translations
translations = {}

#start Browsers
def initialize_browser(service_name, headless_mode=True):
    try:
        options = webdriver.ChromeOptions()
        if headless_mode:
            options.add_argument('-headless')
        browser = webdriver.Chrome(options=options)
        browser.get(services[service_name]['url'])
        return browser
    except Exception as e:
        logging.error(f"Failed to initialize {service_name} browser: {e}")
        print(f"Failed to initialize {service_name} browser: {e}")
        return None

#type -headless in console to start browsers in headless mode
headless_mode = '-headless' in sys.argv

for service_name in services:
    services[service_name]['browser'] = initialize_browser(service_name, headless_mode)

#switch bing to english
language_dropdown = services['Bing']['browser'].find_element(By.CSS_SELECTOR, '#tta_tgtsl')
language_dropdown.click()

english_option = services['Bing']['browser'].find_element(By.XPATH, '//*[@id="t_tgtAllLang"]/option[24]')
english_option.click()

time.sleep(1)

#input the text to MTLs
def translate_text(service_name, user_input):
    try:

        input_field = services[service_name]['browser'].find_element(By.CSS_SELECTOR,
                                                                     services[service_name]['input_selector'])
        input_field.clear()
        input_field.send_keys(user_input)

        #waiting for translation to complete
        time.sleep(10)

        #extracting the results
        if service_name == 'Bing':
            translation = services['Bing']['browser'].find_element(By.CSS_SELECTOR, translation_selector['Bing']).get_attribute("value")
        else:
         translation = services[service_name]['browser'].find_element(By.CSS_SELECTOR,
                                                                     translation_selector[service_name]).text

        #removing 'Look up details' from GT
        if service_name == 'Google Translate' and 'Look up details' in translation:
            translation = translation.replace('Look up details', '').strip()

        #store the translation in the dictionary
        translations[service_name] = translation

        #print the translation on console
        print(f"{service_name} Translation:")
        print(translation)
        print()
    except Exception as e:
        logging.error(f"Failed to translate text using {service_name}: {e}")

#main loop
while True:
    #User Input
    user_input = input("Enter the text you want to translate (or type 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break

    #input all at the same time
    with ThreadPoolExecutor(max_workers=len(services)) as executor:
        executor.map(lambda service_name: translate_text(service_name, user_input), services.keys())

    #storing TLs in txt file
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f"Original Text: {user_input}\n")
        for service_name, translation in translations.items():
            file.write("\n")
            file.write(f"{service_name} translation:\n")
            file.write(f"{translation}\n")
            file.write("\n")
        file.write("-" * 100 + "\n")

#close
for service_name, service_info in services.items():
    if service_info['browser'] is not None:
        service_info['browser'].quit()
