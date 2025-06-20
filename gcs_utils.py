import os
import json
from google.cloud import storage
from werkzeug.utils import secure_filename

GCS_BUCKET = os.environ.get('GCS_BUCKET')
GCS_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# Permite usar la clave como archivo o como JSON (para Render)
if GCS_CREDENTIALS and os.path.exists(GCS_CREDENTIALS):
    client = storage.Client.from_service_account_json(GCS_CREDENTIALS)
elif GCS_CREDENTIALS:
    # Se asume que es el JSON de la clave
    info = json.loads(GCS_CREDENTIALS)
    client = storage.Client.from_service_account_info(info)
else:
    raise RuntimeError('No se encontró la configuración de Google Cloud Storage')

bucket = client.bucket(GCS_BUCKET)

def upload_file_to_gcs(file_storage, folder='uploads', force_jpeg=False):
    filename = secure_filename(file_storage.filename)
    if force_jpeg:
        # Cambiar extensión a .jpg
        filename = os.path.splitext(filename)[0] + '.jpg'
    blob = bucket.blob(f'{folder}/{filename}')
    blob.upload_from_file(file_storage, content_type='image/jpeg' if force_jpeg else file_storage.content_type)
    return blob.public_url

def delete_file_from_gcs(filename, folder='uploads'):
    blob = bucket.blob(f'{folder}/{filename}')
    blob.delete()
