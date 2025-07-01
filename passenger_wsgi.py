import os
import sys

# Đường dẫn tuyệt đối đến file log (nên dùng absolute path để tránh lỗi)
log_path = os.path.join(os.path.dirname(__file__), 'passenger_wsgi.log')

# Mở file log và redirect sys.stderr (lỗi) vào log file
sys.stderr = open(log_path, 'a')

# Nếu cần ghi luôn sys.stdout (in thông thường) thì bỏ comment dòng sau
sys.stdout = open(log_path, 'a')

# Load ứng dụng WSGI
from sun_asia.wsgi import application
