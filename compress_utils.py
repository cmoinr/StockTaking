from PIL import Image
import io

# Tamaño máximo (ancho, alto) y calidad JPEG
MAX_SIZE = (800, 800)
JPEG_QUALITY = 80

def compress_image(file_storage):
    """
    Comprime y redimensiona una imagen recibida como FileStorage.
    Devuelve un objeto BytesIO listo para subir.
    """
    file_storage.stream.seek(0)  # Asegura que el puntero esté al inicio
    image = Image.open(file_storage)
    image.thumbnail(MAX_SIZE, Image.LANCZOS)
    output = io.BytesIO()
    # Convertir a JPEG para máxima compresión universal
    if image.mode in ("RGBA", "P"):
        image = image.convert("RGB")
    image.save(output, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    output.seek(0)
    return output
