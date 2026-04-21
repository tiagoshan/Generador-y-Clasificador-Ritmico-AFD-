from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView

from .automata_logic.mealy_machines import RockMealy, ReggaetonMealy, HipHopMealy, CumbiaMealy
from .automata_logic.aceptador_machines import (
    RockAceptador, ReggaetonAceptador, HipHopAceptador, CumbiaAceptador,
)

GENRE_MEALY = {
    'rock': RockMealy,
    'reggaeton': ReggaetonMealy,
    'hiphop': HipHopMealy,
    'cumbia': CumbiaMealy,
}

GENRE_ACEPTADOR = {
    'rock': RockAceptador,
    'reggaeton': ReggaetonAceptador,
    'hiphop': HipHopAceptador,
    'cumbia': CumbiaAceptador,
}

GENRE_MESSAGES = {
    'rock': '¡Patrón de Rock reconocido! (bombo-caja alternado)',
    'reggaeton': '¡Patrón de Reggaetón reconocido! (dembow)',
    'hiphop': '¡Patrón de Hip-Hop reconocido! (síncopa doble)',
    'cumbia': '¡Patrón de Cumbia reconocido! (bombo seco + contratiempo)',
}


class GenerateRhythmAPI(APIView):
    def get(self, request, genre, measures):
        genre_key = genre.lower()
        MealyClass = GENRE_MEALY.get(genre_key)

        if not MealyClass:
            return Response(
                {"error": f"Género '{genre}' no soportado. Válidos: {', '.join(GENRE_MEALY)}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not (1 <= measures <= 32):
            return Response(
                {"error": "El número de compases debe estar entre 1 y 32."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        secuencia = MealyClass().generar_secuencia(pasos=measures * 16)
        return Response({
            "genre": genre_key,
            "measures": measures,
            "subdivisions_per_measure": 16,
            "sequence": secuencia,
        })


class ClassifyRhythmAPI(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        sequence = request.data.get('sequence', '')
        genre_hint = request.data.get('genre', '').lower()

        if not sequence:
            return Response({"error": "Secuencia vacía."}, status=status.HTTP_400_BAD_REQUEST)

        genres_to_check = (
            [genre_hint] if genre_hint in GENRE_ACEPTADOR else list(GENRE_ACEPTADOR)
        )

        results = {g: GENRE_ACEPTADOR[g]().analizar_cadena(sequence) for g in genres_to_check}
        detected = [g for g, match in results.items() if match]

        if len(detected) == 1:
            message = GENRE_MESSAGES[detected[0]]
            genre_detected = detected[0]
        elif detected:
            message = "Múltiples patrones detectados."
            genre_detected = detected
        else:
            message = "No coincide con ningún patrón conocido."
            genre_detected = "Desconocido"

        return Response({
            "results": results,
            "genre_detected": genre_detected,
            "message": message,
        })


class AppView(TemplateView):
    template_name = 'ritmos/index.html'
