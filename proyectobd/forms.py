from django import forms
from .models import Reservacion, Sala, Requerimiento


class ReservacionForm(forms.ModelForm):
    class Meta:
        model = Reservacion
        fields = [
            'nombre_registra',
            'nombre_evento',
            'fecha_evento',
            'hora_inicio',
            'hora_fin',
            'asistentes',
            'salas',
            'requerimientos',
            'observaciones',
        ]
        widgets = {
            'nombre_registra': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de quien registra',
            }),
            'nombre_evento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del evento',
            }),
            'fecha_evento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'hora_inicio': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'hora_fin': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
            }),
            'asistentes': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
            }),
            'salas': forms.CheckboxSelectMultiple(),
            'requerimientos': forms.CheckboxSelectMultiple(),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales',
            }),
        }
        labels = {
            'nombre_registra': 'Nombre de quien registra',
            'nombre_evento': 'Nombre del evento',
            'fecha_evento': 'Fecha del evento',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
            'asistentes': 'Número de asistentes',
            'salas': 'Salas solicitadas',
            'requerimientos': 'Requerimientos',
            'observaciones': 'Observaciones',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['salas'].queryset = Sala.objects.filter(activa=True).order_by('orden')
        self.fields['requerimientos'].queryset = Requerimiento.objects.order_by('nombre')
        self.fields['requerimientos'].required = False
        self.fields['observaciones'].required = False

    def clean(self):
        cleaned_data = super().clean()
        fecha_evento = cleaned_data.get('fecha_evento')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')
        asistentes = cleaned_data.get('asistentes')
        salas = cleaned_data.get('salas')

        if hora_inicio and hora_fin and hora_fin <= hora_inicio:
            raise forms.ValidationError('La hora de fin debe ser posterior a la hora de inicio.')

        if asistentes and salas:
            capacidad_total = sum(sala.capacidad for sala in salas)

            if capacidad_total < asistentes:
                raise forms.ValidationError(
                    f'La capacidad de las salas seleccionadas es insuficiente. '
                    f'Capacidad total: {capacidad_total}. '
                    f'Asistentes registrados: {asistentes}. '
                    f'Selecciona más salas o una sala con mayor capacidad.'
                )

        if fecha_evento and hora_inicio and hora_fin and salas:
            reservaciones_empalmadas = Reservacion.objects.filter(
                fecha_evento=fecha_evento,
                estatus__in=['PENDIENTE', 'CONFIRMADA'],
                salas__in=salas,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio,
            ).distinct()

            if self.instance and self.instance.pk:
                reservaciones_empalmadas = reservaciones_empalmadas.exclude(pk=self.instance.pk)

            if reservaciones_empalmadas.exists():
                salas_ocupadas = []

                for reservacion in reservaciones_empalmadas:
                    for sala in reservacion.salas.filter(id__in=salas):
                        salas_ocupadas.append(sala.nombre)

                salas_ocupadas = sorted(set(salas_ocupadas))

                raise forms.ValidationError(
                    f'No se puede hacer la reservación. '
                    f'Las siguientes salas ya están ocupadas en ese horario: '
                    f'{", ".join(salas_ocupadas)}.'
                )

        return cleaned_data
