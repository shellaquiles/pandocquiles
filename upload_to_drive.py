import glob
import json
import base64
import urllib.request
import os

# Asegurar que se ejecuta desde la raíz project-docs
os.chdir(os.path.join(os.path.dirname(__file__), '..'))

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbyFnLHLm-q_eYETr1uRFdQJSD-2cKmgz4uLPbbeCexE6bghK_4fmSX8rHQ5IFLvMuGNww/exec"

files_to_upload = []

# Encontrar todos los PDFs generados en la carpeta manuales
for pdf in glob.glob("manuales/*.pdf"):
    files_to_upload.append(pdf)

# Encontrar los HTML generados en la carpeta manuales
for html_file in glob.glob("manuales/*.html"):
    files_to_upload.append(html_file)

if not files_to_upload:
    print("No se encontraron archivos PDF o HTML en 'manuales/' para subir.")
    exit()

print(f"🚀 Iniciando subida de {len(files_to_upload)} archivos a Google Drive...")

for filepath in files_to_upload:
    filename = os.path.basename(filepath)
    ext = os.path.splitext(filename)[1].lower()

    mime_type = "application/octet-stream"
    if ext == ".pdf":
        mime_type = "application/pdf"
    elif ext == ".html":
        mime_type = "text/html"

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

    req = urllib.request.Request(WEBHOOK_URL, method="POST")
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
