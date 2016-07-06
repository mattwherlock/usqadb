
from django.shortcuts import render
from django.db.models import Count
from .models import *
from .forms import *
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import modelformset_factory
import datetime
from django.contrib.auth.decorators import login_required
    
def home(request):
    return render(request, 'usqadb/home.html')

# submit a new qa
@login_required    
def audit(request):
    ProbeFormSet = modelformset_factory(AuditProbe, fields=('probe_serial_no', 'probe_model', 'probe_ok_to_use', 'comments'), extra=5)
    if request.method == 'POST':
        form = AuditForm(request.POST)
        formset = ProbeFormSet(request.POST)
        if form.is_valid():
            form.save()
            id_audit_fk = Audit.objects.latest('id_audit')
            if formset.is_valid():
                for pform in formset.forms:
                    if pform.is_valid() and pform.has_changed():
                        probe = pform.save(commit=False)
                        probe.id_audit = id_audit_fk
                        probe.save()
                    else:
                        continue
            message = 'Submitted.  Thank you!'
            return render(request, 'usqadb/submitted.html', {'message':message})
        else:
            message = "Oh dear, something isn't quite right here!"
            return render(request, 'usqadb/submitted.html', {'message':message})
    else:
        form = AuditForm()
        return render(request, 'usqadb/qa_form.html', {'form':form, 'formset':ProbeFormSet(queryset=AuditProbe.objects.none())})

# show list of previous qa and machines where qa is due in 6 weeks
@login_required 
def machine_list(request):
    date_now = datetime.datetime.now()
    date_now = date_now.date()
    threshold = datetime.timedelta(weeks=46)
    last_week = date_now - threshold
    entry = Audit.objects.all()
    entry_25 = entry.order_by('-id_audit')[0:25]
    late = entry.filter(qa_date__lt=last_week)
    report_to_issue = entry.filter(report_issued = None)
    return render(request, 'usqadb/machine_list.html', {'entry':entry_25, 'late':late, 'report_to_issue':report_to_issue})

# this version allows a more flexible serach for machine
@login_required 
def machine_detail(request):
    # shows details regarding selected machine
    if request.method == 'POST':
        memo = SearchFormMemo(request.POST) # search by machine
        serial = SearchFormSerial(request.POST)
        location = SearchFormLocation(request.POST)
        model = SearchFormModel(request.POST)
        select = []
        search_terms = []
        if memo.is_valid():
            c_memo = memo.cleaned_data['Memo']
            if c_memo is not None:
                result_memo = Machine.objects.filter(memo=c_memo)
                if result_memo.count() != 0:
                    select.append(result_memo)
                    audits = AuditProbe.objects.filter(id_audit__id_machine__memo=c_memo).order_by('-id_probe')[0:25]
                    search_terms.append(['MEMO', c_memo])
        if serial.is_valid():
            c_serial = serial.cleaned_data['Serial']
            if c_serial is not None:
                result_serial = Machine.objects.filter(memo=c_serial)
                if result_serial.count() != 0:
                    select.append(result_serial)
                    audits = AuditProbe.objects.filter(id_audit__id_machine__memo=c_serial).order_by('-id_probe')[0:25]
                    search_terms.append(['Serial Number', c_serial])
        if location.is_valid():
            c_location = location.cleaned_data['Location']
            if c_location is not None:
                result_location = Machine.objects.filter(id_location__location=c_location)
                if result_location.count() != 0:
                    select.append(result_location)
                    audits = AuditProbe.objects.filter(id_audit__id_machine__id_location__location=c_location).order_by('-id_probe')[0:25]
                    search_terms.append(['Location', c_location])    
        if model.is_valid():
            c_model = model.cleaned_data['Model']
            if c_model is not None:
                result_model = Machine.objects.filter(id_name_model__name_model=c_model)
                if result_model.count() != 0:
                    select.append(result_model)
                    audits = AuditProbe.objects.filter(id_audit__id_machine__id_name_model__name_model=c_model).order_by('-id_probe')[0:25]
                    search_terms.append(['Model', c_model])   
        if len(select) == 0:
            message = "Sorry, no records were found for this search."
            return render(request, 'usqadb/submitted.html', {'message':message})
        else:
            matched = list(set.intersection(*map(set,select)))
            if len(matched) == 0:
                message = "Sorry, no records were found for this search."
                return render(request, 'usqadb/submitted.html', {'message':message})
            else:
                search_cat = [entry[0] for entry in search_terms]
                search_val = [entry[1] for entry in search_terms]
                return render(request, 'usqadb/machine_detail2.html', {'matched':matched, 'search_cat':search_cat, 'search_val':search_val, 'audits':audits})
    else:
        memo = SearchFormMemo()
        serial = SearchFormSerial()
        location = SearchFormLocation()
        model = SearchFormModel()
        return render(request, 'usqadb/machine_detail_search.html', {'memo':memo, 'serial':serial, 'location':location, 'model':model})   
    
