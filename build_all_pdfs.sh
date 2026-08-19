#!/bin/bash

# ==============================================================================
# Script de Construcción Universal: Generador de PDFs y MDs
# ==============================================================================

set -e

# Asegurar que se ejecuta en la raíz de project-docs
cd "$(dirname "$0")/.."

for DIR in manual-*/; do
    MANUAL_NAME="${DIR%/}"
    
    if ls $DIR/0*.md 1> /dev/null 2>&1; then
        echo "============================================================"
        echo "📘 Construyendo: $MANUAL_NAME"
        echo "============================================================"
        
        # 1. Unir capítulos en el archivo MD final dentro de 'manuales/'
        python3 -c "
import glob
import re
import datetime

files = glob.glob('$DIR/README.md') + sorted(glob.glob('$DIR/0*.md'))
out_file = 'manuales/$MANUAL_NAME.md'

with open(out_file, 'w') as out:
    # --- Generar Portada ---
    main_title = '$MANUAL_NAME'.replace('-', ' ').title()
    subtitle = 'Plataforma de Transparencia CDMX'
    
    # Intentar extraer el título real del README
    if files and 'README.md' in files[0]:
        with open(files[0], 'r') as readme:
            first_line = readme.readline().strip()
            if first_line.startswith('# '):
                raw_title = first_line[2:]
                if ' — ' in raw_title:
                    main_title, subtitle = raw_title.split(' — ', 1)
                elif ' - ' in raw_title:
                    main_title, subtitle = raw_title.split(' - ', 1)
                else:
                    main_title = raw_title
                    subtitle = 'Plataforma de Transparencia CDMX'

    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
    fecha = f'{meses[datetime.datetime.now().month - 1]} {datetime.datetime.now().year}'

    portada = f'''
<div style=\"text-align: center; padding-top: 80px; padding-bottom: 80px;\">
  <p style=\"font-size: 14px; letter-spacing: 3px; font-weight: bold; color: #9D2449; text-transform: uppercase;\">Gobierno de la Ciudad de México</p>
  <h1 style=\"font-size: 34px; margin-top: 20px; margin-bottom: 10px; color: #333333;\">{main_title}</h1>
  <h3 style=\"font-size: 18px; font-weight: 300; color: #666666;\">{subtitle}</h3>
  <div style=\"width: 80px; height: 4px; background-color: #9D2449; margin: 30px auto;\"></div>
  <p style=\"font-size: 13px; color: #888888;\">Generado automáticamente · {fecha}</p>
</div>

<div style=\"page-break-after: always;\"></div>

'''
    out.write(portada)
    # ----------------------
    
    import json
    pdf_opts = {
        \"pdf_options\": {
            \"displayHeaderFooter\": True,
            \"headerTemplate\": f\"<div style='font-size: 8px; width: 100%; padding: 0 40px; display: flex; justify-content: space-between; font-family: Inter, sans-serif; color: #9D2449; font-weight: bold; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; margin-bottom: 10px; padding-bottom: 5px;'><span>{main_title}</span><span>TRANSPARENCIA CDMX</span></div>\",
            \"footerTemplate\": f\"<div style='font-size: 8px; width: 100%; text-align: center; font-family: Inter, sans-serif; color: #9D2449; font-weight: bold; text-transform: uppercase; border-top: 1px solid #e2e8f0; padding-top: 5px;'><span>{main_title} - TRANSPARENCIA CDMX - PÁGINA <span class=\\\"pageNumber\\\"></span> DE <span class=\\\"totalPages\\\"></span></span></div>\",
            \"margin\": { \"top\": \"25mm\", \"bottom\": \"25mm\", \"left\": \"20mm\", \"right\": \"20mm\" }
        }
    }
    with open('manuales/pdf_config.json', 'w') as f_conf:
        json.dump(pdf_opts, f_conf)
        
    with open('manuales/title.txt', 'w') as f_title:
        f_title.write(main_title)

    for file in files:
        with open(file, 'r') as infile:
            content = infile.read()
            # Si es el README, quitar el H1 principal porque ya lo pusimos en la portada
            if 'README.md' in file:
                content = re.sub(r'^# .*\n', '', content)

            content = re.sub(r'\[!NOTE\]', '**NOTA:**', content)
            content = re.sub(r'\[!IMPORTANT\]', '**IMPORTANTE:**', content)
            content = re.sub(r'\[!WARNING\]', '**ADVERTENCIA:**', content)
            content = re.sub(r'\[!CAUTION\]', '**PRECAUCIÓN:**', content)
            content = re.sub(r'\[!TIP\]', '**CONSEJO:**', content)
            
            # Arreglar links internos entre capítulos
            content = re.sub(r'\]\(\./[0-9]{2}-[^#)]+\.md#([^)]+)\)', r'](#\1)', content)
            content = re.sub(r'\]\(\./[0-9]{2}-[^#)]+\.md\)', r'](#)', content)
            
            # Arreglar rutas de imágenes (ej. ./assets/... -> ../$DIR/assets/...)
            content = re.sub(r'\]\(\./assets/', r'](../$DIR/assets/', content)
            content = re.sub(r'\]\(assets/', r'](../$DIR/assets/', content)
            content = re.sub(r'src=\"\./assets/', r'src=\"../$DIR/assets/', content)
            content = re.sub(r'src=\"assets/', r'src=\"../$DIR/assets/', content)
            
            # Arreglar cualquier otra imagen local (ej. image.png -> ../$DIR/image.png)
            content = re.sub(r'\]\((?:\./)?(?!http|#|/|\.\.)([^)]+\.(?:png|jpg|jpeg|gif|svg|webp))\)', r'](../$DIR\1)', content)
            content = re.sub(r'src=\"(?:\./)?(?!http|/|\.\.)([^\"]+\.(?:png|jpg|jpeg|gif|svg|webp))\"', r'src=\"../$DIR\1\"', content)
            
            out.write(content)
            out.write('\n\n<div style=\"page-break-after: always;\"></div>\n\n')
