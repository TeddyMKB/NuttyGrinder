from selenium import webdriver
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import pytesseract
from selenium.webdriver.common.keys import Keys

url = 'http://nutty.thisislanguage.com/game/nutty_tilez'

uname = input('enter TIL username->')
pword = input('enter TIL password->')

driver = webdriver.Firefox()

driver.get(url)

driver.find_element_by_class_name("login_btn").click()

driver.find_element_by_name("email").send_keys(uname)
driver.find_element_by_name("password").send_keys(pword)
driver.find_element_by_id("submit").click()

driver.get('http://nutty.thisislanguage.com/game/nutty_tilez')

raw_words = []

for tile in range(1, 3):
    driver.find_element_by_css_selector('div[data-tile="' + str(tile) + '"]').click()
    time.sleep(1)
    trs = driver.find_elements_by_tag_name("tr")
    for tr in trs:
        raw_words.append(tr.text)

    driver.find_element_by_class_name("dialogue_close").click()


words = []

for word in raw_words:
    print(word.replace("\n", ":"))
    words.append(word.replace("\n", ":"))

for i in range(len(words)):
    words[i] = [words[i][0:words[i].find(":")], words[i][words[i].find(":") + 1: len(words[i])]]

print(words)

driver.find_element_by_class_name("selected_tile").click()
driver.find_element_by_class_name("play_btn").click()

while driver.find_element_by_class_name("text").value_of_css_property("display") == "none":
    print('waiting for start')

print("game start")
previous = ""
while True:
    time.sleep(.01)
    isBonus = False
    if driver.find_element_by_class_name("bonus_text").value_of_css_property("display") == "none":
        image = driver.execute_script('return document.getElementById("word_canvas").toDataURL("image/png");')
        isBonus = False
    else:
        image = driver.execute_script('return document.getElementById("bonus_canvas").toDataURL("image/png");')
        isBonus = True
    print(image)
    fig = plt.figure()
    plt.axis('off')
    plt.imshow(mpimg.imread(image))
    fig.savefig("1.png")
    plt.clf()
    plt.close(fig)
    text = pytesseract.image_to_string("1.png")
    final = ""
    print(text)
    if text.find("(") != -1:
        final = text[0:text.find("(")].rstrip()
    elif text.find("{") != -1:
        final = text[0:text.find("{")].rstrip()
    else:
        final = text.rstrip()

    print(final)

    result = ""
    if isBonus:
        result = final
    else:
        for word in words:
            if final in word:
                result = word[1]


    print(result)
    if not isBonus:
        driver.find_element_by_class_name("guess").send_keys(result)
        driver.find_element_by_class_name("guess").send_keys(Keys.ENTER)
    else:
        driver.find_element_by_class_name("bonus_guess").send_keys(result)
        driver.find_element_by_class_name("bonus_guess").send_keys(Keys.ENTER)


# end_level_up_btn
