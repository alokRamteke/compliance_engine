from django.contrib import admin
from core.models import Content, Guideline, ReviewItem


@admin.register(Guideline)
class GuidelineAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file', 'version', 'created_at', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'file')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ReviewItem)
class ReviewItemAdmin(admin.ModelAdmin):
    list_display=('id', 'content', 'guideline', 'status', 'reviewer', 'reviewed_at')
    list_filter=('guideline', 'status', 'reviewer')
    search_fields=('guideline__title', 'guideline__description', 'content__title')
    readonly_fields = ('reviewed_at',)
