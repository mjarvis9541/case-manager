from django import forms

from .models import Case, CaseType


class TriageCaseCreate(forms.ModelForm):
    case_ref = forms.CharField(label='CET Reference', max_length=24, min_length=10) # max_length=10, min_length=10)
    case_type = forms.ModelChoiceField(queryset=CaseType.objects.filter(department=1))#), empty_label='Select')

    class Meta:
        model = Case
        fields = [ 'case_type', 'case_ref', 'note']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.date = kwargs.pop('date')
        super().__init__(*args, **kwargs)


    def clean_case_ref(self, *args, **kwargs):
        case_ref = self.cleaned_data.get('case_ref')
        if not case_ref.upper().startswith('CET'):
            raise forms.ValidationError('CET Reference must begin with CET.')

        if Case.objects.filter(user=self.user, date=self.date, case_ref=case_ref).exists():
            raise forms.ValidationError('You have already logged a case with this reference today.')

        return case_ref.upper()


    # def clean(self, *args, **kwargs):

   
    

class TmTriageCaseCreate(forms.ModelForm):
    case_ref = forms.CharField(label='CET Reference', max_length=24, min_length=10)
    case_type = forms.ModelChoiceField(queryset=CaseType.objects.filter(department=1))#), empty_label='Select')

    class Meta:
        model = Case
        fields = [ 'case_type', 'case_ref', 'note']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.date = kwargs.pop('date')
        super().__init__(*args, **kwargs)

    def clean_case_ref(self, *args, **kwargs):
        case_ref = self.cleaned_data.get('case_ref')

        # if not case_ref.upper().startswith('CET'):
        #     raise forms.ValidationError('CET Reference must begin with CET.')
        # if Case.objects.filter(user=self.user, date=self.date, case_ref=case_ref).exists():
        #     raise forms.ValidationError('You have already logged a case with this CET reference today.')

        return case_ref.upper()


class CaseUpdate(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['date', 'case_ref', 'case_type', 'note']


    
class CaseTypeForm(forms.ModelForm):
    class Meta:
        model = CaseType
        fields = ['department', 'name', 'minutes', 'description']