"
        
        # 2. Renderizar Mermaid a PNG (Google Docs no acepta SVG)
        echo "🎨 Renderizando diagramas Mermaid..."
        npx -y @mermaid-js/mermaid-cli -i manuales/$MANUAL_NAME.md -o manuales/MANUAL_MERMAID.md -e png -s 2 -b white
        
        # 3. Preparar archivo PDF inyectando CSS
        python3 -c "
with open('manuales/MANUAL_MERMAID.md', 'r') as f:
    content = f.read()

css_fix = '''<style>
/* Fixes Imágenes y Mermaid */
img, .mermaid svg, pre.mermaid svg, div.mermaid svg {
    max-width: 100% !important;
    height: auto !important;
    page-break-inside: avoid;
    margin: 20px auto;
    display: block;
}
table { page-break-inside: avoid; }
</style>
'''
with open('manuales/MANUAL_PDF.md', 'w') as f:
    f.write(css_fix + '\n' + content)
"
        
        # 4. Construir HTML (para Google Docs) con imágenes incrustadas en Base64
        echo "🌐 Construyendo HTML con recursos embebidos..."
        pandoc manuales/MANUAL_MERMAID.md -o manuales/$MANUAL_NAME.html --self-contained --css=utils/theme-gdocs.css --resource-path=$DIR:.:manuales

        python3 -c "
import re
import base64
from io import BytesIO
from PIL import Image

filename = 'manuales/$MANUAL_NAME.html'
with open(filename, 'r') as f:
    html = f.read()

def replace_img(match):
    img_tag = match.group(0)
    if 'width=' in img_tag: return img_tag
    
    src_match = re.search(r'src=\"data:image/([^;]+);base64,([^\"]+)\"', img_tag)
    if src_match:
        try:
            img = Image.open(BytesIO(base64.b64decode(src_match.group(2))))
            if img.size[0] > 650:
                return img_tag.replace('/>', ' width=\"650\" />').replace('>', ' width=\"650\">')
        except: pass
    return img_tag

new_html = re.sub(r'<img[^>]+>', replace_img, html)

# Arreglo para que los captions de las imágenes no salgan en la misma línea
new_html = re.sub(r'<figcaption[^>]*>', '<br><p style=\"text-align: center; font-style: italic; color: #666666; font-size: 14px; margin-top: 8px;\">', new_html)
new_html = new_html.replace('</figcaption>', '</p><br>')

with open(filename, 'w') as f:
    f.write(new_html)
"

        # 5. Construir PDF usando theme-pdf.css de la carpeta utils/
        echo "📄 Compilando PDF final ($MANUAL_NAME.pdf)..."
        npx -y md-to-pdf manuales/MANUAL_PDF.md --stylesheet utils/theme-pdf.css --config-file manuales/pdf_config.json
        
        # Reescribir metadatos del PDF
        if [ -f manuales/title.txt ]; then
            MAIN_TITLE=$(cat manuales/title.txt)
            echo "📝 Escribiendo metadatos PDF oficiales..."
            exiftool -Title="$MAIN_TITLE" \
                     -Author="Gobierno de la Ciudad de México" \
                     -Creator="Gobierno de la Ciudad de México" \
                     -Producer="Plataforma de Transparencia" \
                     -overwrite_original manuales/MANUAL_PDF.pdf
            rm manuales/title.txt
        fi
        
        # 6. Mover y limpiar dentro de manuales/
        mv manuales/MANUAL_PDF.pdf manuales/$MANUAL_NAME.pdf
        rm manuales/MANUAL_MERMAID.md manuales/MANUAL_PDF.md manuales/MANUAL_MERMAID-*.png 2>/dev/null || true
        
        echo "✅ Completado: manuales/$MANUAL_NAME.html y manuales/$MANUAL_NAME.pdf"
    fi
done

echo "☁️ Sincronizando resultados con Google Drive..."
python3 utils/upload_to_drive.py

echo "🎉 ¡Todos los manuales han sido actualizados y subidos con éxito!"
