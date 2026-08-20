"""
html_formatter.py

Módulo responsable de ajustar las imágenes codificadas en Base64 dentro
de los archivos HTML generados por Pandoc, limitando su ancho para
que se visualicen correctamente en Google Docs.
"""
import re
import base64
from io import BytesIO
import sys
import os
from PIL import Image

def fix_html_images(html_filepath: str):
    """
    Lee un archivo HTML, busca imágenes incrustadas en Base64, determina 
    su tamaño original y añade el atributo 'width=650' si exceden 
    dicho ancho, evitando que se desborden en la previsualización.
    
    También ajusta las etiquetas de <figcaption> para mejorar su formato.
    
    Args:
        html_filepath (str): Ruta absoluta o relativa al archivo HTML.
    """
    if not os.path.exists(html_filepath):
        print(f"Error: No se encontró el archivo HTML {html_filepath}")
        return

    with open(html_filepath, 'r') as f:
        html = f.read()

    def replace_img(match):
        img_tag = match.group(0)
        # Si ya tiene un ancho, no tocarla
        if 'width=' in img_tag: 
            return img_tag
        
        # Extraer base64
        src_match = re.search(r'src="data:image/([^;]+);base64,([^"]+)"', img_tag)
        if src_match:
            try:
                img_data = base64.b64decode(src_match.group(2))
                img = Image.open(BytesIO(img_data))
                if img.size[0] > 650:
                    return img_tag.replace('/>', ' width="650" />').replace('>', ' width="650">')
            except Exception as e:
                print(f"Aviso: No se pudo procesar imagen Base64: {e}")
        return img_tag

    # Remplazar etiquetas de imagen limitando el ancho
    new_html = re.sub(r'<img[^>]+>', replace_img, html)

    # Arreglo para que los captions de las imágenes no salgan en la misma línea y se vean mejor
    new_html = re.sub(
        r'<figcaption[^>]*>', 
        '<br><p style="text-align: center; font-style: italic; color: #666666; font-size: 14px; margin-top: 8px;">', 
        new_html
    )
    new_html = new_html.replace('</figcaption>', '</p><br>')

    # Guardar cambios
    with open(html_filepath, 'w') as f:
        f.write(new_html)
        
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python html_formatter.py <html_filepath>")
        sys.exit(1)
    fix_html_images(sys.argv[1])
