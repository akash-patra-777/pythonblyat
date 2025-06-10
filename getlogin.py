import json 
import os
import time
from datetime import datetime
from typing import List, Dict, Optional

class TikTokAccount:
   def __init__(self, username: str, password: str, email: str,display_name: str = ""):
       self.username = username
       self.password = password
       self.email = email
       self.display_name = display_name or username
       self.created_at = datetime.now().isoformat()
       self.is_active = True

   def to_dict(self) -> Dict:
         return {
           "username": self.username,
           "password": self.password,
           "email": self.email,
           "display_name": self.display_name,
           "created_at": self.created_at,
           "is_active": self.is_active
       }
   @classmethod
   def from_dict(cls, data: Dict):
      account = cls(data["username"],data["password"],data["email"],data["display_name"])
      account.created_at = data.get("created_at", datetime.now().isoformat())
      account.is_active = data.get("is_active", True)
      return account
class TikTokAccountManager:
   def __init__(self, storage_file: str = "accounts.json"):
      self.storage_file = storage_file
      self.accounts: List[TikTokAccount] = []
      self.load_accounts()

   def add_account(self, username: str, password: str, email: str, display_name: str = "") -> bool:
       if self.get_account(username):
           print(f"Poszel nachuj {username} jest zajety")
           return False
       
       account = TikTokAccount(username, password, email, display_name)
       self.accounts.append(account)
       self.save_accounts()
       print(f"Poszel nachuj {username} zostal dodany")
       return True
   
   def get_account(self, username: str) -> Optional[TikTokAccount]:
       for account in self.accounts:
           if account.username == username:
               return account
       return None
   
   """List accounts"""

   def list_accounts(self) -> List[TikTokAccount]:
       active_accounts = [account for account in self.accounts if account.is_active]
       if not active_accounts:
              print("Nima kont")
              return []
       for account in active_accounts:
           print(f"Username: {account.username}, Email: {account.email}, Display Name: {account.display_name}, Created At: {account.created_at}")
           
       return active_accounts   
   


   def remove_account(self, username: str) -> bool:
       account = self.get_account(username)
       if account:
           account.is_active = False
           self.save_accounts()
           print(f"Poszel nachuj {username} zostal usuniety")
           return True
       print(f"Poszel nachuj {username} nie isntieje")
       return False
   
   def save_accounts(self):
       data = [account.to_dict() for account in self.accounts]
       with open(self.storage_file, "w") as f:
           json.dump(data, f, indent=2)

   def load_accounts(self):
       if os.path.exists(self.storage_file):
          try:
               with open(self.storage_file, "r") as f:
                   data = json.load(f)
                   self.accounts = [TikTokAccount.from_dict(account) for account in data]
          except(json.JSONDecodeError, KeyError) as e:
              print(f"Error loading accounts: {e}")
              self.accounts = []
       else:
          self.accounts = []
   def import_accounts_txt(self,filename: str):
       
       try:
            with open(filename, "r") as f:
                 lines = f.readlines()

            for line in lines:
                line = line.strip() # removve spaces / newlines
                if line:

                    parts =line.split(":")
                    if len(parts) >= 3:
                        username = parts[0]
                        password = parts[1]
                        email = parts[2]
                        display_name = parts[3] if len(parts) > 3 else ""

                        self.add_account(username, password, email, display_name)
                    print(f"Poszel nachuj {filename} imported")
                    return True
       except FileNotFoundError:
                print(f"Poszel nachuj {filename} nie istnieje")
                return False


def main():
    manager = TikTokAccountManager()
    while True:
        print("TikTok Traffic Manager")
        print("1. Add Account")
        print("2. Remove Account")
        print("3. List Accounts")
        print("4. Exit")
        print("5. Checker")
        print("6. Publish Video")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            print("1. Add Single Account")
            print("2. Add Multiple Accounts")
            sub_choice = input("Enter choice: ").strip()
            if sub_choice == "1":
                username = input("Enter Username: ").strip()
                password = input("Enter Passwrod: ").strip()
                email = input("Enter Email: ").strip()
                display_name = input("Enter Display Name (optioonal): ").strip()
                manager.add_account(username, password, email, display_name)
            elif sub_choice == "2":
                filename = input("Enter filename with accounts (*.txt): ").strip()
                manager.import_accounts_txt(filename)
        
        elif choice == "2":
            username = input("Enter username to remove: ").strip()
            manager.remove_account(username)
        elif choice == "3":
            manager.list_accounts()
        elif choice == "4":
            print("Exiting...")
            time.sleep(2)
            exit(0)
        elif choice == "5":
            from checker import TikTokChecker
            accounts = manager.list_accounts()
            if accounts:
                headless = input("Run in headless mode? (y/n): ").strip().lower() == 'y'
                delay = int(input("Enter delay between checks (seconds && defalut 5 sec): ").strip() or 5)
                checker = TikTokChecker(headless=headless)
                try:
                    checker.check_accounts(accounts, delay)
                    checker.print_summary()
                finally:
                    checker.close()
            else:
                print("No active accounts to check.")
        elif choice == "6":
            from publisher import TikTokPublisher
            accounts = manager.list_accounts()
            if accounts:
                video_path = input("Enter video file path: ").strip().strip('"')
                if not os.path.exists(video_path):
                    print("❌ Video file not found!")
                    continue
                
                caption = input("Enter video caption (optional): ").strip()
                headless = input("Run in headless mode? (y/n): ").strip().lower() == 'y'
                delay = int(input("Delay between uploads (seconds, default 10): ").strip() or "10")
                
                publisher = TikTokPublisher(headless=headless)
                try:
                    publisher.publish_video(accounts, video_path, caption, delay)
                finally:
                    publisher.close()
            else:
                print("No active accounts to publish to.")
        else:
            print("jeestes inwalidem")
        
if __name__ == "__main__":
    main()    

        
       