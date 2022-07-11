from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from gestionPedidos.models import Articulos
from gestionPedidos.forms import FormularioContacto

# Create your views here.

def busqueda_productos (request):

    return render (request, "busqueda_productos.html")

def buscar (request):

    if request.GET["prd"]:

        #mensaje="Articulo buscado: %r" %request.GET["prd"]

        producto=request.GET["prd"]

        if len(producto)>20:

            mensaje="Texto de busqueda demasiado largo"

        else:
                
            articulos=Articulos.objects.filter(nombre__icontains=producto)

            return render (request, "resultados_busqueda.html", {"articulos":articulos, "query":producto})

    else:

        mensaje="No has introducido nada"

    return HttpResponse(mensaje)

def contacto(request):

    if request.method=="POST":

    # ----codigo necesario para obtener la informacón que se agregó en el formulario y completar el envío del email---

    #     subject=request.POST["asunto"]

    #     message=request.POST["mensaje"] + " " + request.POST["email"]

    #     email_from=settings.EMAIL_HOST_USER

    #     recipient_list=["crosio.fernando@gmail.com"]

    #     send_mail(subject, message, email_from, recipient_list)

    #     return render(request, "gracias.html")

    # return render(request, "contacto.html")

    #------codigo necesario en caso que para obtener los datos del formulario se haga uso de la API forms,
    # para ello es necesario importar "from gestionPedidos.forms import FormularioContacto" haciendo uso de la clase
    # FormularioContacto en el archivo forms.py.

        miFormulario=FormularioContacto(request.POST)    #se coloca request.POST como parametro de la instancia de clase FormularioContacto
                                                         # de manera de obtener los datos que viajan desde el formulario contacto.html

        if miFormulario.is_valid():     # is_valid() devuelve True en caso de que la informacion del formulario
                                        #  del template "contacto" este validada)

            infForm=miFormulario.cleaned_data    # cleaned_data devuelve un diccionario con la información
                                                   # que se agregó en el formulario

            send_mail(infForm['asunto'], infForm['mensaje'], settings.EMAIL_HOST_USER, ['crosio.fernando@gmail.com'],)

            return render (request, "gracias.html")

    else:

        miFormulario=FormularioContacto()

    return render(request, "formulario_contacto.html", {"form":miFormulario})
