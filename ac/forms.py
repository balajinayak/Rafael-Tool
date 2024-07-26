from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Dummy, FG





class DummyForm(forms.ModelForm):
    marking = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Dummy
        fields = ['fg_number','doc_ref_no','checklist_rev_no','customer','product_desc','product','pro_rev','project_name','security','description','marking']
        
    def clean_fg_number(self):
        fg_number = self.cleaned_data.get('fg_number')
        if Dummy.objects.filter(fg_number=fg_number).exists():
            raise forms.ValidationError("FG number already exists.")
        return fg_number

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("This field is required.")
        return description

        


class FGForm(forms.ModelForm):
    class Meta:
        model = FG
        fields = ['fg_number','work_order','starting','wo_quantity','ending','serial']


    def clean_fg_number(self):
        fg_number = self.cleaned_data.get('fg_number')
        if not fg_number:
            raise forms.ValidationError("This field is required.")
        dummy_fg = Dummy.objects.filter(fg_number=fg_number).exists()
        if dummy_fg == False:
            raise forms.ValidationError("FG Part Number does not exists")
        return fg_number


    def clean_work_order(self):
        work_order = self.cleaned_data.get('work_order')
        if not work_order:
            raise forms.ValidationError("This field is required.")
        if FG.objects.filter(work_order=work_order).exists():
            raise forms.ValidationError("Work order already exists.")
        return work_order

    def clean_starting(self):
        starting = self.cleaned_data.get('starting')
        if not starting:
            raise forms.ValidationError("This field is required.")
        if FG.objects.filter(starting=starting).exists():
            raise forms.ValidationError("Starting already exists.")
        return starting

    def clean_wo_quantity(self):
        wo_quantity = self.cleaned_data.get('wo_quantity')
        if wo_quantity is None:
            raise forms.ValidationError("This field is required.")
        return wo_quantity

    def clean_ending(self):
        ending = self.cleaned_data.get('ending')
        if ending is None:
            raise forms.ValidationError("This field is required.")
        if FG.objects.filter(ending=ending).exists():
            raise forms.ValidationError("Ending already exists.")
        return ending

    def clean_ending(self):
        ending = self.cleaned_data.get('ending')
        if ending is None:
            raise forms.ValidationError("This field is required.")
        if FG.objects.filter(ending=ending).exists():
            raise forms.ValidationError("Ending already exists.")
        return ending