# First time setup - run this only once to save cookies
import pickle
from selenium import webdriver

def first_time_setup(url_login):
    try:
        driver = webdriver.Chrome()
        driver.get(url_login)
        
        print(f"Opening {url_login}")
        print("Please login manually in the browser window...")
        print("After logging in successfully, press Enter in this console...")
        input()  # Wait for user to login and press Enter
        
        # After manual login, save the cookies
        cookies = driver.get_cookies()
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)
        print("Cookies saved successfully!")
        return driver
    except Exception as e:
        print(f"Error: {e}")
# Usage:
url_login = "https://authn.edx.org/login"
driver = first_time_setup(url_login)