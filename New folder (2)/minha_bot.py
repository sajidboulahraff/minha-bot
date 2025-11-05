import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

# إعدادات التلغرام
BOT_TOKEN = "7874668042:AAHPPkMFfwR85eNUK_SxzecGB1KHRsc4GFs"
CHAT_ID = "911861074"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# إعدادات الموقع
url = "https://minha.anem.dz/pre_inscription"

def send_telegram_message(message):
    """إرسال رسالة إلى تيلغرام"""
    try:
        requests.post(TELEGRAM_URL, data={"chat_id": CHAT_ID, "text": message})
    except Exception as e:
        print(f"⚠️ فشل في إرسال الرسالة: {e}")

def run_check():
    """تنفيذ الفحص"""
    try:
        # إعدادات Chrome بدون واجهة
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        # تشغيل المتصفح بدون الحاجة لتثبيت Chrome يدوياً
        driver = uc.Chrome(options=chrome_options)
        driver.get(url)
        time.sleep(4)

        # تعبئة البيانات الخاصة بك
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

# تكرار الفحص كل دقيقتين
if __name__ == "__main__":
    while True:
        print("🔍 بدء الفحص...")
        run_check()
        print("⏳ في انتظار دقيقتين للفحص القادم...")
        time.sleep(120)
