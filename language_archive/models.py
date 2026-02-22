# language_archive/models.py
# Create your models here.

from django.db import models
from django.utils import timezone
import re

class Village(models.Model):
    """集落情報テーブル"""
    name = models.CharField(max_length=100, verbose_name="集落名")
    latitude = models.FloatField(verbose_name="緯度")
    longitude = models.FloatField(verbose_name="経度")
    description = models.TextField(blank=True, verbose_name="説明")
    
    class Meta:
        verbose_name = "集落"
        verbose_name_plural = "集落"
    
    def __str__(self):
        return self.name


class Speaker(models.Model):
    """話者情報テーブル"""
    GENDER_CHOICES = [
        ('M', '男性'),
        ('F', '女性'),
        ('O', 'その他'),
    ]

    AGE_RANGE_CHOICES = [
        ('30-39', '30代'),
        ('40-49', '40代'),
        ('50-59', '50代'),
        ('60-69', '60代'),
        ('70-79', '70代'),
        ('80-89', '80代'),
        ('90-99', '90代'),
        ('100+', '100歳以上'),
    ]

    speaker_id = models.CharField(max_length=50, unique=True, verbose_name="話者ID")
    age_range = models.CharField(max_length=10, choices=AGE_RANGE_CHOICES, verbose_name="年代")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="性別")
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, verbose_name="集落")
    consent_video = models.BooleanField(default=False, verbose_name="映像公開同意")
    notes = models.TextField(blank=True, verbose_name="備考")
    
    class Meta:
        verbose_name = "話者"
        verbose_name_plural = "話者"
    
    def __str__(self):
        return f"{self.speaker_id} ({self.age_range}, {self.get_gender_display()})"


class OnomatopoeiaType(models.Model):
    """オノマトペ型マスタ"""
    type_code = models.CharField(max_length=10, unique=True, verbose_name="型コード")
    type_name = models.CharField(max_length=100, verbose_name="型名")
    description = models.TextField(verbose_name="説明")
    
    class Meta:
        verbose_name = "オノマトペ型"
        verbose_name_plural = "オノマトペ型"
    
    def __str__(self):
        return f"{self.type_code}: {self.type_name}"


class LanguageRecord(models.Model):
    """言語記録データテーブル"""
    FILE_TYPE_CHOICES = [
        ('audio', '音声'),
        ('video', '映像'),
        ('image', '画像'),
    ]
    
    FREQUENCY_CHOICES = [
        ('','未選択'),
        ('daily', '日常的に使用'),
        ('often', 'よく使用'),
        ('sometimes', 'たまに使用'),
        ('rarely', 'ほとんど使用しない'),
    ]
    # 基本情報（YouTubeのみの場合は null 可）
    onomatopoeia_text = models.CharField(max_length=100, blank=True, null=True, verbose_name="オノマトペ")
    meaning = models.TextField(blank=True, null=True, verbose_name="意味")
    usage_example = models.TextField(blank=True, null=True, verbose_name="用例")
    phonetic_notation = models.TextField(blank=True, null=True, verbose_name="音声記号")
    language_frequency = models.CharField(blank=True, default='', max_length=20, choices=FREQUENCY_CHOICES, null=True, verbose_name="言語使用頻度")
    
    # ファイル情報
    file_type = models.CharField(max_length=10, choices=FILE_TYPE_CHOICES, verbose_name="ファイル種類")
    file_path = models.URLField(max_length=1024, null=True, blank=True, verbose_name="ファイルURL")
    thumbnail_path = models.URLField(max_length=1024, blank=True, verbose_name="サムネイルURL")
    youtube_url = models.URLField(max_length=1024, blank=True, null=True, verbose_name="YouTube URL")
    
    # 関連情報
    speaker = models.ForeignKey(Speaker, on_delete=models.PROTECT, null=True, blank=True, verbose_name="話者")
    onomatopoeia_type = models.ForeignKey(OnomatopoeiaType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="型")
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="関連集落")
    
    # メタデータ（YouTube の場合は title / description を使用）
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name="タイトル")
    description = models.TextField(blank=True, null=True, verbose_name="説明")
    recorded_date = models.DateField(verbose_name="収録日")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    notes = models.TextField(blank=True, verbose_name="備考")
    
    class Meta:
        verbose_name = "言語記録"
        verbose_name_plural = "言語記録"
        ordering = ['-recorded_date']
    
    def __str__(self):
        if self.youtube_url and self.title:
            return self.title
        if self.onomatopoeia_text:
            return self.onomatopoeia_text
        return f"記録 #{self.pk}"

    @property
    def display_title(self):
        """一覧・詳細で表示するタイトル（YouTube の場合は title、それ以外は onomatopoeia_text）"""
        if self.youtube_url and self.title:
            return self.title
        return self.onomatopoeia_text or ""
    
    def get_youtube_embed_url(self):
        """
        get_youtube_embed_url の Docstring
        
        :param self: 説明
        """
        if self.youtube_url:
            match = re.search(r'(?:v=|youtu\.be/)([^&]+)', self.youtube_url)
            if match:
                return f"https://www.youtube.com/embed/{match.group(1)}"
        return None


class GeographicRecord(models.Model):
    """地理・環境データテーブル"""
    CONTENT_TYPE_CHOICES = [
        ('drone_video', 'ドローン映像'),
        ('drone_photo', 'ドローン画像'),
        ('other', 'その他'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="タイトル")
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, verbose_name="コンテンツ種類")
    file_path = models.URLField(max_length=1024, null=True, blank=True, verbose_name="ファイルURL")
    thumbnail_path = models.URLField(max_length=1024, blank=True, verbose_name="サムネイルURL")
    youtube_url = models.URLField(max_length=1024, null=True, blank=True, verbose_name="YouTube URL")
    
    description = models.TextField(verbose_name="説明")
    village = models.ForeignKey(Village, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="集落")
    latitude = models.FloatField(null=True, blank=True, verbose_name="緯度")
    longitude = models.FloatField(null=True, blank=True, verbose_name="経度")
    
    captured_date = models.DateField(verbose_name="撮影日")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="登録日時")
    
    class Meta:
        verbose_name = "地理環境データ"
        verbose_name_plural = "地理環境データ"
        ordering = ['-captured_date']
    
    def __str__(self):
        return self.title
    
    def get_youtube_embed_url(self):
        """YouTube URLを埋め込み用URLに変換"""
        if not self.youtube_url:
            return None
        patterns = [
            r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]+)', # Standard URL
            r'(?:https?://)?(?:www\.)?youtu\.be/([a-zA-Z0-9_-]+)', # Shortened URL
            r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]+)', # Embed URL
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.youtube_url)
            if match:
                video_id = match.group(1)
                return f"https://www.youtube-nocookie.com/embed/{video_id}?rel=0&modestbranding=1"
        
        return None
