import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from getlogin import TikTokAccountManager, TikTokAccount
from typing import List, Dict

class TikTokChecker:
    def __init__(self, headless: bool = True):
        self.setup_driver(headless)
        self.results: List[Dict] = []

    def setup_driver(self, headless: bool):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36") 
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
        except Exception as e:
            print(f"error with drivers: {e}")

    def check_account(self, account: TikTokAccount) -> Dict:

        result = {
            "username": account.username,
            "password": account.password,
            "status": "unknown",
            "message": "",
            "timestamp": time.time()
        }

        try:
            # Go to TikTok login page
            self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
            time.sleep(3)
            
            # Find email input
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
            )
            email_input.clear()
            email_input.send_keys(account.username)
            
            # Find password input
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_input.clear()
            password_input.send_keys(account.password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-e2e='login-button']")
            login_button.click()
            
            time.sleep(5)

            current_url = self.driver.current_url
            if "login" not in current_url:
                result["status"] = "valid"
                result["message"] = "Account is valid"
                print(f"✅ {account.username} - VALID")
            else:
                
                try:
                    error_element = self.driver.find_element(By.CSS_SELECTOR, ".TUXTextError")
                    error_text = error_element.text
                    result["status"] = "inwalido jebany"
                    result["message"] = f"Invalid account: {error_text}"
                    print(f"❌ {account.username} - INVALID: {error_text}")
                except NoSuchElementException:
                    result["status"] = "unknown"
                    result["message"] = "Unknown error occurred"
                    print(f"❓ {account.username} - UNKNOWN ERROR")
        except TimeoutException:
            result["status"] = "timeout"
            result["message"] = "Request timed out"
            print(f"⏳ {account.username} - TIMEOUT")
        except Exception as e:
            result["status"] = "error"
            result["message"] = f"An error occurred: {e}"
            print(f"⚠️ {account.username} - ERROR: {e}")
        
        return result
    
    def check_accounts(self, accounts: list[TikTokAccount], delay: int = 5):
        print(f"Start to check {len(accounts)} accounts...")

        for i, account in enumerate(accounts):
            print(f"\n[{i}/{len(accounts)}] Checking account: {account.username}")

            result = self.check_account(account)
            self.results.append(result)

            if i < len(accounts):
                print(f"Waiting {delay} seconds...")
                time.sleep(delay)
            
            self.save_results()

    def save_results(self):
            """logs kurwa"""
            filename = f"check_results_{int(time.time())}.json"
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\nResults saved to {filename}")

    def print_summary(self):
        """Print summary of check results"""
        valid = len([r for r in self.results if r["status"] == "valid"])
        invalid = len([r for r in self.results if r["status"] == "invalid"])
        unknown = len([r for r in self.results if r["status"] == "unknown"])
        errors = len([r for r in self.results if r["status"] == "error"])
        
        print(f"\n=== SUMMARY ===")
        print(f"✅ Valid: {valid}")
        print(f"❌ Invalid: {invalid}")
        print(f"⚠️ Unknown: {unknown}")
        print(f"💥 Errors: {errors}")
        print(f"📊 Total: {len(self.results)}")

    def close(self):

            if hasattr(self, 'driver'):
                self.driver.quit()

def main():
    manager = TikTokAccountManager()
    accounts = manager.list_accounts()

    if not accounts:
        print("No accs")
        return

    print("Titok Checker")
    print(f"found {len(accounts)} accounts")

    headless = input("Run in headless mode? (y/n): ").strip().lower() == 'y'
    delay = int(input("Enter delay between checks (seconds && defalut 5 sec): ").strip() or 5)

    checker = TikTokChecker(headless=headless)

    try:
        checker.check_accounts(accounts, delay)
        checker.print_summary()
    finally:
        
        print("Closing checker...")
        time.sleep(2)
        print("Checker closed.")
        checker.close()

if __name__ == "__main__":
    main()
