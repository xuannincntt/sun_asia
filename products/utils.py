import unicodedata
import re

def create_slug(name):
    name = name.lower()
    name = unicodedata.normalize('NFD', name)
    name = name.encode('ascii', 'ignore').decode('utf-8')
    name = re.sub(r'[^a-z0-9\s.-]', '', name)
    name = re.sub(r'[.\s]+', '-', name)
    name = re.sub(r'-+', '-', name)
    return name.strip('-')

def create_unique_slug(instance, name_field, slug_field='slug'):
    """
    Tạo slug không trùng từ trường tên. Nếu đã có sẽ thêm hậu tố -1, -2,...
    """
    from django.db.models import Model
    assert isinstance(instance, Model), "instance phải là model object"

    slug = create_slug(getattr(instance, name_field))
    ModelClass = instance.__class__
    unique_slug = slug
    num = 1

    while ModelClass.objects.filter(**{slug_field: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"
        num += 1

    return unique_slug
