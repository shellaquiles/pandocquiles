"""
uploader.py

Módulo responsable de recolectar los archivos compilados (.pdf, .html y .docx)
en el directorio configurado (OUTPUT_DIR) y enviarlos al webhook de Google Apps Script 
para su almacenamiento en Google Drive.

Agradecimiento especial a @m1gl0 por la contribución de este módulo.
"""
import glob
import json
import base64
import urllib.request
import os

def upload_to_drive():
    """
    Busca archivos generados en la carpeta configurada (OUTPUT_DIR) y los envía a Google Drive.
    Lee la URL del webhook desde la variable de entorno 'DRIVE_WEBHOOK_URL'.
    """
    # Asegurar que se ejecuta desde la raíz project-docs (estamos en src/python/)
    os.chdir(os.path.join(os.path.dirname(__file__), '..', '..'))

    webhook_url = os.environ.get("DRIVE_WEBHOOK_URL")

    if not webhook_url:
        print("⚠️ DRIVE_WEBHOOK_URL no está configurada en las variables de entorno. Omitiendo la subida a Google Drive.")
        return

    output_dir = os.environ.get("OUTPUT_DIR", "manuales")
    files_to_upload = []

    # Encontrar todos los PDFs generados en la carpeta configurada
    for pdf in glob.glob(f"{output_dir}/*.pdf"):
        files_to_upload.append(pdf)

    # Encontrar los HTML generados en la carpeta configurada
    for html_file in glob.glob(f"{output_dir}/*.html"):
        files_to_upload.append(html_file)

    # Encontrar los DOCX generados en la carpeta configurada
    for docx_file in glob.glob(f"{output_dir}/*.docx"):
        files_to_upload.append(docx_file)

    if not files_to_upload:
        print(f"No se encontraron archivos PDF, HTML o DOCX en '{output_dir}/' para subir.")
        exit(0)

    print(f"🚀 Iniciando subida de {len(files_to_upload)} archivos a Google Drive...")

    for filepath in files_to_upload:
        filename = os.path.basename(filepath)
        ext = os.path.splitext(filename)[1].lower()

        mime_type = "application/octet-stream"
        if ext == ".pdf":
            mime_type = "application/pdf"
        elif ext == ".html":
            mime_type = "text/html"
        elif ext == ".docx":
            mime_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

        print(f"Subiendo {filename}...")

        with open(filepath, "rb") as f:
            file_data = f.read()

        # Convertir a Base64
        base64_data = base64.b64encode(file_data).decode('utf-8')
        data_url = f"data:{mime_type};base64,{base64_data}"

        payload = {
            "filename": filename,
            "fileDataUrl": data_url
        }

        req = urllib.request.Request(webhook_url, method="POST")
        req.add_header('Content-Type', 'text/plain;charset=utf-8')
        data = json.dumps(payload).encode('utf-8')

        try:
            response = urllib.request.urlopen(req, data=data)
            res_body = response.read().decode('utf-8')
            try:
                res_json = json.loads(res_body)
                if res_json.get('status') == 'success':
                    print(f"✅ {filename} subido correctamente.")
                else:
                    print(f"❌ Error al subir {filename}: {res_json}")
            except:
                print(f"✅ Enviado {filename}, respuesta (No JSON): {res_body}")
        except Exception as e:
            print(f"❌ Error de red al subir {filename}: {e}")

    print("🎉 Sincronización con Drive finalizada.")

if __name__ == '__main__':
    upload_to_drive()
