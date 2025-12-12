import os
import json
import time
from datetime import datetime
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ================= إعداد الجلسة والمتصفح =================

print("=" * 50)
print("🤖 بوت واتساب - بدء التشغيل")
print("=" * 50)

# مجلد المشروع على سطح المكتب
BASE_DIR = Path.home() / "Desktop" / "WhatsApp_Bot"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# مجلد الجلسة
SESSION_DIR = BASE_DIR / "whatsapp_session"
SESSION_DIR.mkdir(parents=True, exist_ok=True)

# ملف الرسائل
MSG_FILE = BASE_DIR / "messages.json"
if not MSG_FILE.exists():
    with open(MSG_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=2)

print(f"📂 مجلد المشروع: {BASE_DIR}")
print(f"📂 مجلد الجلسة:  {SESSION_DIR}")
print(f"📄 ملف الرسائل:  {MSG_FILE}")

# إعداد خيارات كروم
options = Options()
options.add_argument(f"--user-data-dir={SESSION_DIR}")     # حفظ الجلسة
options.add_argument("--profile-directory=Default")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")

print("\n⚙️  جاري تشغيل المتصفح...")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get("https://web.whatsapp.com")
print("📱 تم فتح واتساب ويب\n")

# ================= انتظار تسجيل الدخول =================

try:
    print("⏳ إذا ظهَر QR امسحه من جوالك مرة واحدة فقط.")
    print("   (واتساب -> الإعدادات -> الأجهزة المرتبطة -> ربط جهاز)\n")

    # ننتظر حتى تظهر منطقة الكتابة (يعني تم تسجيل الدخول)
    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[@contenteditable='true']")
        )
    )
    print("✅ تم تسجيل الدخول بنجاح، الجلسة محفوظة.\n")
except Exception as e:
    print("❌ لم يكتمل تسجيل الدخول، تأكد أنك مسحت الـ QR.")
    print(f"الخطأ: {e}")
    driver.quit()
    exit()

# ================= دوال مساعدة =================

def load_messages():
    with open(MSG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_messages(data):
    with open(MSG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_message(chat_name, text):
    messages = load_messages()
    msg = {
        "chat_name": chat_name,
        "text": text,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    messages.append(msg)
    save_messages(messages)
    print(f"📩 رسالة جديدة من: {chat_name}")

# ================= حلقة مراقبة الرسائل (متوافقة مع العربية) =================
print("=" * 50)
print("👀 البوت يعمل الآن ويبحث عن رسائل جديدة")
print("📄 سيتم حفظ الرسائل في messages.json داخل مجلد WhatsApp_Bot على سطح المكتب")
print("⏹ لإيقاف البوت اضغط Ctrl + C في نافذة الأوامر")
print("=" * 50)

def get_chat_name():
    try:
        el = driver.find_element(By.XPATH, "//header//span[@dir='auto']")
        return el.text
    except:
        return "محادثة"

def get_last_incoming_text():
    # نلتقط النص من الرسائل الواردة message-in بغض النظر عن اتجاه النص [web:90]
    try:
        nodes = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'message-in')]//span[contains(@class,'selectable-text')]/span"
        )
        if nodes:
            return nodes[-1].text
    except:
        pass
    return None

def click_unread_chats_if_any():
    # نحاول إيجاد أي بادج لعدد غير مقروء بصيغ متعددة (إنجليزي/عربي) [web:88][web:93]
    selectors = [
        "//span[contains(@aria-label,'unread')]",
        "//span[contains(@aria-label,'غير مقروء')]",
        "//*[@data-testid='icon-unread-count']"
    ]
    for sel in selectors:
        try:
            badges = driver.find_elements(By.XPATH, sel)
            if badges:
                try:
                    badges[0].find_element(
                        By.XPATH,
                        "./ancestor::*[contains(@role,'listitem') or @tabindex]"
                    ).click()
                except:
                    badges[0].find_element(By.XPATH, "./ancestor::div[1]").click()
                time.sleep(2)
                return True
        except:
            continue
    return False

last_saved = {"chat": None, "text": None}

try:
    while True:
        opened = click_unread_chats_if_any()

        chat_name = get_chat_name()
        text = get_last_incoming_text()

        if text and (chat_name != last_saved.get("chat") or text != last_saved.get("text")):
            # قراءة الملف الحالي
            with open(MSG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # إضافة الرسالة الجديدة
            data.append({
                "chat_name": chat_name,
                "text": text,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # حفظ الملف
            with open(MSG_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"📩 تم الحفظ من: {chat_name} | النص: {text[:40]}")
            last_saved = {"chat": chat_name, "text": text}

        time.sleep(5)

except KeyboardInterrupt:
    print("\n⏹ تم إيقاف البوت.")
    driver.quit()