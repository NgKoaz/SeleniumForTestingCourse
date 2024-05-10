import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time


class Main:
    WAIT_LOADING_PAGE_TIME = 30

    def __init__(self):
        # Initialization
        self.EXE_PATH = "chromedriver.exe"
        self.service = Service(executable_path=self.EXE_PATH)
        self.driver = webdriver.Chrome(service=self.service)

        self.log_file = "result/log.txt"

        # Go to login page
        self.goToLoginPageAndLogin()

        # Check has logon.
        self.checkHasLogon()

        # Run quiz test
        self.traverseCoursesAndDoSomething(self.quizTest)

        # Run assignment test
        self.doAssignmentTest()

        time.sleep(100)

    def goToLoginPageAndLogin(self):
        # Get login page and credentials
        with open("input/login.json", "r") as file:
            login_json = json.load(file)
            login_url = login_json["url"]
            username = login_json["username"]
            password = login_json["password"]

        # Login locator
        with open("web_item/login_page.json", "r") as file:
            login_item = json.load(file)
            username_field = login_item["username_field"]
            password_field = login_item["password_field"]
            login_button = login_item["login_button"]

        # Go to login page moodle
        self.driver.get(url=login_url)
        # Wait until page loaded
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
            lambda x: x.find_element(By.CSS_SELECTOR, username_field)
        )

        # Put username and password
        username_tag = self.driver.find_element(By.CSS_SELECTOR, username_field)
        password_tag = self.driver.find_element(By.CSS_SELECTOR, password_field)
        username_tag.send_keys(username)
        password_tag.send_keys(password)

        # Click sign in button
        sign_in_button = self.driver.find_element(By.CSS_SELECTOR, login_button)
        sign_in_button.click()

    def checkHasLogon(self):
        with open("input/login.json", "r") as file:
            login_json = json.load(file)
            name_profile = login_json["name_profile"]

        with open("web_item/my_courses_page.json", "r") as file:
            my_courses_locator = json.load(file)
            login_info_selector = my_courses_locator["login_info"]

            # Wait until page loaded
            WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, login_info_selector))
            )
            # Wait secondary loading
            time.sleep(2)

            login_info = self.driver.find_element(By.CSS_SELECTOR, login_info_selector)
            if str(login_info.get_attribute("text")) == name_profile:
                self.log("Login success!")

    def traverseCoursesAndDoSomething(self, doSomething):
        with open("web_item/my_courses_page.json", "r") as file:
            js = json.load(file)
            courses_selector = js["courses"]

        with open("web_item/course_detail.json", "r") as file:
            js = json.load(file)
            quiz_selector = js["quiz"]

        counter = 0
        course_index = 0
        while True:
            courses = self.driver.find_elements(By.CSS_SELECTOR, courses_selector)
            print("NUM OF COURSE: ", len(courses))
            print("INDEX: ", course_index)
            if len(courses) <= 0:
                time.sleep(1)
                counter += 1
                if counter >= 4:
                    break
                continue

            counter = 0

            # Out of range
            if course_index >= len(courses):
                break

            # Click with current index
            try:
                courses[course_index].click()
            except Exception as e:
                self.driver.execute_script("window.scrollBy(0, 230);")
                continue

            # Unfold all task
            self.unFoldAll()

            # Do something
            # doSomething()
            with open("web_item/course_detail.json", "r") as file:
                js = json.load(file)
                quiz_selector = js["quiz"]
                assignment_selector = js["assignment"]

            with open("web_item/start_quiz_page.json", "r") as file:
                js = json.load(file)
                attempt_button_selector = js["attempt_button"]

            quizzes = self.driver.find_elements(By.CSS_SELECTOR, assignment_selector)

            for quiz in quizzes:
                print(quiz.get_attribute("href"))

            # ---------------------------------

            self.driver.back()
            course_index += 1

    def quizTest(self):
        with open("web_item/course_detail.json", "r") as file:
            js = json.load(file)
            quiz_selector = js["quiz"]
        with open("web_item/start_quiz_page.json", "r") as file:
            js = json.load(file)
            attempt_button_selector = js["attempt_button"]

        quizzes = self.driver.find_elements(By.CSS_SELECTOR, quiz_selector)

        if len(quizzes) <= 0:
            return

        quizzes[0].click()
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME)

        try:
            attempt_button = self.driver.find_element(By.CSS_SELECTOR, attempt_button_selector)
            attempt_button.click()
            WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME)
        except:
            self.driver.back()
            return

        self.doQuiz()
        time.sleep(100)

        self.driver.back()

    def doQuiz(self):
        with open("web_item/quiz_page.json", "r") as file:
            js = json.load(file)
            radio_choice_selector = js["choice"]
            finish_button_selector = js["finish_button"]
            submit_button_selector = js["submit_button"]
            submit_button_in_modal_selector = js["submit_button_in_warning_modal"]
        with open("web_item/review_quiz.json", "r") as file:
            js = json.load(file)
            finish_review_button_selector = js["finish_review_button"]

        choices = self.driver.find_elements(By.CSS_SELECTOR, radio_choice_selector)
        for choice in choices:
            choice.click()
            time.sleep(0.25)

        finish_button = self.driver.find_element(By.CSS_SELECTOR, finish_button_selector)
        finish_button.click()
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME)

        submit_button = self.driver.find_element(By.CSS_SELECTOR, submit_button_selector)
        submit_button.click()


        try:
            WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
                lambda x: self.driver.find_element(By.CSS_SELECTOR, submit_button_in_modal_selector)
            )
            submit_button_in_modal = self.driver.find_element(By.CSS_SELECTOR, submit_button_in_modal_selector)
            submit_button_in_modal.click()
            WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME)
        except:
            pass

        time.sleep(3)

        finish_review_button = self.driver.find_element(By.CSS_SELECTOR, finish_review_button_selector)
        self.clickAction(finish_review_button)
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME)
        time.sleep(10)
        # Check UI
        self.checkStartQuizUI()

        time.sleep(100)

    def checkStartQuizUI(self):
        with open("web_item/quiz_page.json") as file:
            js = json.load(file)
            attempt_button_selector = js["attempt_button"]
            quiz_review_summary_selector = js["quiz_review_summary"]

        attempt_button = self.driver.find_element(By.CSS_SELECTOR, attempt_button_selector)
        print(attempt_button.text)

        review_summaries = self.driver.find_elements(By.CSS_SELECTOR, quiz_review_summary_selector)
        print("REVIEW SUMMARIES", len(review_summaries))

        time.sleep(100)


    def doAssignmentTest(self):
        pass

    def assignmentTest(self):
        pass

    def unFoldAll(self):
        with open("web_item/course_detail.json", "r") as file:
            js = json.load(file)
            collapse_all_selector = js["collapse_all"]
            nav_selector = js["nav"]

            # Wait until page loaded
            WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
                lambda x: x.find_element(By.CSS_SELECTOR, nav_selector)
            )
            # Wait secondary loading
            time.sleep(2)

            # Some course detail don't have. So we have to catch error here
            try:
                collapse_all = self.driver.find_element(By.CSS_SELECTOR, collapse_all_selector)
                attribute_value = collapse_all.get_attribute("aria-expanded")
                if str(attribute_value) == "false":
                    collapse_all.click()
                else:
                    collapse_all.click()
                    time.sleep(0.8)
                    collapse_all.click()
            except:
                pass

            time.sleep(1)

    def zoomOut(self):
        self.driver.execute_script("document.body.style.zoom = 0.5")
        time.sleep(2)

    def clickAction(self, obj):
        try:
            obj.click()
            return
        except:
            self.driver.execute_script("window.scrollBy(0, 230);")
        try:
            obj.click()
        except:
            pass



    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(message)


Main()

