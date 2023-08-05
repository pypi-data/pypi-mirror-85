import time
import json
import multiprocessing
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import socket
import requests
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from testing.testcases import LiveTornadoTestCase
from testing.selenium_helper import SeleniumHelper

from django.core import mail


# From https://realpython.com/testing-third-party-apis-with-mock-servers/
class MockServerRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/admin/?page=call&pi=restapi':
            self.send_response(requests.codes.not_found)
            self.end_headers()
            return
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )
        cmd = form['cmd'].value
        if cmd == 'login':
            self.send_response(requests.codes.ok)
            self.send_header('Set-Cookie', 'fish=2000')
            self.end_headers()
        elif cmd == 'subscriberAdd':
            self.send_response(requests.codes.ok)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                'status': 'OK',
                'data': {
                    'id': 19
                }
            }).encode(encoding='utf_8'))
        elif cmd == 'listSubscriberAdd':
            self.send_response(requests.codes.ok)
            self.end_headers()
        else:
            self.send_response(requests.codes.not_found)
            self.end_headers()
        return


def get_free_port():
    s = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    address, port = s.getsockname()
    s.close()
    return port


class PHPlistTest(LiveTornadoTestCase, SeleniumHelper):
    fixtures = [
        'initial_documenttemplates.json',
        'initial_styles.json'
    ]

    @classmethod
    def start_server(cls, port):
        httpd = HTTPServer(('', port), MockServerRequestHandler)
        httpd.serve_forever()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.base_url = cls.live_server_url
        driver_data = cls.get_drivers(1)
        cls.driver = driver_data["drivers"][0]
        cls.client = driver_data["clients"][0]
        cls.driver.implicitly_wait(driver_data["wait_time"])
        cls.wait_time = driver_data["wait_time"]
        cls.server_port = get_free_port()
        cls.server = multiprocessing.Process(
            target=cls.start_server,
            args=(cls.server_port,)
        )
        cls.server.daemon = True
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        cls.server.terminate()
        super().tearDownClass()

    def test_signup_yes_not_available(self):
        self.signup(self.driver, True)

    def test_signup_no_not_available(self):
        self.signup(self.driver, False)

    def test_signup_no_available(self):
        with self.settings(
            PHPLIST_BASE_URL='http://localhost:{}/'.format(self.server_port)
        ):
            self.signup(self.driver, False)

    def test_signup_yes_available(self):
        with self.settings(
            PHPLIST_BASE_URL='http://localhost:{}/'.format(self.server_port)
        ):
            self.signup(self.driver, True, True)

    def assertInfoAlert(self, message):
        i = 0
        message_found = False
        while(i < 100):
            i = i + 1
            try:
                if self.driver.find_element(
                    By.CSS_SELECTOR,
                    "body #alerts-outer-wrapper .alerts-info"
                ).text == message:
                    message_found = True
                    break
                else:
                    time.sleep(0.1)
                    continue
            except StaleElementReferenceException:
                time.sleep(0.1)
                continue
        self.assertTrue(message_found)

    def signup(self, driver, list=False, signed_up=False):
        driver.get(urljoin(self.base_url, "/account/sign-up/"))
        driver.find_element_by_id(
            'id_username'
        ).send_keys('username_no')
        driver.find_element_by_id(
            'id_password1'
        ).send_keys('password')
        driver.find_element_by_id(
            'id_password2'
        ).send_keys('password')
        driver.find_element_by_id(
            'id_email'
        ).send_keys('my.no@email.com')
        driver.find_element_by_id(
            'signup-submit'
        ).click()
        time.sleep(1)
        signup_link = self.find_urls(mail.outbox[-1].body)[0]
        driver.get(signup_link)
        driver.find_element(
            By.ID,
            'terms-check'
        ).click()
        driver.find_element(
            By.ID,
            'test-check'
        ).click()
        if list:
            answer = "yes"
        else:
            answer = "no"
        driver.find_element(
            By.CSS_SELECTOR,
            'input[name="emaillist"][value="{}"]'.format(answer)
        ).click()
        submit_button = driver.find_element(
            By.ID,
            'submit'
        )
        submit_button.click()
        if signed_up:
            self.assertInfoAlert("Subscribed to email list")
        WebDriverWait(driver, self.wait_time).until(
            EC.staleness_of(submit_button)
        )
        self.assertEqual(
            driver.find_element_by_css_selector(
                '.fw-contents h1'
            ).text,
            'Thanks for verifying!'
        )
