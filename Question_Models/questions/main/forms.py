from django import forms

class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(TestForm, self).__init__(*args, **kwargs)
        for question in questions:
            if question.choice_set.exists():
                choices = [(choice.id, choice.text) for choice in question.choice_set.all()]
                self.fields[str(question.id)] = forms.ChoiceField(label=question.text, choices=choices, widget=forms.RadioSelect)
            else:
                self.fields[str(question.id)] = forms.CharField(label=question.text, widget=forms.Textarea)
