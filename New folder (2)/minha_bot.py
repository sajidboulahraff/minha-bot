import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

# إعدادات التلغرام
BOT_TOKEN = "7874668042:AAHPPkMFfwR85eNUK_SxzecGB1KHRsc4GFs"
CHAT_ID = "911861074"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# إعدادات المتصفح
driver_path = "chromedriver.exe"
url = "https://minha.anem.dz/pre_inscription"

chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # متصفح مرئي

def send_telegram_message(message):
    """إرسال رسالة إلى تيلغرام"""
    try:
        requests.post(TELEGRAM_URL, data={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print(f"⚠️ فشل في إرسال الرسالة: {e}")

def run_check():
    """تنفيذ الفحص"""
    try:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(3)

        # إدخال المعلومات
        driver.find_element(By.ID, "numeroWassit").send_keys("121901007320")
        driver.find_element(By.ID, "numeroPieceIdentite").send_keys("100010385007320006")
        time.sleep(1)

        driver.find_element(By.ID, "mui-6").click()
        time.sleep(2)

        # زر المواصلة
        continue_button = driver.find_element(By.XPATH, "//button[contains(text(), 'المواصلة')]")
        continue_button.click()
        time.sleep(3)

        # فحص الصفحة
        page_source = driver.page_source

        if "لا يوجد أي موعد متاح" in page_source or "نعتذر" in page_source:
            send_telegram_message("❌ لا توجد مواعيد متاحة حالياً.")
        else:
            send_telegram_message("✅ هناك مواعيد متاحة! ادخل بسرعة إلى الموقع.")

        driver.quit()

    except Exception as e:
        send_telegram_message(f"⚠️ حدث خطأ أثناء الفحص: {e}")
        print(f"⚠️ خطأ في البوت: {e}")

if __name__ == "__main__":
    while True:
        print("🔍 بدء الفحص...")
        run_check()
        print("⏳ في انتظار 2 دقائق للفحص القادم...")
        time.sleep(120)
