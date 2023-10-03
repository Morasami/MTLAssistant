# @title Main MTL Assistant { vertical-output: true, display-mode: "form" }
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from IPython.display import display, HTML
from selenium.webdriver.common.keys import Keys

selectors = {
    'google_translate_input_field': '.er8xn',
    'reverso_input_field': '.no-border',
    'papago_input_field': '#txtSource'
}

translation_selector = {
    'Google Translate': '#yDmH0d > c-wiz > div > div.ToWKne > c-wiz > div.OlSOob > c-wiz > div.ccvoYb.EjH7wc > div.AxqVh > div.OPPzxe > c-wiz.sciAJc',
    'Reverso': '.translation-input__result',
    'Papago': '#txtTarget'
}

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
    }
}

translations = {}

def initialize_browser(service_name):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        browser = webdriver.Chrome(options=options)
        browser.get(services[service_name]['url'])
        return browser
    except Exception as e:
        logging.error(f"Failed to initialize {service_name} browser: {e}")
        print(f"Failed to initialize {service_name} browser: {e}")
        return None

for service_name in services:
    services[service_name]['browser'] = initialize_browser(service_name)

def translate_text(service_name, user_input):
    try:
        browser = services[service_name]['browser']
        input_field = browser.find_element(By.CSS_SELECTOR, services[service_name]['input_selector'])

        input_field.clear()
        input_field.send_keys(user_input)

        time.sleep(10)

        translation = browser.find_element(By.CSS_SELECTOR, translation_selector[service_name]).text
        translations[service_name] = translation

        if service_name == 'Google Translate':
            translation = translation.replace('Look up details', '').strip()
            translation = translation.replace('Translation results', '').strip()
            translation = translation.replace('Translation result', '').strip()

        display(HTML(f"<h2>{service_name} Translation:</h2><p>{copied_text if service_name == 'DeepL' else translation}</p>"))

    except Exception as e:
        logging.error(f"Failed to translate text using {service_name}: {e}")





#main loop
while True:

    user_input = input("Enter the text you want to translate (or type 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break  # Exit the loop

    with ThreadPoolExecutor(max_workers=len(services)) as executor:
        executor.map(lambda service_name: translate_text(service_name, user_input), services.keys())

for service_name, service_info in services.items():
    if service_info['browser'] is not None:
        service_info['browser'].quit()
