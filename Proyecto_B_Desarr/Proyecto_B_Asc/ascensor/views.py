from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from ascensor.forms import ClienteForm, OrdenForm, TecnicoForm

from .models import Cliente, Orden, Tecnico


# Create your views here.
@login_required
def index(request):
    if not request.user.is_authenticated:
        return redirect('%s?next=%s&noauth=noauth' % (settings.LOGIN_URL, request.path))
    else:
        if request.user.is_staff:
            return redirect('ListadoOrdenes.html')
        else:
            return redirect('MisClientes.html')

@staff_member_required(login_url=settings.LOGIN_URL)
def listadoOrdenes(request):
    ordenes = Orden.objects.all()
    return render(request, 'ascensor/ListadoOrdenes.html', {'ordenes':ordenes})

@login_required
def nuevaOrden(request):
    if request.method == 'POST':
        form = OrdenForm(request.POST)
        if form.is_valid():
            #TODO: Guardar
            return HttpResponseRedirect('ascensor/ListadoOrdenes.html')
    else:
        form = OrdenForm()

    return render(request, 'ascensor/NuevaOrden.html', {'form': form})

def salir(request):
    logout(request)
    return HttpResponseRedirect('/ascensor')


# Clientes
@staff_member_required(login_url=settings.LOGIN_URL)
def listadoClientes(request):
    if request.method == 'POST':
        form = None
        if (request.POST['idCliente'] != "None"):
            instance = get_object_or_404(Cliente,id=request.POST['idCliente'])
            form = ClienteForm(request.POST,instance=instance)
        else:
            form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ascensor/ListadoClientes.html?mensaje=exito')
    else:
        form = ClienteForm()
    # Consulta de clientes
    clientes = Cliente.objects.all()
    return render(request, 'ascensor/ListadoClientes.html', {'form': form,'clientes':clientes})

@staff_member_required(login_url=settings.LOGIN_URL)
def formClientes(request):
    pk = request.GET.get('id','')
    datos = dict()
    if(pk!=''):
        # Editar
        form = ClienteForm(instance=get_object_or_404(Cliente,pk=request.GET['id']))
        datos['formulario'] = render_to_string('ascensor/formularios/form_clientes.html',context={'form':form},request=request)
        # return render(request,'ascensor/formularios/form_clientes.html',context={'form':form})
    else:
        # Nuevo
        form = ClienteForm()
        datos['formulario'] = render_to_string('ascensor/formularios/form_clientes.html',context={'form':form},request=request)
    return JsonResponse(datos)

@staff_member_required(login_url=settings.LOGIN_URL)
def eliminarCliente(request):
    pk = request.GET.get('id','')
    cliente = get_object_or_404(Cliente,pk=pk)
    cliente.delete()
    return JsonResponse({"respuesta":"OK"})

#Tecnicos
@staff_member_required(login_url=settings.LOGIN_URL)
def listadoTecnicos(request):
    if request.method == 'POST':
        form = None
        if (request.POST['idTecnico'] != "None"):
            instance = get_object_or_404(Tecnico,id=request.POST['idTecnico'])
            form = TecnicoForm(request.POST,instance=instance)
        else:
            form = TecnicoForm(request.POST)
        if form.is_valid():
            form.instance.username = form.instance.email
            form.instance.set_password(form.instance.password)
            form.save()
            return HttpResponseRedirect('/ascensor/ListadoTecnicos.html?mensaje=exito')
    else:
        form = TecnicoForm()
    # Consulta de clientes
    tecnicos = Tecnico.objects.all()
    return render(request, 'ascensor/ListadoTecnicos.html', {'form': form,'tecnicos':tecnicos})

@staff_member_required(login_url=settings.LOGIN_URL)
def formTecnicos(request):
    pk = request.GET.get('id','')
    datos = dict()
    if(pk!=''):
        # Editar
        form = TecnicoForm(instance=get_object_or_404(Tecnico,pk=request.GET['id']))
        datos['formulario'] = render_to_string('ascensor/formularios/form_tecnicos.html',context={'form':form},request=request)
    else:
        # Nuevo
        form = TecnicoForm()
        datos['formulario'] = render_to_string('ascensor/formularios/form_tecnicos.html',context={'form':form},request=request)
    return JsonResponse(datos)

@staff_member_required(login_url=settings.LOGIN_URL)
def eliminarTecnicos(request):
    pk = request.GET.get('id','')
    tecnico = get_object_or_404(Tecnico,pk=pk)
    tecnico.delete()
    return JsonResponse({"respuesta":"OK"})

# Clientes (tecnico)
@login_required
def misClientes(request):    
    # Consulta de clientes
    clientes = Cliente.objects.filter(tecnico=request.user.id)
    return render(request, 'ascensor/MisClientes.html', {'clientes':clientes})

def formOrdenes(request):
    pk = request.GET.get('id','')
    idCliente = request.GET.get('idCliente','')
    datos = dict()
    if(pk!=''):
        # Editar
        form = OrdenForm(instance=get_object_or_404(Orden,pk=request.GET['id']))
        datos['formulario'] = render_to_string('ascensor/formularios/form_ordenes.html',context={'form':form,'idCliente':idCliente},request=request)
    else:
        # Nuevo
        form = OrdenForm()
        if(idCliente!=''):
            form.instance.cliente = get_object_or_404(Cliente,pk=idCliente)
        datos['formulario'] = render_to_string('ascensor/formularios/form_ordenes.html',context={'form':form,'idCliente':idCliente},request=request)
    return JsonResponse(datos)

@login_required
def misOrdenes(request):
    if request.method == 'POST':
        form = None
        if (request.POST['idOrden'] != "None"):
            instance = get_object_or_404(Orden,id=request.POST['idOrden'])
            form = OrdenForm(request.POST,instance=instance)
        else:
            form = OrdenForm(request.POST)
        if form.is_valid():
            idCliente = request.POST.get('idCliente','')
            if (idCliente!=''):
                form.instance.cliente = get_object_or_404(Cliente,pk=idCliente)
            form.instance.tecnico = get_object_or_404(Tecnico,pk=request.user.id)
            form.save()
            return HttpResponseRedirect('/ascensor/MisOrdenes.html?mensaje=exito')
    else:
        form = TecnicoForm()
    # Consulta de clientes
    ordenes = Orden.objects.filter(cliente__tecnico=request.user.id)
    return render(request, 'ascensor/MisOrdenes.html', {'form': form,'ordenes':ordenes})

@login_required
def eliminarOrdenes(request):
    pk = request.GET.get('id','')
    orden = get_object_or_404(Orden,pk=pk)
    orden.delete()
    return JsonResponse({"respuesta":"OK"})