from django import forms
from .models import Notes,Answers

class Notesform(forms.ModelForm):
    class Meta:
        model=Notes
        fields=("Subject","year","sem","dept","chapter_name","topic_name","video_clip_url","PDF_url","notes")


class AnswerForm(forms.ModelForm):
    class Meta:
        model=Answers
        fields=('question','answer')