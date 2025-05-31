from django import template

register = template.Library()

@register.filter
def last_name_initial(username):
    if username:
        parts = username.strip().split()
        if parts:
            return parts[-1][0].upper()  # Lấy ký tự đầu của từ cuối cùng
    return ''
