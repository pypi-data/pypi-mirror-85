# -*- coding: utf-8 -*-

import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from juriscraper.lib.cookie_utils import normalize_cookies
from juriscraper.lib.html_utils import clean_html
from juriscraper.lib.html_utils import get_html_parsed_text
from juriscraper.lib.html_utils import fix_links_but_keep_anchors


class WebDriven:
    def __init__(self, *args, **kwargs):
        self.cookies = {}
        self.url = False
        self.uses_selenium = True
        self.wait = False
        self.webdriver = False

    def __del__(self):
        if self.webdriver:
            # sometimes quiting below throws a cryptic and otherwise ignorable OS error
            try:
                self.webdriver.quit()
            except:
                pass

    def get_page(self):
        text = clean_html(self.webdriver.page_source)
        html = get_html_parsed_text(text)
        html.rewrite_links(fix_links_but_keep_anchors, base_href=self.url)
        return html

    def initiate_webdriven_session(self):
        if not self.url:
            raise Exception("self.url not set")

        webdriver_conn = os.environ.get("WEBDRIVER_CONN", "local")
        if webdriver_conn == "local":
            # Use the locally installed PhantomJS binary
            phantomjs_bin_path = "/usr/local/bin/phantomjs"
            self.webdriver = webdriver.PhantomJS(
                executable_path=phantomjs_bin_path,
                service_args=[
                    "--ignore-ssl-errors=true",
                    "--ssl-protocol=any",
                ],
                # uncomment line below to see webdriver log
                service_log_path=os.path.devnull,
            )
        else:
            # It's a connection string to a remote driver
            options = webdriver.ChromeOptions()
            if not os.environ.get("SELENIUM_VISIBLE", False):
                options.add_argument("headless")
            options.add_argument("silent")
            options.add_experimental_option("w3c", False)

            # Workaround for
            # https://bugs.chromium.org/p/chromium/issues/detail?id=1033941
            options.add_argument(
                "--disable-features=AvoidFlashBetweenNavigation,PaintHolding"
            )

            capabilities = options.to_capabilities()
            self.webdriver = webdriver.Remote(
                webdriver_conn,
                desired_capabilities=capabilities,
                keep_alive=True,
            )

        self.webdriver.implicitly_wait(30)
        self.webdriver.set_window_size(5000, 3000)
        self.wait = WebDriverWait(self.webdriver, 10)
        self.webdriver.get(self.url)
        self.cookies = normalize_cookies(self.webdriver.get_cookies())

    def wait_for_id(self, id_attr):
        self.wait.until(EC.presence_of_element_located((By.ID, id_attr)))

    """Use this method to snap screenshots during debugging"""

    def take_screenshot(self, name="screenshot.png"):
        self.webdriver.save_screenshot(name)
