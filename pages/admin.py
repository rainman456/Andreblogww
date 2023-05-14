from django.contrib import admin
from .models import Post,Comments
admin.site.register(Post)

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display=('name','body','post','created')
    list_filter=('active','created')
    search_fields=('name','body')
    actions=['approve']
    def approve(self,request,queryset):
        queryset.update(active=True)
