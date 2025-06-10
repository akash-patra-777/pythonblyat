import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from getlogin import TikTokAccountManager, TikTokAccount
from typing import List, Dict

class TikTokPublisher:
    def __init__(self, headless: bool = False):
        self.setup_driver(headless)
        self.results: List[Dict] = []
    
    def setup_driver(self, headless: bool):
        """Setup Chrome driver"""
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 15)
        except Exception as e:
            print(f"Error setting up driver: {e}")

    def login_account(self, account: TikTokAccount) -> bool:
        """Login to TikTok account"""
        try:
            self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
            time.sleep(3)
            
            # Enter email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
            )
            email_input.clear()
            email_input.send_keys(account.email)
            
            # Enter password
            password_input = self.driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_input.clear()
            password_input.send_keys(account.password)
            
            # Click login
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-e2e='login-button']")
            login_button.click()
            
            time.sleep(5)
            
            # Check if login successful
            current_url = self.driver.current_url
            if "login" not in current_url:
                print(f"✅ Logged into {account.username}")
                return True
            else:
                print(f"❌ Failed to login {account.username}")
                return False
                
        except Exception as e:
            print(f"❌ Login error for {account.username}: {e}")
            return False

    def upload_video(self, account: TikTokAccount, video_path: str, caption: str = "", delay: int = 3) -> Dict:
        """Upload video to TikTok account"""
        result = {
            "username": account.username,
            "status": "unknown",
            "message": "",
            "timestamp": time.time()
        }
        
        try:
            # Login first
            if not self.login_account(account):
                result["status"] = "login_failed"
                result["message"] = "Failed to login"
                return result
            
            # Go to upload page
            self.driver.get("https://www.tiktok.com/upload")
            time.sleep(3)
            
            # Find file input and upload video
            file_input = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(os.path.abspath(video_path))
            
            print(f"📤 Uploading video for {account.username}...")
            time.sleep(10)  # Wait for video to process
            
            # Add caption if provided
            if caption:
                try:
                    caption_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-text='true']"))
                    )
                    caption_input.clear()
                    caption_input.send_keys(caption)
                except:
                    print(f"⚠️ Could not add caption for {account.username}")
            
            # Click post button
            post_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-e2e='publish-button']"))
            )
            post_button.click()
            
            time.sleep(5)
            
            # Check if upload was successful
            try:
                success_element = self.driver.find_element(By.CSS_SELECTOR, ".upload-success")
                result["status"] = "success"
                result["message"] = "Video uploaded successfully"
                print(f"✅ Video uploaded successfully for {account.username}")
            except NoSuchElementException:
                result["status"] = "unknown"
                result["message"] = "Upload status unknown"
                print(f"❓ Upload status unknown for {account.username}")
            
        except TimeoutException:
            result["status"] = "timeout"
            result["message"] = "Upload timeout"
            print(f"⏳ Upload timeout for {account.username}")
        except Exception as e:
            result["status"] = "error"
            result["message"] = f"Upload error: {e}"
            print(f"❌ Upload error for {account.username}: {e}")
        
        return result

    def publish_to_all_accounts(self, accounts: List[TikTokAccount], video_path: str, caption: str = "", delay: int = 10):
        """Publish video to all accounts"""
        if not os.path.exists(video_path):
            print(f"❌ Video file not found: {video_path}")
            return
        
        print(f"🚀 Starting to publish video to {len(accounts)} accounts...")
        print(f"📹 Video: {video_path}")
        print(f"📝 Caption: {caption}")
        
        for i, account in enumerate(accounts, 1):
            print(f"\n[{i}/{len(accounts)}] Publishing to: {account.username}")
            
            result = self.upload_video(account, video_path, caption, delay)
            self.results.append(result)
            
            # Add delay between uploads
            if i < len(accounts):
                print(f"⏳ Waiting {delay} seconds before next upload...")
                time.sleep(delay)
        
        self.print_summary()

    def print_summary(self):
        """Print upload summary"""
        successful = len([r for r in self.results if r["status"] == "success"])
        failed = len([r for r in self.results if r["status"] in ["login_failed", "error", "timeout"]])
        unknown = len([r for r in self.results if r["status"] == "unknown"])
        
        print(f"\n=== UPLOAD SUMMARY ===")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"❓ Unknown: {unknown}")
        print(f"📊 Total: {len(self.results)}")

    def close(self):
        """Close browser"""
        if hasattr(self, 'driver'):
            self.driver.quit()

def main():
    manager = TikTokAccountManager()
    accounts = manager.list_accounts()
    
    if not accounts:
        print("❌ No accounts found! Add accounts first.")
        return
    
    print("🎬 TikTok Video Publisher")
    print(f"📱 Found {len(accounts)} accounts")
    
    # Get video file
    video_path = input("Enter video file path: ").strip().strip('"')
    if not os.path.exists(video_path):
        print("❌ Video file not found!")
        return
    
    # Get caption
    caption = input("Enter video caption (optional): ").strip()
    
    # Get settings
    headless = input("Run in headless mode? (y/n): ").lower().strip() == 'y'
    delay = int(input("Delay between uploads (seconds, default 10): ").strip() or "10")
    
    publisher = TikTokPublisher(headless=headless)
    
    try:
        publisher.publish_to_all_accounts(accounts, video_path, caption, delay)
    finally:
        publisher.close()

if __name__ == "__main__":
    main()