from dataclasses import dataclass


@dataclass
class Contacto:
    id: int
    nombre: str
    telefono: str
    correo: str
    ciudad: str
