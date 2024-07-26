from django import forms
from .models import SIPlan, SerialNumber, Mapping, NCRTracker, POTracker, DefectiveLibrary, SIShipped 
from .models import *


class SiPlanForm(forms.ModelForm):
    class Meta:
        model = SIPlan
        fields = "__all__"
    
    date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter PO'})

    
class ExcelUploadForm(forms.Form):
    excel_file = forms.FileField(label='Upload Excel File')



class SerialNumberForm(forms.ModelForm):
    class Meta:
        model = SerialNumber
        fields = '__all__'

    date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))


class MappingForm(forms.ModelForm):
    class Meta:
        model = Mapping
        fields = '__all__'




class NCRTrackerForm(forms.ModelForm):
    ncr_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    approval_Date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    containment_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    corrective_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    preventive_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    varifiction_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    details = forms.CharField(widget=forms.TextInput)
    po_details = forms.CharField(widget=forms.TextInput)
    product_description = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = NCRTracker
        exclude=['consumed','add_quantity']

class NcrdumpForm(forms.ModelForm):
    class Meta:
        model = Ncrdump
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            # Set readonly attribute for cuspn and product fields
            self.fields['add_qty'].widget.attrs['readonly'] = True

class NCRTrackerUpdateForm(forms.ModelForm):
    class Meta:
        model = NCRTracker
        fields=['add_quantity']
        


class POTrackerForm(forms.ModelForm):
    class Meta:
        model = POTracker
        exclude = ['add_quantity','consumed','remaining']

    def __init__(self, *args, **kwargs):
        super(POTrackerForm, self).__init__(*args, **kwargs)



class NCRdumpupdateForm(forms.ModelForm):
    class Meta:
        model = Ncrdump
        fields='__all__'


            
        


class POTrackerUpdateForm(forms.ModelForm):
    class Meta:
        model = POTracker
        fields=['add_quantity']

class DefectiveLibraryForm(forms.ModelForm):
    original_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta: 
        model = DefectiveLibrary
        fields = '__all__'

class SIShippedAddForm(forms.ModelForm):
    invoice_date = forms.DateTimeField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = SIShipped
        exclude = ['sl_no']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set all fields as required
        for field_name, field in self.fields.items():
            field.required = True



from django import forms

class SIShippedSearchForm(forms.Form):
 search_term = forms.CharField(
        label=False,  # Hides the label
        required=False,  # Makes the field non-required
        widget=forms.TextInput(attrs={'placeholder': 'search'})
    )
