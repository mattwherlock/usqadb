from django import forms
from django.forms import formset_factory, ModelChoiceField
from .models import *
import datetime, extras
from django.utils.translation import ugettext_lazy as _
from bootstrap3_datetime.widgets import DateTimePicker
from datetime import date
from django.db.models.fields import BLANK_CHOICE_DASH
    

# forms for new machine entry - free text:
class NewmachMachine(forms.ModelForm):
    memo = forms.CharField(label='MEMO')
    cris = forms.CharField(label='CRIS')
    system_id = forms.CharField(label='Serial Number')
    ae = forms.CharField(label='AE Title')
    status = forms.CharField(label='Status')
    integrated = forms.CharField(label='PACS Integrated?')
    file_types = forms.CharField(label='File Types:')
    ip = forms.CharField(label='IP address')
    class Meta:
        model = Machine
        fields = ['memo','cris','system_id','ae','status','integrated','file_types','ip']

#class NewmachLocation(forms.Form):
#    location = forms.CharField(label='Location', required=False)
    
class NewmachLocation(forms.ModelForm):
    location = forms.CharField(label='Location', required=False)
    class Meta:
        model = Location
        fields = ['location']
    
class NewmachManufacturer(forms.ModelForm):
    manufacturer = forms.CharField(label='Manufacturer')
    class Meta:
        model = Manufacturer
        fields = ['manufacturer']
    
class NewmachNameModel(forms.ModelForm):
    name_model = forms.CharField(label='Name/Model')
    class Meta:
        model = NameModel
        fields = ['name_model']
    
class NewmachGateway(forms.ModelForm):
    gateway = forms.CharField(label='Gateway')
    class Meta:
        model = Gateway
        fields = ['gateway']
    
class NewmachSubnet(forms.ModelForm):
    subnet = forms.CharField(label='Subnet')
    class Meta:
        model = Subnet
        fields = ['subnet']
    
class NewmachPort(forms.ModelForm):
    port = forms.CharField(label='Port')
    class Meta:
        model = Port
        fields = ['port']
    
# forms for searching database:    
class SearchFormMachine(forms.Form):
    Machine = forms.ModelChoiceField(label='MEMO', required=False, queryset = Machine.objects.all().order_by('memo')) 

class SearchFormMemo(forms.Form):
    Memo = forms.ModelChoiceField(required=False, queryset=Machine.objects.all().order_by('memo'))

class SearchFormLocation(forms.Form):
    Location = forms.ModelChoiceField(required=False, queryset=Location.objects.all().order_by('location'))
    
class SearchFormModel(forms.Form):
    Model = forms.ModelChoiceField(required=False, queryset=NameModel.objects.all().order_by('name_model'))
    
class SearchFormManufacturer(forms.Form):
    Manufacturer = forms.ModelChoiceField(required=False, queryset=Manufacturer.objects.all().order_by('manufacturer'))
    
class SearchFormGateway(forms.Form):
    Gateway = forms.ModelChoiceField(required=False, queryset=Gateway.objects.all().order_by('gateway'))
    
class SearchFormSubnet(forms.Form):
    Subnet = forms.ModelChoiceField(required=False, queryset=Subnet.objects.all().order_by('subnet'))
    
class SearchFormPort(forms.Form):
    Port = forms.ModelChoiceField(required=False, queryset=Port.objects.all().order_by('port'))
    
# to override which field is used for dropdowns, we need to subclass
class SerialModelChoiceField(ModelChoiceField):
    def label_from_instance(self,obj):
        return obj.system_id
class SearchFormSerial(forms.Form):
    Serial = SerialModelChoiceField(required=False, queryset = Machine.objects.all().order_by('system_id'), label='Serial Number', to_field_name='system_id')    
    # NB. this is displaying system_id in dropdown, but returning memo

# forms for submitting QA:
class AuditForm(forms.ModelForm):
    id_machine = forms.ModelChoiceField(label='MEMO',required=False, queryset = Machine.objects.all().order_by('memo'))
    patient_id = forms.CharField(label='Patient ID')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name', initial='PHYSICSQA')
    qa_date = forms.DateField(label='Date of QA', initial=date.today(),widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    qa_comments = forms.CharField(label='Audit Comments')
    number_of_probes = forms.IntegerField(label='Number of Probes') 
    tested_by = forms.CharField(label='Tested By')
    test_location = forms.CharField(label='Test Location')
    class Meta:
        model = Audit
        fields = ['id_machine','patient_id','first_name','last_name','qa_date','qa_comments','number_of_probes','tested_by','test_location']
            
class ProbeForm(forms.ModelForm):
    class Meta:
        model = AuditProbe
        fields = ['probe_serial_no', 'probe_model', 'probe_ok_to_use', 'comments']
        labels = {'probe_serial_no':_('Probe Serial Number'), 'probe_model':_('Probe Model'), 'probe_ok_to_use':_('Ok to use?'), 'comments':_('Comments')}
        
class YesNoForm(forms.Form):
    yesno = forms.ChoiceField(choices=extras.YESNO, required=True, label='Probe ok to use?')
    
class YesNoForm2(forms.Form):
    yesno = forms.ChoiceField(choices=BLANK_CHOICE_DASH + list(extras.YESNO), required=False, label='Probe ok to use?') 
    
class SearchFormOkToUse(forms.Form):
    AuditProbe = forms.ModelChoiceField(label='Was the probe ok to use?', required=False, queryset = AuditProbe.objects.all().order_by('probe_ok_to_use'))
# date forms:        
class StartDateForm(forms.Form):
    Start_Date = forms.DateField(label='Start date for search', widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
class EndDateForm(forms.Form):
    End_Date = forms.DateField(label='End date for search', widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    
class ReportDateForm(forms.Form):
    issue_date = forms.DateField(label='Date of report', widget=DateTimePicker(options={"format": "YYYY-MM-DD", "pickTime": False}))
    
class ReportAuditForm(forms.Form):
    audit = forms.ModelChoiceField(label='Patient ID', required=True, queryset=Audit.objects.all())