from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ReservacionForm
from .models import Reservacion, HistorialReservacion


@login_required
def crear_reservacion(request):
    if request.method == 'POST':
        form = ReservacionForm(request.POST)

        if form.is_valid():
            reservacion = form.save(commit=False)
            reservacion.usuario = request.user
            reservacion.estatus = 'PENDIENTE'
            reservacion.save()
            form.save_m2m()

            HistorialReservacion.objects.create(
                reservacion=reservacion,
                usuario=request.user,
                accion='CREACION',
                descripcion='Reservación creada por el usuario.'
            )

            messages.success(request, 'La reservación se registró correctamente.')
            return redirect('lista_reservaciones')
    else:
        form = ReservacionForm()

    return render(request, 'proyectobd/crear_reservacion.html', {
        'form': form
    })


@login_required
def lista_reservaciones(request):
    reservaciones = Reservacion.objects.all().order_by('-fecha_evento', '-hora_inicio')

    return render(request, 'proyectobd/lista_reservaciones.html', {
        'reservaciones': reservaciones
    })
