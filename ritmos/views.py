from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render

from .automata_logic.mealy_machines import RockMealy, ReggaetonMealy, HipHopMealy, CumbiaMealy
from .automata_logic.aceptador_machines import RockAceptador

class GenerateRhythmAPI(APIView):
    
    # API View para generar secuencias rítmicas usando el autómata de Mealy correspondiente al género.
    
    
    def get(self, request, genre, measures):
        # selecciona el autómata basado en la URL
        automata = None
        if genre.lower() == 'rock':
            automata = RockMealy()
        elif genre.lower() == 'reggaeton':
            automata = ReggaetonMealy()
        elif genre.lower() == 'hiphop':
            automata = HipHopMealy()
        elif genre.lower() == 'cumbia':
            automata = CumbiaMealy()

        if not automata:
            # Si el género no se encuentra, retornar un error 404
            return Response(
                {"error": f"Género '{genre}' no soportado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # asumimos 16 semicorcheas por compás (measure)
        try:
            num_pasos = int(measures) * 16
        except ValueError:
            return Response(
                {"error": "El número de compases (measures) debe ser un entero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # generar la secuencia llamando a nuestro método
        secuencia = automata.generar_secuencia(pasos=num_pasos)

        # retornar la secuencia como JSON
        return Response({
            "genre": genre,
            "measures": measures,
            "subdivisions_per_measure": 16,
            "sequence": secuencia
        })
class ClassifyRhythmAPI(APIView):
    def post(self, request):
        # recibe la secuencia del usuario
        sequence_str = request.data.get('sequence', '')
        
        if not sequence_str:
            return Response({"error": "Secuencia vacía"}, status=400)

        # aceptador
        afd_rock = RockAceptador()
        
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

    def get(self, request):
        return render(request, 'ritmos/index.html')