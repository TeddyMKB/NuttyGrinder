import selenium
from selenium import webdriver
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
import pytesseract
from selenium.webdriver.common.keys import Keys
import cv2 as cv


class NuttyGrinder:
    url = 'http://nutty.thisislanguage.com/game/nutty_tilez'

    def __init__(self, u, p):
        self.uname = u
        self.pword = p
        self.driver = webdriver.Firefox()
        self.driver.get(NuttyGrinder.url)
        self.driver.find_element_by_class_name("login_btn").click()
        self.driver.find_element_by_name("email").send_keys(self.uname)
        self.driver.find_element_by_name("password").send_keys(self.pword)
        self.driver.find_element_by_id("submit").click()
        self.driver.get('http://nutty.thisislanguage.com/game/nutty_tilez')

        self.raw_words = []
        self.words = []

        self.level = int(self.driver.find_element_by_class_name("selected_tile").get_attribute("data-tile"))

    def get_words(self):
        for tile in range(1, self.level+1):
            self.driver.execute_script("arguments[0].scrollIntoView()", self.driver.find_element_by_css_selector('div[data-tile="' + str(tile) + '"]'))
            self.driver.find_element_by_css_selector('div[data-tile="' + str(tile) + '"]').click()
            wordsets = self.driver.find_elements_by_tag_name("tr")
            for wordset in wordsets:
                self.raw_words.append(wordset.text)

            self.driver.find_element_by_class_name("dialogue_close").click()
            time.sleep(.1)

        for word in self.raw_words:
            print(word.replace("\n", ":"))
            self.words.append(word.replace("\n", ":"))

        for i in range(len(self.words)):
            self.words[i] = [self.words[i][0:self.words[i].find(":")], self.words[i][self.words[i].find(":") + 1:
                                                                                     len(self.words[i])]]

        print(self.words)

    def init_match(self):
        self.driver.find_element_by_class_name("selected_tile").click()
        self.driver.find_element_by_class_name("play_btn").click()

    def game_loop(self):
        while self.driver.find_element_by_class_name("text").value_of_css_property("display") == "none":
            print('waiting for start')

        print("game start")
        while True:
            if self.driver.find_element_by_class_name("game_over_sign").value_of_css_property("display") == "block":
                break
            time.sleep(.01)
            isBonus = False
            if self.driver.find_element_by_class_name("bonus_text").value_of_css_property("display") == "none":
                image = self.driver.execute_script('return document.getElementById("word_canvas").toDataURL("image/png");')
                isBonus = False
            else:
                image = self.driver.execute_script('return document.getElementById("bonus_canvas").toDataURL("image/png");')
                isBonus = True
            print(image)
            fig = plt.figure()
            plt.axis('off')
            plt.imshow(mpimg.imread(image))
            fig.savefig("1.png")

            plt.clf()
            plt.close(fig)
            if isBonus:
                text = pytesseract.image_to_string("1.png", lang="fra")
            else:
                text = pytesseract.image_to_string("1.png", lang="eng")
            final = ""
            print(text)
            if text.find("(") != -1:
                final = text[0:text.find("(")].rstrip()
            elif text.find("{") != -1:
                final = text[0:text.find("{")].rstrip()
            elif text.find("@") != -1:
                final = text[0:text.find("@")].rstrip()
            elif text == "e":
                final = "à"
            elif text == "la matiéere":
                final = "la matière"
            elif text == "honnéte":
                final = "honnête"
            elif text == "I'odeur":
                final = "l'odeur"
            else:
                final = text.rstrip()

            print(final)

            result = ""
            if isBonus:
                result = final
            else:
                for word in self.words:
                    if final in word:
                        result = word[1]

            if self.driver.find_element_by_class_name("game_over_sign").value_of_css_property("display") == "block":
                break

            print(result)
            if not isBonus:
                try:
                    self.driver.find_element_by_class_name("guess").send_keys(result)
                    self.driver.find_element_by_class_name("guess").send_keys(Keys.ENTER)
                except:
                    break
            else:
                try:
                    self.driver.find_element_by_class_name("bonus_guess").send_keys(result)
                    self.driver.find_element_by_class_name("bonus_guess").send_keys(Keys.ENTER)
                except:
                    break

    def level_up(self):
        time.sleep(5)
        self.driver.find_element_by_class_name("end_level_up_btn").click()
        time.sleep(2)
        self.game_loop()
        time.sleep(5)
        self.driver.find_element_by_class_name("back").click()

    def stop(self):
        self.driver.close()


grinder = NuttyGrinder("tbird2@k12albemarle.org", "#Warriors")


def grind():
    try:
        grinder.driver.find_element_by_class_name("dismiss").click()
    except selenium.common.exceptions.ElementNotInteractableException:
        pass

    time.sleep(5)
    grinder.get_words()
    grinder.init_match()
    grinder.game_loop()
    grinder.level_up()
    time.sleep(5)


grind()
# end_level_up_btn