# search for previous qa
@login_required 
def search(request):
    if request.method == 'POST':
        audit = ReportAuditForm(request.POST)
        machine = SearchFormMachine(request.POST) # search by machine
        probeok = YesNoForm2(request.POST) # search by passed or failed probes
        start_date = StartDateForm(request.POST)
        end_date = EndDateForm(request.POST)
        # list containers for output from selected dropdowns
        select = []
        search_terms = []   
        if audit.is_valid():
            c_audit = audit.cleaned_data['audit']
            result_audit = AuditProbe.objects.filter(id_audit__patient_id=c_audit)
            if result_audit.count() != 0:
                select.append(result_audit)
                search_terms.append(['Patient ID',c_audit]) 
        if machine.is_valid():
            c_machine = machine.cleaned_data['Machine']
            result_machine = AuditProbe.objects.filter(id_audit__id_machine__memo=c_machine)
            if result_machine.count() != 0:
                select.append(result_machine)
                search_terms.append(['Machine',c_machine])                
        if probeok.is_valid():
            c_probeok = probeok.cleaned_data['yesno']
            result_probeok = AuditProbe.objects.filter(probe_ok_to_use=c_probeok)
            if result_probeok.count() != 0:
                select.append(result_probeok)
                search_terms.append(['Probe ok to use?',c_probeok])
        if start_date.is_valid() and end_date.is_valid():
            c_start_date = start_date.cleaned_data['Start_Date']
            c_end_date = end_date.cleaned_data['End_Date']
            result_date = AuditProbe.objects.filter(id_audit__qa_date__range=(c_start_date, c_end_date))
            if result_date.count() != 0:
                select.append(result_date)
                search_terms.append(['Start Date',c_start_date])
                search_terms.append(['End Date',c_end_date])
        if len(select) == 0:
            message = "Sorry, no records were found for this search."
            return render(request, 'usqadb/submitted.html', {'message':message})
        else:
            matched = list(set.intersection(*map(set,select)))
            search_cat = [entry[0] for entry in search_terms]
            search_val = [entry[1] for entry in search_terms]
            return render(request, 'usqadb/search_result2.html', {'matched':matched, 'search_cat':search_cat, 'search_val':search_val, 'select':select}) 
    else:
        audit = ReportAuditForm()
        machine = SearchFormMachine()
        #probeok = SearchFormOkToUse()
        probeok = YesNoForm2()
        start_date = StartDateForm()
        end_date = EndDateForm()
        return render(request, 'usqadb/search.html', {'audit':audit,'machine':machine,'probeok':probeok, 'start_date':start_date, 'end_date':end_date})

