from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import time

# Telegram bot tokeni
TELEGRAM_TOKEN = '7470209818:AAFMOnZ1zaECMQve3acmnmACMMTwWCX2-5Y'

# Telegram botga xabar yuborish funksiyasi
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {
        'chat_id': '@your_channel_or_bot_id',  # Kanal yoki bot ID
        'text': message
    }
    requests.post(url, data=payload)

# Multiple login and password pairs
login_credentials = [
    {'login': 'muhammadsamadarov', 'password': 'Ulugbek2008'},
    {'login': 'navruzxujanov', 'password': 'shagzod2008'},
    # Add more login and password pairs here
]

def login_to_emaktab():
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--headless")  # Headless rejim
    
    # ChromeDriver ni o'rnatish
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get('https://login.emaktab.uz/')
    
    for creds in login_credentials:
        try:
            # Explicit wait: elementlar mavjud bo'lishini kutish
            wait = WebDriverWait(driver, 10)
            username_field = wait.until(EC.presence_of_element_located((By.NAME, 'login')))
            password_field = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
            
            # Login va parolni kiritish
            username_field.clear()
            password_field.clear()
            username_field.send_keys(creds['login'])
            password_field.send_keys(creds['password'])
            
            # Tizimga kirish tugmasini topish va bosish
            submit_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="submit"]')))
            submit_button.click()
            
            # Kirish jarayonidan so'ng kutish
            time.sleep(5)

            # Chiqish tugmasini topish va bosish
            logout_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Chiqish')]")))
            logout_button.click()

            # Chiqish jarayonidan so'ng kutish
            time.sleep(3)

            # "Kirish" tugmasini topish va bosish
            login_again_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Kirish']")))
            login_again_button.click()

        except Exception as e:
            send_telegram_message(f"{creds['login']} sahifaga kirishda xato: {str(e)}")
    
    driver.quit()
    
    # Barcha kirish jarayonlari tugagandan so'ng, xabar yuborish
    send_telegram_message("Barcha foydalanuvchilar muvaffaqiyatli faollashtirildi!")

# Telegram bot komandasi
async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    login_to_emaktab()  # Sahifaga kirish
    await update.message.reply_text('9 - B SINF EMAKTAB FAOLASHTIRILDI!')

# Botni ishga tushirish
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("hello", hello))

app.run_polling()
