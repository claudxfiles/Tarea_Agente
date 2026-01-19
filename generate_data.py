import os

DOCS_DIR = "data/documents"
os.makedirs(DOCS_DIR, exist_ok=True)

topics = [
    ("Ley de Aranceles Interestelares 2045", "Establece un impuesto del 5% sobre todas las importaciones de dilitio."),
    ("Protocolos de Seguridad de Motor Warp", "Periodos de enfriamiento obligatorios para motores Clase-V."),
    ("Cuarentena de Flora Alienigena", "Prohíbe el transporte de plantas sintientes del Sector 7."),
    ("Enmienda de Derechos de Droides", "Otorga ciudadanía básica a unidades IA que pasen el test de Turing-V."),
    ("Intercambio de Creditos Galacticos", "Tipo de cambio fijo entre Créditos y Latinum."),
    ("Licencias de Mineria de Asteroides", "Requiere permiso A-99 para cinturones no regulados."),
    ("Leyes Laborales de Gravedad Cero", "Turnos máximos de 6 horas en entornos de gravedad cero."),
    ("Codigo de Etica de Teletransportacion", "Prohíbe el transporte de materia orgánica viva sin consentimiento."),
    ("Prohibicion de Armas de Plasma", "Prohíbe la posesión civil de armas de fuego basadas en plasma."),
    ("Estandar de Comunicaciones de Espacio Profundo", "Estandariza frecuencias subespaciales a 45.2MHz."),
    ("Ley de Colonizacion de Exoplanetas", "Protección de biodiversidad para mundos habitables verificados."),
    ("Mandato de Seguro de Naves Estelares", "Toda nave más rápida que la luz debe tener cobertura de casco."),
    ("Restricciones de Publicidad Holografica", "Prohíbe anuncios intrusivos en vías espaciales públicas."),
    ("Especificacion de Traductor Universal", "Actualiza matriz de lenguaje para dialectos Klingon."),
    ("Limpieza de Basura Espacial", "Multas por arrojar desechos en rutas de navegación."),
    ("Prohibicion de Viajes en el Tiempo", "Prohibición estricta de dispositivos de desplazamiento temporal."),
    ("Proteccion de Identidad de Clones", "Los clones comparten derechos genéticos con los donantes."),
    ("Zonificacion de Esferas de Dyson", "Restringe mega-estructuras alrededor de estrellas habitadas."),
    ("Estandares de Encriptacion Cuantica", "Claves mínimas de 4096-qubits para comunicaciones gubernamentales."),
    ("Conservacion de Ballenas del Vacio", "Estatus protegido para Leviatanes espaciales.")
]

for i, (title, content) in enumerate(topics):
    filename = f"doc_{i+1:02d}_{title.replace(' ', '_')}.txt"
    path = os.path.join(DOCS_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(f"Título: {title}\n")
        f.write(f"ID: DOC-{i+1:03d}\n")
        f.write(f"Categoría: Regulación\n\n")
        f.write(f"{content}\n")
        f.write("Esta regulación es aplicada por el Consejo de la Federación Galáctica.\n")
        f.write("El incumplimiento resulta en sanciones nivel 4.\n")
        
print(f"Generados {len(topics)} documentos en {DOCS_DIR}")
