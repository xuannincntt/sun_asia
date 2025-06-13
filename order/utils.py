import random
import string
from email_validator import validate_email, EmailNotValidError
from babel import Locale
from datetime import datetime
from babel.dates import format_datetime

LANG_TO_LOCALE = {
    "vi": "vi_VN",
    "en": "en_US",
    "ja": "ja_JP"
}

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def check_email(email):
    try:
        valid = validate_email(email)
        return True, valid.normalized
    except EmailNotValidError as e:
        return False, str(e)

def validate_order_form(form):
    print(form)
    if not form['name'] or len(form['name']) == 0:
        return "Bạn chưa điền họ tên của người nhận hàng."
    result, value = check_email(form['email'])
    if not result:
        return "Email không hợp lệ."
    if not form['tel'] or len(form['tel']) == 0:
        return "Bạn chưa điền số điện thoại nhận hàng."
    if not form['address'] or len(form['address']) == 0:
        return "Bạn chưa điền địa chỉ nhận hàng."
    if not form['items'] or len(form['items']) == 0:
        return "Bạn chưa có mặt hàng nào."
    return None

def format_date_time(dt=None, lang_code="vi"):
    if dt is None:
        dt = datetime.now()

    try:
        locale = LANG_TO_LOCALE.get(lang_code)
        print(locale)  # ví dụ: vi_VN
        formatted = format_datetime(dt, locale=locale)
        return formatted
    except Exception as e:
        print("Không tìm thấy locale hoặc lỗi khác:", e)
        return None
    