# enter details of a new machine.  Won't allow duplicates of model, manufactuere etc
# need a way of picking up existing records - drop down primary to free text?
@login_required
def new_machine(request):
    if request.method == 'POST':
        # free text forms
        machine = NewmachMachine(request.POST)
        location = NewmachLocation(request.POST)
        manufacturer = NewmachManufacturer(request.POST)
        name_model = NewmachNameModel(request.POST)
        gateway = NewmachGateway(request.POST)
        subnet = NewmachSubnet(request.POST)
        port = NewmachPort(request.POST)
        # dropdowns of existing data
        location_drop = SearchFormLocation(request.POST)
        manufacturer_drop = SearchFormManufacturer(request.POST)
        name_model_drop = SearchFormModel(request.POST)
        gateway_drop = SearchFormGateway(request.POST)
        subnet_drop = SearchFormSubnet(request.POST)
        port_drop = SearchFormPort(request.POST)

        if location_drop.is_valid():
            c_location_drop = location_drop.cleaned_data['Location']
        if location.is_valid():
            c_location = location.cleaned_data['location']
        if c_location_drop is not None:
            location_fk = Location.objects.get(location=c_location_drop).id_location
        elif location.is_valid() and len(c_location) != 0:
            new_item = Location(location=c_location)
            new_item.save()
            location_fk = Location.objects.get(location=c_location).id_location
        else:
            message = "Please check details for location and resubmit"
            return render(request, 'usqadb/submitted.html', {'message':message})
        
        if manufacturer_drop.is_valid():
            c_manufacturer_drop = manufacturer_drop.cleaned_data['Manufacturer']
        if manufacturer.is_valid():
            c_manufacturer = manufacturer.cleaned_data['manufacturer']
        if c_manufacturer_drop is not None:
            manufacturer_fk = Manufacturer.objects.get(manufacturer=c_manufacturer_drop).id_manufacturer
        elif manufacturer.is_valid() and len(c_manufacturer) != 0:
            new_item = Manufacturer(manufacturer=c_manufacturer)
            new_item.save()
            manufacturer_fk = Manufacturer.objects.get(manufacturer=c_manufacturer).id_manufacturer
        else:
            message = "Please check details for manufacturer and resubmit"
            return render(request, 'usqadb/submitted.html', {'message':message})

        if name_model_drop.is_valid():
            c_name_model_drop = name_model_drop.cleaned_data['Model']
        if name_model.is_valid():
            c_name_model = name_model.cleaned_data['name_model']
        if c_name_model_drop is not None:
            name_model_fk = NameModel.objects.get(name_model=c_name_model_drop).id_name_model
        elif name_model.is_valid() and len(c_name_model) != 0:
            new_item = NameModel(name_model=c_name_model)
            new_item.save()
            name_model_fk = NameModel.objects.get(name_model=c_name_model).id_name_model
        else:
            message = "Please check details for name/model and resubmit"
            return render(request, 'usqadb/submitted.html', {'message':message})

        if gateway_drop.is_valid():
            c_gateway_drop = gateway_drop.cleaned_data['Gateway']
        if gateway.is_valid():
            c_gateway = gateway.cleaned_data['gateway']
        if c_gateway_drop is not None:
            gateway_fk = Gateway.objects.get(gateway=c_gateway_drop).id_gateway
        elif gateway.is_valid() and len(c_gateway) != 0:
            new_item = Gateway(gateway=c_gateway)
            new_item.save()
            gateway_fk = Gateway.objects.get(gateway=c_gateway).id_gateway
        else:
            message = "Please check details for gateway and resubmit"
            return render(request, 'usqadb/submitted.html', {'message':message})

        if subnet_drop.is_valid():
            c_subnet_drop = subnet_drop.cleaned_data['Subnet']
        if subnet.is_valid():
            c_subnet = subnet.cleaned_data['subnet']
        if c_subnet_drop is not None:
            subnet_fk = Subnet.objects.get(subnet=c_subnet_drop).id_subnet
        elif subnet.is_valid() and len(c_subnet) != 0:
            new_item = Subnet(subnet=c_subnet)
            new_item.save()
            subnet_fk = Subnet.objects.get(subnet=c_subnet).id_subnet
        else:
            message = "Please check details for subnet and resubmit"
            return render(request, 'usqadb/submitted.html', {'message':message})

        if port_drop.is_valid():    
            c_port_drop = port_drop.cleaned_data['Port']
        if port.is_valid():
            c_port = port.cleaned_data['port']
        if c_port_drop is not None:
            port_fk = Port.objects.get(port=c_port_drop).id_port
        elif port.is_valid() and len(c_port) != 0:
            new_item = Port(port=c_port)
            new_item.save()
            port_fk = Port.objects.get(port=c_port).id_port
        else:
            message = "Please check details for port and resubmit"
            return render(request, 'usqadb/submitted.html', {'message':message})
        
        if machine.is_valid():
            mach = machine.save(commit=False)
            mach.id_location = Location.objects.get(id_location=location_fk)
            mach.id_manufacturer = Manufacturer.objects.get(id_manufacturer=manufacturer_fk)
            mach.id_name_model = NameModel.objects.get(id_name_model=name_model_fk)
            mach.id_gateway = Gateway.objects.get(id_gateway=gateway_fk)
            mach.id_subnet = Subnet.objects.get(id_subnet=subnet_fk)
            mach.id_port = Port.objects.get(id_port=port_fk)
            mach.save()
                
        message = 'Submitted.  Thank you!'
        return render(request, 'usqadb/submitted.html', {'message':message})  
    else:
        machine = NewmachMachine()
        location = NewmachLocation()
        manufacturer = NewmachManufacturer()
        name_model = NewmachNameModel()
        gateway = NewmachGateway()
        subnet = NewmachSubnet()
        port = NewmachPort()
        location_drop = SearchFormLocation()
        manufacturer_drop = SearchFormManufacturer()
        name_model_drop = SearchFormModel()
        gateway_drop = SearchFormGateway()
        subnet_drop = SearchFormSubnet()
        port_drop = SearchFormPort()
        return render(request, 'usqadb/new_machine_form.html', {'machine':machine,'location':location,'manufacturer':manufacturer,'name_model':name_model,'gateway':gateway,'subnet':subnet,'port':port,'location_drop':location_drop,'manufacturer_drop':manufacturer_drop,'name_model_drop':name_model_drop,'gateway_drop':gateway_drop,'subnet_drop':subnet_drop,'port_drop':port_drop})

@login_required    
def report_issued(request):
    if request.method == 'POST':
        audit = ReportAuditForm(request.POST)
        issue_date = ReportDateForm(request.POST)
        if audit.is_valid() and issue_date.is_valid():
            c_issued = audit.cleaned_data['audit']
            c_date = issue_date.cleaned_data['issue_date']
            issued = Audit.objects.get(patient_id=c_issued)
            issued.report_issued = c_date
            issued.save()
            message = 'Submitted.  Thank you!'
            return render(request, 'usqadb/submitted.html', {'message':message})
        else:
            message = "Oh dear, something isn't quite right here!  Please check the form."
            return render(request, 'usqadb/submitted.html', {'message':message})
    else:
        audit = ReportAuditForm()
        issue_date = ReportDateForm()
        return render(request, 'usqadb/report_issued.html', {'audit':audit, 'issue_date':issue_date})