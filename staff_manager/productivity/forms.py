from django import forms

from .models import Case, CaseType



class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=50)


class ExportForm(forms.Form):
    pass




class TriageCaseCreate(forms.ModelForm):
    case_ref = forms.CharField(label='CET Reference', max_length=24, min_length=10) # max_length=10, min_length=10)
    case_type = forms.ModelChoiceField(label='Case Type', queryset=CaseType.objects.filter(department=1))#), empty_label='Select')

    class Meta:
        model = Case
        fields = [ 'case_type', 'case_ref', 'note']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.date = kwargs.pop('date')
        super().__init__(*args, **kwargs)


    def clean_case_ref(self, *args, **kwargs):
        case_ref = self.cleaned_data.get('case_ref')
        case_type = self.cleaned_data.get('case_type')

        # if str(case_type) == 'Reclassified' and len(str(case_type)) < 20:
        #     raise forms.ValidationError('Please enter a valid BURN Reference for Reclassified cases.')
          
        if not case_ref.upper().startswith('CET') and not str(case_type) == 'Reclassified':
            raise forms.ValidationError('Please enter a valid CET Reference.')

        if Case.objects.filter(user=self.user, date=self.date, case_ref=case_ref).exists()  and not str(case_type) == 'Additional':
            raise forms.ValidationError('You have already logged a case with this reference today.')

        return case_ref.upper()

    

class CalcCaseCreate(forms.ModelForm):
    case_ref = forms.CharField(label='CET Reference', max_length=24, min_length=10) # max_length=10, min_length=10)
    case_type = forms.ModelChoiceField(label='Case Type', queryset=CaseType.objects.filter(department=2))#), empty_label='Select')

    class Meta:
        model = Case
        fields = [ 'case_type', 'case_ref', 'note']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.date = kwargs.pop('date')
        super().__init__(*args, **kwargs)


    def clean_case_ref(self, *args, **kwargs):
        case_ref = self.cleaned_data.get('case_ref')
        case_type = self.cleaned_data.get('case_type')

        # if str(case_type) == 'Reclassified' and len(str(case_type)) < 20:
        #     raise forms.ValidationError('Please enter a valid BURN Reference for Reclassified cases.')
          
        if not case_ref.upper().startswith('CET') and not str(case_type) == 'Reclassified':
            raise forms.ValidationError('Please enter a valid CET Reference.')

        if Case.objects.filter(user=self.user, date=self.date, case_ref=case_ref).exists():
            raise forms.ValidationError('You have already logged a case with this reference today.')

        return case_ref.upper()




    # def clean(self, *args, **kwargs):
    #     cleaned_data = super().clean()
    #     case_ref = cleaned_data.get('case_ref')
    #     case_type = cleaned_data.get('case_type')
    #     print(case_type)
    #     if str(case_type) == 'Reclassified':
    #         print('re')
    #     if not case_ref.upper().startswith('CET'):
    #         self.add_error('case_ref', 'CET Reference must begin with CET.')

    #     return cleaned_data
   
    

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

        if not case_ref.upper().startswith('CET'):
            raise forms.ValidationError('Please enter a valid CET Reference.')
        if Case.objects.filter(user=self.user, date=self.date, case_ref=case_ref).exists():
            raise forms.ValidationError('You have already logged a case with this CET reference today.')

        return case_ref.upper()


class CaseUpdate(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['date', 'case_ref', 'case_type', 'note']


    
class CaseTypeForm(forms.ModelForm):
    class Meta:
        model = CaseType
        fields = ['department', 'name', 'minutes', 'description']