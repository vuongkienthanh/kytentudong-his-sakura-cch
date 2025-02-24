from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains

from typing import Callable
import time
import logging
import sys

from config import Config

# set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
stdout = logging.StreamHandler(sys.stdout)
logger.addHandler(stdout)
file = logging.FileHandler("kytentudong.log", mode="w", encoding="utf-8")
file.setFormatter(logging.Formatter("{asctime}: {msg}", style="{"))
logger.addHandler(file)

class MyDriver(webdriver.Chrome):
    def __init__(self):
        logger.info("opening chrome ...")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")
        options.add_argument("--remote-debugging-port=9222")
        super().__init__(options=options)

    def finding(self, css: str):
        return self.find_element(By.CSS_SELECTOR, css)

    def waiting(self, css: str):
        logger.info(f"---waiting {css}")
        WebDriverWait(self, 300).until(lambda _: self.finding(css).is_displayed())
        logger.info(f"---done waiting {css}")

    def clicking(self, css: str):
        logger.info(f"---clicking {css}")
        ele = self.finding(css)
        ActionChains(self).scroll_to_element(ele).pause(2).click(ele).perform()
        logger.info(f"---done clicking {css}")

    def goto(self, url: str):
        logger.info(f"---goto {url}")
        self.get(url)
        time.sleep(2)

    def quit(self):
        for i in range(5):
            time.sleep(1)
            logger.info(f"shutting down in {i}")
        super().quit()

def login(driver: MyDriver, username: str, password: str) -> str:
    driver.goto("http://emr.ndtp.org/login")
    logger.info("input username and password, then submit...")
    driver.waiting("input")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    inputs[0].send_keys(username)
    inputs[1].send_keys(password)
    time.sleep(3)
    driver.clicking(".action>button")
    logger.info("submit login done")
    logger.info("waiting cards...")
    driver.waiting("div:has(>.card)")
    logger.info("save current tab handle")
    return driver.current_window_handle

def open_todieutri(driver: MyDriver, url: str):
    driver.goto(url)
    logger.info("waiting for url info ...")
    driver.waiting(".name span:nth-child(1)")
    name = driver.finding(".name span:nth-child(1)").text
    date = driver.finding(".date .input-content>input").get_attribute("value")
    logger.info(f"Patient name is [[[ {name} ]]]")
    logger.info(f"Working on date [[[ {date} ]]]")
    driver.waiting(".footer-btn .right button:nth-child(1)")
    time.sleep(2)

def process(driver: MyDriver, tab0, name: str, tag: str):
    def inner(f: Callable):
        def clicking_link(name: str) -> bool:
            logger.info("clicking footer button ...")
            driver.clicking(".footer-btn .right button:nth-child(1)")
            logger.info(f"======= clicking link {name} ======")
            for _ in range(60):
                time.sleep(1)
                found = False
                for ele in driver.find_elements(By.TAG_NAME, tag):
                    if ele.text == name:
                        ele.click()
                        found = True
                        break
                if found:
                    break
            else:
                logger.warning(f"cant find {name}")
                driver.clicking(".footer-btn .right button:nth-child(1)")
                return False
            return True

        def go_to_new_tab():
            logger.info("goto new tab")
            for window_handle in driver.window_handles:
                if window_handle != tab0:
                    driver.switch_to.window(window_handle)
                    break
            else:
                driver.quit()
                raise Exception("cant go to new tab")

        def finish_and_go_back(name: str):
            logger.info(f"finish {name}")
            logger.info("close tab, switch back to first tab")
            driver.close()
            driver.switch_to.window(tab0)

        def inner2():
            if clicking_link(name):
                if len(driver.window_handles) == 2:
                    go_to_new_tab()
                    f()
                    finish_and_go_back(name)
                else:
                    f()

        return inner2

    return inner

