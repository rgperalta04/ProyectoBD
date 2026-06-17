from django.shortcuts import render, redirect, get_object_or_404
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

@login_required
def detalle_reservacion(request, reservacion_id):
    reservacion = get_object_or_404(Reservacion, id=reservacion_id)

    return render(request, 'proyectobd/detalle_reservacion.html', {
        'reservacion': reservacion
    })

@login_required
def confirmar_reservacion(request, reservacion_id):
    reservacion = get_object_or_404(Reservacion, id=reservacion_id)

    if request.method == 'POST':
        reservacion.estatus = 'CONFIRMADA'
        reservacion.save()

        HistorialReservacion.objects.create(
            reservacion=reservacion,
            usuario=request.user,
            accion='CONFIRMACION',
            descripcion='Reservación confirmada.'
        )

        messages.success(request, 'La reservación fue confirmada correctamente.')

    return redirect('detalle_reservacion', reservacion_id=reservacion.id)


@login_required
def cancelar_reservacion(request, reservacion_id):
    reservacion = get_object_or_404(Reservacion, id=reservacion_id)

    if request.method == 'POST':
        reservacion.estatus = 'CANCELADA'
        reservacion.save()

        HistorialReservacion.objects.create(
            reservacion=reservacion,
            usuario=request.user,
            accion='CANCELACION',
            descripcion='Reservación cancelada.'
        )

        messages.success(request, 'La reservación fue cancelada correctamente.')

    return redirect('detalle_reservacion', reservacion_id=reservacion.id)


@login_required
def finalizar_reservacion(request, reservacion_id):
    reservacion = get_object_or_404(Reservacion, id=reservacion_id)

    if request.method == 'POST':
        reservacion.estatus = 'FINALIZADA'
        reservacion.save()

        HistorialReservacion.objects.create(
            reservacion=reservacion,
            usuario=request.user,
            accion='FINALIZACION',
            descripcion='Reservación finalizada.'
        )

        messages.success(request, 'La reservación fue finalizada correctamente.')

    return redirect('detalle_reservacion', reservacion_id=reservacion.id)

@login_required
def editar_reservacion(request, reservacion_id):
    reservacion = get_object_or_404(Reservacion, id=reservacion_id)

    if request.method == 'POST':
        form = ReservacionForm(request.POST, instance=reservacion)

        if form.is_valid():
            reservacion = form.save()

            HistorialReservacion.objects.create(
                reservacion=reservacion,
                usuario=request.user,
                accion='EDICION',
                descripcion='Reservación editada por el administrador.'
            )

            messages.success(request, 'La reservación fue actualizada correctamente.')
            return redirect('detalle_reservacion', reservacion_id=reservacion.id)
    else:
        form = ReservacionForm(instance=reservacion)

    return render(request, 'proyectobd/editar_reservacion.html', {
        'form': form,
        'reservacion': reservacion
    })