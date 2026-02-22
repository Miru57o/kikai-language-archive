# language_archive/admin.py

from django.contrib import admin
from .models import Village, Speaker, OnomatopoeiaType, LanguageRecord, GeographicRecord

@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude']
    search_fields = ['name']
    list_per_page = 20


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ['speaker_id', 'age_range', 'gender', 'village', 'consent_video']
    list_filter = ['gender', 'consent_video', 'village']
    search_fields = ['speaker_id', 'age_range']
    list_per_page = 20


@admin.register(OnomatopoeiaType)
class OnomatopoeiaTypeAdmin(admin.ModelAdmin):
    list_display = ['type_code', 'type_name']
    search_fields = ['type_code', 'type_name']
    list_per_page = 20


@admin.register(LanguageRecord)
class LanguageRecordAdmin(admin.ModelAdmin):
    list_display = ['get_display_title', 'file_type', 'village', 'speaker', 'language_frequency', 'recorded_date']
    list_filter = ['file_type', 'speaker__village', 'recorded_date', 'onomatopoeia_type', 'language_frequency']
    search_fields = ['onomatopoeia_text', 'meaning', 'title', 'description']
    date_hierarchy = 'recorded_date'
    list_per_page = 20
    readonly_fields = ['created_at', 'updated_at']

    autocomplete_fields = ['speaker', 'village', 'onomatopoeia_type']

    def get_display_title(self, obj):
        return obj.display_title or '-'
    get_display_title.short_description = 'タイトル / オノマトペ'
    
    FIELDSETS_BASE = (
        ('基本情報', {
            'fields': ('onomatopoeia_text', 'meaning', 'usage_example', 'phonetic_notation', 'language_frequency')
        }),
        ('ファイル情報', {
            'fields': ('file_type', 'file_path', 'thumbnail_path', 'youtube_url')
        }),
        ('関連情報', {
            'fields': ('speaker', 'onomatopoeia_type', 'village')
        }),
        ('メタデータ', {
            'fields': ('title', 'description', 'recorded_date', 'notes', 'created_at', 'updated_at')
        }),
    )
    
    FIELDSETS_ADD = (
        ('基本情報', {
            'fields': ('onomatopoeia_text', 'meaning', 'usage_example', 'phonetic_notation', 'language_frequency')
        }),
        ('ファイル情報', {
            'fields': ('file_type', 'file_path', 'thumbnail_path', 'youtube_url')
        }),
        ('関連情報', {
            'fields': ('speaker', 'onomatopoeia_type')
        }),
        ('メタデータ', {
            'fields': ('title', 'description', 'recorded_date', 'notes')
        }),
    )

    def get_fieldsets(self, request, obj=None):
        """
        新規作成(obj=None)か編集かでフィールドセットを切り替える
        """
        if not obj:
            # 新規作成時
            return self.FIELDSETS_ADD
        # 編集時
        return self.FIELDSETS_BASE

    def save_model(self, request, obj, form, change):
        """
        新規作成時・編集時ともに話者の集落を関連集落に自動設定
        """
        # 常に話者の集落に同期
        if obj.speaker and obj.speaker.village:
            obj.village = obj.speaker.village
        super().save_model(request, obj, form, change)


@admin.register(GeographicRecord)
class GeographicRecordAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_type', 'village', 'captured_date']
    list_filter = ['content_type', 'village', 'captured_date']
    search_fields = ['title', 'description']
    date_hierarchy = 'captured_date'
    list_per_page = 20
    readonly_fields = ['created_at']
    autocomplete_fields = ['village']

# Register your models here.
