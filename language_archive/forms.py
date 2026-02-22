# language_archive/forms.py

from django import forms
from .models import LanguageRecord, GeographicRecord, Speaker, Village

class LanguageRecordForm(forms.ModelForm):
    """言語記録アップロードフォーム"""
    file = forms.FileField(label="ファイル", required=False)
    youtube_url = forms.URLField(
        label="YouTube URL", 
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.youtube.com/watch?v=...'
        })
    )

# --- カスタム初期化メソッドで必須Selectフィールドの設定 ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # file_type (必須)
        file_type_choices = [("", "ファイル種類を選択")] + list(LanguageRecord.FILE_TYPE_CHOICES)
        self.fields['file_type'].choices = file_type_choices
        self.fields['file_type'].widget.attrs['required'] = True

        #language_frequency (未選択を選択肢に追加)
        self.fields['language_frequency'].choices = LanguageRecord.FREQUENCY_CHOICES
        self.fields['language_frequency'].required = False

        # speaker (必須)
        self.fields['speaker'].required = True
        self.fields['speaker'].empty_label = "話者を選択"
        self.fields['speaker'].widget.attrs['required'] = True

        # 言語項目は YouTube の場合は任意のため、required は clean で判定
        self.fields['onomatopoeia_text'].required = False
        self.fields['meaning'].required = False
        self.fields['usage_example'].required = False
        self.fields['onomatopoeia_type'].required = False
        self.fields['onomatopoeia_type'].empty_label = "オノマトペ型を選択"

    # サーバーサイドでのバリデーション
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        youtube_url = cleaned_data.get('youtube_url')

        # ファイルまたはYouTube URLのどちらかが必須
        if not file and not youtube_url:
            raise forms.ValidationError("ファイルまたはYouTube URLのいずれかを入力してください。")

        # 両方入力されている場合はエラー
        if file and youtube_url:
            raise forms.ValidationError("ファイルとYouTube URLの両方は指定できません。どちらか一方を選択してください。")

        # YouTube の場合はタイトル必須・言語項目は任意
        if youtube_url:
            if not cleaned_data.get('title') or not str(cleaned_data.get('title')).strip():
                raise forms.ValidationError("YouTube で登録する場合は「タイトル」を入力してください。")
        else:
            # ファイルの場合は言語項目必須
            if not cleaned_data.get('onomatopoeia_text') or not str(cleaned_data.get('onomatopoeia_text')).strip():
                raise forms.ValidationError("オノマトペを入力してください。")
            if not cleaned_data.get('meaning') or not str(cleaned_data.get('meaning')).strip():
                raise forms.ValidationError("意味を入力してください。")
            if not cleaned_data.get('usage_example') or not str(cleaned_data.get('usage_example')).strip():
                raise forms.ValidationError("用例を入力してください。")
            if not cleaned_data.get('onomatopoeia_type'):
                raise forms.ValidationError("オノマトペ型を選択してください。")

        return cleaned_data

    class Meta:
        model = LanguageRecord
        fields = [
            'onomatopoeia_text', 'meaning', 'usage_example',
            'phonetic_notation', 'language_frequency', 'file_type', 'speaker',
            'onomatopoeia_type', 'recorded_date', 'notes', 'youtube_url',
            'title', 'description'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タイトル（YouTube の場合は必須）'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '説明（YouTube の場合は任意）'
            }),
            'onomatopoeia_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'オノマトペを入力'
            }),
            'meaning': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '意味を入力'
            }),
            'usage_example': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '用例を入力'
            }),
            'phonetic_notation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': '音声記号を入力（オプション）'
            }),
            'language_frequency': forms.Select(attrs={'class': 'form-control'}),
            'file_type': forms.Select(attrs={'class': 'form-control'}),
            'speaker': forms.Select(attrs={'class': 'form-control'}),
            'onomatopoeia_type': forms.Select(attrs={'class': 'form-control'}),
            'recorded_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '備考（オプション）'
            }),
        }


class GeographicRecordForm(forms.ModelForm):
    """地理環境データアップロードフォーム"""
    file = forms.FileField(label="ファイル", required=False)  # ファイルは任意に変更
    youtube_url = forms.URLField(
        label="YouTube URL", 
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'https://www.youtube.com/watch?v=...'
        })
    )

    # --- カスタム初期化メソッドで必須Selectフィールドの設定 ---
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # content_type (必須)
        content_type_choices = [("", "コンテンツ種類を選択")] + list(GeographicRecord.CONTENT_TYPE_CHOICES)
        self.fields['content_type'].choices = content_type_choices
        self.fields['content_type'].widget.attrs['required'] = True

        # village (モデルでは任意だが、フォームでは必須)
        self.fields['village'].required = True 
        self.fields['village'].empty_label = "集落を選択"
        self.fields['village'].widget.attrs['required'] = True

    #サーバーサイドでのバリテーション
    def clean_content_type(self):
        data = self.cleaned_data.get('content_type')
        if not data:
            raise forms.ValidationError("コンテンツ種類を選択してください。")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        youtube_url = cleaned_data.get('youtube_url')
        
        # ファイルまたはYouTube URLのどちらかが必須
        if not file and not youtube_url:
            raise forms.ValidationError("ファイルまたはYouTube URLのいずれかを入力してください。")
        
        # 両方入力されている場合はエラー
        if file and youtube_url:
            raise forms.ValidationError("ファイルとYouTube URLの両方は指定できません。どちらか一方を選択してください。")
        
        return cleaned_data
    
    class Meta:
        model = GeographicRecord
        fields = [
            'title', 'content_type', 'description', 'village',
            'latitude', 'longitude', 'captured_date', 'youtube_url'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'タイトルを入力'
            }),
            'content_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': '説明を入力'
            }),
            'village': forms.Select(attrs={'class': 'form-control'}),
            'captured_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class SpeakerForm(forms.ModelForm):
    """話者登録フォーム"""
    
    class Meta:
        model = Speaker
        fields = [
            'speaker_id', 'age_range', 'gender', 'village',
            'consent_video', 'notes'
        ]
        widgets = {
            'speaker_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '話者IDを入力(例: SPK001)'
            }),
            'age_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '年代を入力（例: 70代）'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'village': forms.Select(attrs={'class': 'form-control'}),
            'consent_video': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '備考（オプション）'
            }),
        }