def run_bs(config: Config):
    logger.info("runner for bacsi ...")
    driver = MyDriver()
    tab0 = login(driver, config["bacsi"]["username"], config["bacsi"]["password"])

    for p in config["patients"]:
        open_todieutri(driver, p["url"])

        @process(driver, tab0, name="Phiếu chỉ định", tag="div")
        def phieuchidinh():
            finish = False
            for _ in range(45):
                time.sleep(1)
                logger.info("checking finish the sign button ")
                for w in driver.find_elements(
                    By.CSS_SELECTOR, "button >.button-content"
                ):
                    if w.text == "Hủy ký Bác sĩ":
                        finish = True
                        break
                if finish:
                    logging.info("phieu chi dinh already signed")
                    break
                for w in driver.find_elements(
                    By.CSS_SELECTOR, "button >.button-content"
                ):
                    if w.text == "Ký Bác sĩ":
                        logger.info("clicking the sign button ")
                        w.click()
                        time.sleep(5)
                        break
            logging.info("finish phieu chi dinh")
            logging.info("clicking close button")
            driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Close']")[
                1
            ].click()
            time.sleep(3)

        @process(driver, tab0, name="Tờ điều trị", tag="a")
        def todieutri():
            logger.info("waiting the sign area")
            driver.waiting(".sign-image")
            logger.info("checking if signed")
            time.sleep(5)
            try:
                driver.finding(".sign-image img.text-patient-sign")
                logger.info("-->sign area is already signed")
            except:
                logger.info("-->sign area is not signed")
                logger.info("clicking the sign button")
                driver.clicking(".sign-image .button-content")
                logger.info("waiting the sign image")
                driver.waiting(".sign-image img.text-patient-sign")

        @process(driver, tab0, name="Phiếu thực hiện y lệnh", tag="a")
        def phieuthuchienylenh():
            logger.info("begin signing names...")
            logger.info("initial waiting...")
            driver.waiting(".table-tbody")
            time.sleep(10)
            for col, isok in zip([3, 4, 5, 6, 7], p["vitri_ky_3tra"]["bacsi"]):
                if isok:
                    for row in [4, 3]:
                        try:
                            logger.info(f"clicking sign button at row {row} col {col}")
                            driver.clicking(
                                f"table tbody tr:nth-last-child({row}) td:nth-child({col}) button"
                            )
                            logger.info(f"waiting signed img at row {row} col {col}")
                            driver.waiting(
                                f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img"
                            )
                        except Exception as e:
                            logger.warning(e)
                            continue
                        finally:
                            time.sleep(3)

        if p["ky_xetnghiem"]:
            phieuchidinh()
        if p["ky_todieutri"]:
            todieutri()
        if any(k for k in p["vitri_ky_3tra"]["bacsi"]):
            phieuthuchienylenh()

    driver.quit()

def run_dd(config: Config):
    logger.info("runner for dieuduong ...")
    driver = MyDriver()
    tab0 = login(
        driver, config["dieuduong"]["username"], config["dieuduong"]["password"]
    )

    for p in config["patients"]:
        open_todieutri(driver, p["url"])

        @process(driver, tab0, name="Phiếu thực hiện y lệnh", tag="a")
        def phieuthuchienylenh():
            logger.info("begin signing names...")
            logger.info("initial waiting...")
            driver.waiting(".table-tbody")
            time.sleep(10)
            for col, isok in zip([3, 4, 5, 6, 7], p["vitri_ky_3tra"]["dieuduong"]):
                if isok:
                    row = 2
                    try:
                        logger.info(f"clicking sign button at row {row} col {col}")
                        driver.clicking(
                            f"table tbody tr:nth-last-child({row}) td:nth-child({col}) button"
                        )
                        logger.info(f"waiting signed img at row {row} col {col}")
                        driver.waiting(
                            f"table tbody tr:nth-last-child({row}) td:nth-child({col}) img"
                        )
                    except Exception as e:
                        logger.info(e)
                        continue
                    finally:
                        time.sleep(3)

        if any(k for k in p["vitri_ky_3tra"]["dieuduong"]):
            phieuthuchienylenh()

    driver.quit()
