# ritmos/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

# Importar la lógica del autómata que acabamos de crear
from .automata_logic.mealy_machines import RockMealy, ReggaetonMealy, HipHopMealy
from .automata_logic.aceptador_machines import RockAceptador

# (Más adelante importaremos aquí RockAceptador, HipHopMealy, etc.)

class GenerateRhythmAPI(APIView):
    """
    API View para generar secuencias rítmicas usando
    el autómata de Mealy correspondiente al género.
    """
    
    def get(self, request, genre, measures):
        # 1. Seleccionar el autómata basado en la URL
        automata = None
        if genre.lower() == 'rock':
            automata = RockMealy()
        elif genre.lower() == 'reggaeton':  # <--- ¡ESTO ES LO QUE FALTA!
            automata = ReggaetonMealy()
        elif genre.lower() == 'hiphop':
            automata = HipHopMealy()

        if not automata:
            # Si el género no se encuentra, retornar un error 404
            return Response(
                {"error": f"Género '{genre}' no soportado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # 2. Calcular el número total de pasos (semicorcheas)
        # Asumimos 16 semicorcheas por compás (measure)
        try:
            num_pasos = int(measures) * 16
        except ValueError:
            return Response(
                {"error": "El número de compases (measures) debe ser un entero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Generar la secuencia llamando a nuestro método
        secuencia = automata.generar_secuencia(pasos=num_pasos)

        # 4. Retornar la secuencia como JSON
        return Response({
            "genre": genre,
            "measures": measures,
            "subdivisions_per_measure": 16,
            "sequence": secuencia
        })
class ClassifyRhythmAPI(APIView):
    def post(self, request):
        # Recibimos la secuencia del usuario
        # Esperamos un JSON: { "sequence": "B-H-C-H..." }
        sequence_str = request.data.get('sequence', '')
        
        if not sequence_str:
            return Response({"error": "Secuencia vacía"}, status=400)

        # Instanciamos el Aceptador
        afd_rock = RockAceptador()
        
        # Ejecutamos el análisis
        es_rock = afd_rock.analizar_cadena(sequence_str)
        
        # Resultado
        if es_rock:
            return Response({
                "input": sequence_str,
                "genre_detected": "Rock",
                "message": "¡Patrón de Rock reconocido!"
            })
        else:
             return Response({
                "input": sequence_str,
                "genre_detected": "Desconocido",
                "message": "No coincide con el patrón de Rock básico."
            })    
class AppView(APIView):
    """
    Sirve la aplicación principal de frontend (index.html).
    """
    def get(self, request):
        # 2. AÑADE ESTA VISTA
        # Django buscará automáticamente en 'ritmos/templates/ritmos/index.html'
        return render(request, 'ritmos/index.html')