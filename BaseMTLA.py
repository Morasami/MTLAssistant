from selenium import webdriver
from selenium.webdriver.common.by import By
import time

#asking for txt file name
file_name = input("Enter the name of the text file (e.g., translations.txt): ")
file_name += '.txt'

#opening browsers&websites
google_translate_browser = webdriver.Firefox()
google_translate_browser.get('https://translate.google.com/')

reverso_browser = webdriver.Firefox()
reverso_browser.get('https://www.reverso.net/text-translation#sl=kor&tl=eng')

papago_browser = webdriver.Firefox()
papago_browser.get('https://papago.naver.com/?sk=auto&tk=en')

#main loop
while True:
    user_input = input("Enter the text you want to translate (or type 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break

    #input into services
    google_translate_input_field = google_translate_browser.find_element(By.CLASS_NAME, 'er8xn')
    google_translate_input_field.clear()
    google_translate_input_field.send_keys(user_input)

    reverso_input_field = reverso_browser.find_element(By.CSS_SELECTOR, '.no-border')
    reverso_input_field.clear()
    reverso_input_field.send_keys(user_input)

    papago_input_field = papago_browser.find_element(By.ID, 'txtSource')
    papago_input_field.clear()
    papago_input_field.send_keys(user_input)

    #delay for translations
    time.sleep(10)

    reverso_translation = reverso_browser.find_element(By.CSS_SELECTOR, '.translation-input__result').text

    google_translate_translation = google_translate_browser.find_element(By.CSS_SELECTOR,'.usGWQd').text
    #removing extra words from GT
    google_translate_translation = google_translate_translation.replace('Look up details', '').strip()

    papago_translation = papago_browser.find_element(By.CSS_SELECTOR,'#targetEditArea').text
                                                     
    #print in console
    print("Google Translate Translation:")
    print(google_translate_translation)
    print("\nReverso Translation:")
    print(reverso_translation)
    print("\nPapago Translation:")
    print(papago_translation)

    #saving this session translations in txt file
    with open(file_name, 'a', encoding='utf-8') as file:
        file.write(f"Original Text: {user_input}\n")
        file.write("\n")  # Add a space
        file.write(f"Google Translate Translation: {google_translate_translation}\n")
        file.write("\n")  # Add a space
        file.write(f"Reverso Translation: {reverso_translation}\n")
        file.write("\n")  # Add a space
        file.write(f"Papago Translation: {papago_translation}\n\n")
        file.write("-" * 100 + "\n")  # Add a line of dashes
#close
google_translate_browser.quit()
reverso_browser.quit()
papago_browser.quit()
