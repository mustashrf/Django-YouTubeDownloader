from django import forms

CHOICE_OPTIONS = [
    ('p', 'Playlist'),
    ('s', 'Single Video'),
]
TYPE_OPTIONS = [
    ('video', 'Video'),
    ('audio', 'Audio'),
]
QUALITY_OPTIONS = [
    ('360p', '360p'),
    ('720p', '720p'),
]

class DownloaderForm(forms.Form):
    choice = forms.ChoiceField(choices=CHOICE_OPTIONS, label='Playlist or Single Video')
    url = forms.CharField(max_length=100, label='URL')
    exceptions = forms.CharField(max_length=50, required=False)
    av = forms.ChoiceField(choices=TYPE_OPTIONS, label='Video or Audio')
    quality = forms.ChoiceField(choices=QUALITY_OPTIONS)