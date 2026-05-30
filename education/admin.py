from django.contrib import admin
from .models import Category, Module, Lesson, PhishingIndicator, Resource, Video


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'sort_order', 'slug', 'color', 'icon']
    list_editable = ['sort_order', 'color']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1
    fields = ['title', 'order', 'has_interactive']


class ResourceInline(admin.TabularInline):
    model = Resource
    extra = 1
    fields = ['title', 'resource_type', 'url']


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'module_type', 'difficulty', 'points', 'duration_minutes', 'is_active', 'order']
    list_filter = ['category', 'module_type', 'difficulty', 'is_active']
    list_editable = ['is_active', 'order', 'points']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['prerequisites']
    inlines = [LessonInline, ResourceInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'category')
        }),
        ('Content', {
            'fields': ('content', 'video_url')
        }),
        ('Settings', {
            'fields': ('module_type', 'difficulty', 'duration_minutes', 'points', 'order', 'is_active')
        }),
        ('Prerequisites', {
            'fields': ('prerequisites',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'module', 'order', 'has_interactive']
    list_filter = ['module', 'has_interactive']
    list_editable = ['order']
    search_fields = ['title', 'module__title']


@admin.register(PhishingIndicator)
class PhishingIndicatorAdmin(admin.ModelAdmin):
    list_display = ['name', 'indicator_type', 'severity']
    list_filter = ['indicator_type', 'severity']
    search_fields = ['name', 'description']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'module', 'created_at']
    list_filter = ['resource_type']
    search_fields = ['title', 'description']


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration', 'status', 'sort_order']
    list_filter = ['category', 'status']
    list_editable = ['status', 'sort_order']
    search_fields = ['title', 'description']
