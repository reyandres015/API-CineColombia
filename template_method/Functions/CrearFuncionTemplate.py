class CrearFuncionTemplate:
    """
    Clase base abstracta que define el método plantilla para crear una función de película.
    Las subclases deben implementar los pasos específicos para verificar la película, la sala,
    validar la fecha e insertar la función.

    Métodos
    -------
    crear_funcion(data):
        Método plantilla que orquesta la creación de una función llamando los pasos de verificación e inserción.

    verificar_pelicula(data):
        Método abstracto para verificar si la película existe o es válida. Debe ser implementado por las subclases.

    verificar_sala(data):
        Método abstracto para verificar si la sala está disponible o es válida. Debe ser implementado por las subclases.

    validar_fecha(data):
        Método abstracto para validar la fecha de la función. Debe ser implementado por las subclases.

    insertar_funcion(data):
        Método abstracto para insertar la función en el sistema. Debe ser implementado por las subclases.
    """

    def crear_funcion(self, data):
        pelicula = self.verificar_pelicula(data)
        sala = self.verificar_sala(data)
        function_datetime = self.validar_fecha(data, pelicula)
        return self.insertar_funcion(data, function_datetime, pelicula, sala)

    def verificar_pelicula(self, data): raise NotImplementedError
    def verificar_sala(self, data): raise NotImplementedError
    def validar_fecha(self, data): raise NotImplementedError

    def insertar_funcion(self, data, function_datetime,
                         pelicula, sala): raise NotImplementedError
