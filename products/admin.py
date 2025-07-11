from django.contrib import admin
from .models import Category, Product, ProductImage
import cloudinary.uploader
from django.utils.safestring import mark_safe
from tinymce.widgets import TinyMCE
from django.db import models
import os
from modeltranslation.admin import TranslationAdmin

# Register your models here.
class CategoryAdmin(TranslationAdmin):
    fields = ['name', 'slug','description']  # Cho phép nhập slug thủ công
admin.site.register(Category, CategoryAdmin)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0  # Mặc định không thêm dòng trốngAdd commentMore actions
    max_num = 4  # Hạn chế tổng số ảnh được hiển thị là 4
    fields = ('image_file', 'image_url', 'preview')
    readonly_fields = ('image_url', 'preview')

    def preview(self, obj):
        if obj.image_url:
            return mark_safe(f'<img src="{obj.image_url}" width="100" />')
        return "Chưa có ảnh"
    preview.short_description = "Preview"

    def has_add_permission(self, request, obj):
        if obj and obj.images.count() >= self.max_num:
            return False
        return super().has_add_permission(request, obj)

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            remaining_slots = self.max_num - obj.images.count()
            return max(remaining_slots, 0)
        return self.max_num  # Nếu đang tạo mới, cho phép tối đa 4

class ProductAdmin(TranslationAdmin):
    fields = ['name','category','unit','description', 'sold', 'stock', 'sale_price', 'org_price']
    inlines = [ProductImageInline]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 100, 'rows': 30})},
    }

    def save_related(self, request, form, formsets, change):
        
        super().save_related(request, form, formsets, change)

        product = form.instance

        for image in product.images.all():
            if image.image_file and not image.image_url:
                try:
                    # Mở file tường minh
                    image.image_file.open('rb')  # hoặc 'r' nếu là text (nhưng ở đây là binary ảnh)
                    upload_result = cloudinary.uploader.upload(image.image_file)
                    image.image_file.close()  # Đảm bảo đóng file sau khi upload

                    image_url = upload_result.get("secure_url")

                    if image_url:
                        image.image_url = image_url
                        print("✅ Uploaded:", image_url)
                        self.message_user(request, f"✅ Đã upload ảnh cho {product.name}", level='info')

                        # Xoá file local
                        if image.image_file.path and os.path.exists(image.image_file.path):
                            os.remove(image.image_file.path)

                        image.image_file = None
                        image.save()
                    else:
                        self.message_user(request, "⚠️ Upload thất bại: Không có secure_url.", level='error')
                except Exception as e:
                    self.message_user(request, f"❌ Upload lỗi: {e}", level='error')
admin.site.register(Product, ProductAdmin)
