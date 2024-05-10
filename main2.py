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
        # Go to quiz page
        #self.quizTest()
        # Go to assignment page
        self.assignmentTest()

        time.sleep(200)

    def assignmentTest(self):
        with open("test/assignment.json", "r") as file:
            js = json.load(file)
            assignmentTests = js["assignment"]

        for testcase in assignmentTests:
            self.goToAssignmentPage(testcase)

    def quizTest(self):
        with open("test/quiz.json", "r") as file:
            js = json.load(file)
            quizTestcases = js["quiz"]
        for quizTc in quizTestcases:
            self.goToQuizPage(quizTc)
            time.sleep(3)

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

    def goToQuizPage(self, quizTestcase):
        quiz_url = quizTestcase["url"]
        answers = quizTestcase["answer"]
        with open("web_item/start_quiz_page.json", "r") as file:
            js = json.load(file)
            attempt_button_selector = js["attempt_button"]
            attempt_button_dialog_selector = js["attempt_button_dialog"]
        with open("web_item/quiz_page.json", "r") as file:
            js = json.load(file)
            answer_selection_box_selector = js["answer_selection_box"]
            finish_button_selector = js["finish_button"]
            submit_button_selector = js["submit_button"]
            question_not_answer_yet_selector = js["question_not_answer_yet"]
            submit_button_in_modal_selector = js["submit_button_in_warning_modal"]
        with open("web_item/review_quiz_page.json", "r") as file:
            js = json.load(file)
            correct_answer_selector = js["correct_answer"]

        # Go to quiz page moodle
        self.driver.get(url=quiz_url)
        # Wait until page loaded
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
            lambda x: self.driver.find_element(By.CSS_SELECTOR, attempt_button_selector)
        )
        print("QUIZ PAGE HERE!!!!!!!!!!!")

        # Click attempt button, ready to do quiz.
        try:
            attempt_button = self.driver.find_element(By.CSS_SELECTOR, attempt_button_selector)
            attempt_button.click()
            print("ATTEMP CLICKL!!!!!!!!!!!!!!")
            time.sleep(0.1)
            attempt_button_dialog = self.driver.find_elements(By.CSS_SELECTOR, attempt_button_dialog_selector)
            if len(attempt_button_dialog) > 0:
                pass
            print("ATTEMPT BUTTON CLICKL!!!!!!!!!!!!!!")
            WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
                lambda x: self.driver.find_element(By.CSS_SELECTOR, answer_selection_box_selector)
            )
        except:
            self.driver.back()
            return

        # Do quiz
        question_id = []
        question_not_answer = self.driver.find_elements(By.CSS_SELECTOR, question_not_answer_yet_selector)
        for question in question_not_answer:
            _id = question.get_attribute("id")
            question_id.append(_id)
            idx = int(_id.split("-")[-1])
            answer_box_selector = f"#{_id} input[value=\"{answers[idx - 1]}\"][type=\"radio\"]"
            print(answer_box_selector)
            answer_box = self.driver.find_element(By.CSS_SELECTOR, answer_box_selector)
            answer_box.click()
            time.sleep(0.1)

        finish_button = self.driver.find_element(By.CSS_SELECTOR, finish_button_selector)
        finish_button.click()
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
            lambda x: self.driver.find_element(By.CSS_SELECTOR, submit_button_selector)
        )

        # Submit
        submit_button = self.driver.find_element(By.CSS_SELECTOR, submit_button_selector)
        submit_button.click()
        time.sleep(1)
        submit_button_in_modal = self.driver.find_elements(By.CSS_SELECTOR, submit_button_in_modal_selector)
        if len(submit_button_in_modal) > 0:
            submit_button_in_modal[0].click()
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME)

        # We are at review page
        correct_answer = self.driver.find_elements(By.CSS_SELECTOR, correct_answer_selector)
        print(len(correct_answer))

    def goToAssignmentPage(self, assignmentTest):
        url = assignmentTest["url"]
        text = assignmentTest["text"]

        with open("web_item/start_assignment.json", "r") as file:
            js = json.load(file)
            assignment_button_selector = js["assignment_button"]
        with open("web_item/assignment_page.json", "r") as file:
            js = json.load(file)
            textarea_selector = js["textarea"]
            save_button_selector = js["save_button"]

        # Go to quiz page moodle
        self.driver.get(url=url)
        # Wait until page loaded
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
            lambda x: self.driver.find_element(By.CSS_SELECTOR, assignment_button_selector)
        )

        print("Click button")
        assignment_button = self.driver.find_element(By.CSS_SELECTOR, assignment_button_selector)
        assignment_button.click()
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME).until(
            lambda x: self.driver.find_element(By.CSS_SELECTOR, textarea_selector)
        )
        print("Preparing to send keys:", text)
        while True:
            try:
                textarea = self.driver.find_element(By.CSS_SELECTOR, textarea_selector)
                textarea.send_keys(text)
                break
            except:
                print("TextArea cannot be sent keys! Send again...")

        save_button = self.driver.find_element(By.CSS_SELECTOR, save_button_selector)
        save_button.click()
        WebDriverWait(self.driver, self.WAIT_LOADING_PAGE_TIME)

        # Check if save fail, we will navigate to start assignment page
        textarea = self.driver.find_elements(By.CSS_SELECTOR, textarea_selector)
        if len(textarea) > 0:
            print("FAILLLLLLLLLLLLLLLLLUIRE")

    def log(self, message):
        with open(self.log_file, "a") as file:
            file.write(message)


Main()

