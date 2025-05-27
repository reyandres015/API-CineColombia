from bson import ObjectId
from datetime import datetime
from template_method.Functions.CrearFuncionTemplate import CrearFuncionTemplate
from dependencies.database import db_client
from models.common import APIResponse


class CrearFuncionEstandar(CrearFuncionTemplate):
    def verificar_pelicula(self, data):
        # 1. Verificar que la película exista y obtener su fecha de estreno
        pelicula = db_client.local.movies.find_one(
            {
                "_id": ObjectId(data.pelicula_id),
            },
            {"_id": 1, "estreno": 1}
        )
        if not pelicula:
            raise APIResponse(
                code=400,
                status="error",
                message="La película no existe",
                data=None
            )

        return pelicula

    def verificar_sala(self, data):
        # 2. Verificar que la sala exista y esté disponible
        sala = db_client.local.rooms.find_one(
            {
                "_id": ObjectId(data.sala_id),
                "estado": {"$ne": "No Disponible"}
            },
            {"_id": 1, "capacidad": 1}
        )
        if not sala:
            raise APIResponse(
                code=400,
                status="error",
                message="Sala no encontrada o no disponible",
                data=None
            )
        return sala

    def validar_fecha(self, data, pelicula):
        # 3. Combinar fecha y hora en un solo datetime
        function_datetime = datetime.combine(
            data.fecha, data.hora)

        # 4. Validar que la función no sea antes del estreno de la película
        if pelicula["estreno"] > function_datetime.replace(tzinfo=None):
            raise APIResponse(
                code=400,
                status="error",
                message="La película aún no se ha estrenado en la fecha seleccionada",
                data=None
            )

        # 5. Validar que la función no sea en el pasado
        if function_datetime.replace(tzinfo=None) < datetime.now():
            raise APIResponse(
                code=400,
                status="error",
                message="La fecha u hora de la función no puede ser anterior a la hora actual en el día de hoy",
                data=None
            )
        return function_datetime

    def insertar_funcion(self, data, function_datetime, pelicula, sala):
        # 6. Crear nueva función y guardar en la base de datos
        new_function = {
            "pelicula_id": pelicula["_id"],
            "sala_id": sala["_id"],
            "fecha": function_datetime,
            "precio": data.precio,
            "sillas_disponibles": sala["capacidad"],
            "status": "En Venta"
        }

        result = db_client.local.functions.insert_one(new_function)

        if not result.acknowledged:
            raise APIResponse(
                code=500,
                status="error",
                message="Failed to create function",
                data=None
            )
        return str(result.inserted_id)
