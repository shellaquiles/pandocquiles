"""
compiler.py

Módulo responsable de unir múltiples archivos Markdown en un solo documento
y generar la portada junto con la configuración de impresión PDF (JSON).
"""
import glob
import re
import datetime
import os
import json
import sys
import unicodedata
from theme import get_current_theme, generate_css_variables

def slugify(text: str) -> str:
    """
    Convierte texto con caracteres especiales y acentos en un slug URL-safe compatible
    con las anclas generadas en los encabezados.
    """
    clean = re.sub(r'[`*\[\]:?.,/\\()\'"]', '', text)
    normalized = unicodedata.normalize('NFKD', clean).encode('ASCII', 'ignore').decode('utf-8')
    normalized = normalized.lower()
    slug = re.sub(r'[^a-z0-9]+', '-', normalized).strip('-')
    return slug

def compile_markdown(dir_path: str, doc_name: str, output_dir: str):
    """
    Lee los archivos Markdown del directorio especificado, los une,
    les agrega una portada oficial y crea la configuración del PDF.
    
    Args:
        dir_path (str): Ruta al directorio que contiene los .md.
        doc_name (str): Nombre del documento (ej. 'pandocquiles').
        output_dir (str): Directorio donde se guardarán los resultados.
    """
    os.makedirs(output_dir, exist_ok=True)
    theme = get_current_theme()
    
    # Buscar README y los demás capítulos (0*.md, 1*.md, etc.)
    files = []
    readme_path = os.path.join(dir_path, 'README.md')
    if os.path.exists(readme_path):
        files.append(readme_path)
        
    chapter_files = sorted(glob.glob(os.path.join(dir_path, '[0-9]*.md')))
    files.extend(chapter_files)
    
    if not files:
        print(f"No se encontraron archivos Markdown en {dir_path}")
        return

    out_file = os.path.join(output_dir, f'{doc_name}.md')

    with open(out_file, 'w', encoding='utf-8') as out:
        # Inyectar variables CSS de tema
        out.write(generate_css_variables())
        out.write('\n\n')

        # --- Generar Portada ---
        main_title = doc_name.replace('-', ' ').title()
        subtitle = os.environ.get('PDF_SUBTITLE', 'Documentación del Proyecto')
        
        # Intentar extraer el título real del README o frontmatter si existe
        if files and 'README.md' in files[0]:
            with open(files[0], 'r', encoding='utf-8') as readme:
                content_first = readme.read()
                # Extraer título de YAML frontmatter si existe
                m_title = re.search(r'^title:\s*\"([^\"]+)\"', content_first, re.MULTILINE)
                m_sub = re.search(r'^subtitle:\s*\"([^\"]+)\"', content_first, re.MULTILINE)
                if m_title:
                    main_title = m_title.group(1).strip()
                    if m_sub:
                        subtitle = m_sub.group(1).strip()
                else:
                    lines = content_first.split('\n')
                    if lines and lines[0].startswith('# '):
                        raw_title = lines[0][2:].strip()
                        if ' — ' in raw_title:
                            main_title, subtitle = raw_title.split(' — ', 1)
                        elif ' - ' in raw_title:
                            main_title, subtitle = raw_title.split(' - ', 1)
                        else:
                            main_title = raw_title
                            subtitle = os.environ.get('PDF_SUBTITLE', 'Documentación del Proyecto')

        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        fecha = f'{meses[datetime.datetime.now().month - 1]} {datetime.datetime.now().year}'
        pdf_top_header = os.environ.get('PDF_TOP_HEADER', os.environ.get('PDF_GOV_HEADER', 'Organización'))

        portada = f'''
<div style="text-align: center; padding-top: 80px; padding-bottom: 80px;">
  <p style="font-size: 14px; letter-spacing: 3px; font-weight: bold; color: {theme['primary']}; text-transform: uppercase;">{pdf_top_header}</p>
  <h1 style="font-size: 34px; margin-top: 20px; margin-bottom: 10px; color: #333333;">{main_title}</h1>
  <h3 style="font-size: 18px; font-weight: 300; color: #666666;">{subtitle}</h3>
  <div style="width: 80px; height: 4px; background-color: {theme['primary']}; margin: 30px auto;"></div>
  <p style="font-size: 13px; color: #888888;">Generado automáticamente · {fecha}</p>
</div>

'''
        out.write(portada)
        # ----------------------
        
        pdf_org_name = os.environ.get('PDF_ORG_NAME', 'Organización')
        pdf_opts = {
            "pdf_options": {
                "displayHeaderFooter": True,
                "headerTemplate": f"<div style='font-size: 8px; width: 100%; padding: 0 40px; display: flex; justify-content: space-between; font-family: Inter, sans-serif; color: {theme['primary']}; font-weight: bold; text-transform: uppercase; border-bottom: 1px solid #e2e8f0; margin-bottom: 10px; padding-bottom: 5px;'><span>{main_title}</span><span>{pdf_org_name}</span></div>",
                "footerTemplate": f"<div style='font-size: 8px; width: 100%; text-align: center; font-family: Inter, sans-serif; color: {theme['primary']}; font-weight: bold; text-transform: uppercase; border-top: 1px solid #e2e8f0; padding-top: 5px;'><span>{main_title} - {pdf_org_name} - PÁGINA <span class=\"pageNumber\"></span> DE <span class=\"totalPages\"></span></span></div>",
                "margin": { "top": "25mm", "bottom": "25mm", "left": "20mm", "right": "20mm" }
            }
        }
        
        with open(os.path.join(output_dir, 'pdf_config.json'), 'w', encoding='utf-8') as f_conf:
            json.dump(pdf_opts, f_conf)
            
        with open(os.path.join(output_dir, 'title.txt'), 'w', encoding='utf-8') as f_title:
            f_title.write(main_title)

        for file in files:
            with open(file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                
                # Sanitizar YAML frontmatter inicial si existe en archivos o capítulos
                content = re.sub(r'^---\s*\n.*?\n---\s*\n?', '', content, flags=re.DOTALL)

                # Si es el README, quitar el H1 principal porque ya lo pusimos en la portada
                if 'README.md' in file:
                    content = re.sub(r'^# .*\n', '', content)

                # Sustituir callouts estilo GitHub
                content = re.sub(r'\[!NOTE\]', '**NOTA:**', content)
                content = re.sub(r'\[!IMPORTANT\]', '**IMPORTANTE:**', content)
                content = re.sub(r'\[!WARNING\]', '**ADVERTENCIA:**', content)
                content = re.sub(r'\[!CAUTION\]', '**PRECAUCIÓN:**', content)
                content = re.sub(r'\[!TIP\]', '**CONSEJO:**', content)
                
                # Arreglar links internos entre capítulos con slugificación de fragmento
                content = re.sub(
                    r'\[([^\]]+)\]\(\.\/[0-9]+-[^#)]+\.md#([^)]+)\)',
                    lambda m: f'[{m.group(1)}](#{slugify(m.group(2))})',
                    content
                )
                content = re.sub(r'\[([^\]]+)\]\(\.\/[0-9]+-[^#)]+\.md\)', r'\1', content)
                content = re.sub(r'\[([^\]]+)\]\(README\.md\)', r'\1', content)
                
                # Arreglar rutas de imágenes (ej. ./assets/... -> ../$DIR/assets/...)
                content = re.sub(r'\]\(\./assets/', f'](../{dir_path}/assets/', content)
                content = re.sub(r'\]\(assets/', f'](../{dir_path}/assets/', content)
                content = re.sub(r'src="\./assets/', f'src="../{dir_path}/assets/', content)
                content = re.sub(r'src="assets/', f'src="../{dir_path}/assets/', content)
                
                # Arreglar cualquier otra imagen local (ej. image.png -> ../$DIR/image.png)
                content = re.sub(r'\]\((?:\./)?(?!http|#|/|\.\.)([^)]+\.(?:png|jpg|jpeg|gif|svg|webp))\)', rf'](../{dir_path}/\1)', content)
                content = re.sub(r'src="(?:\./)?(?!http|/|\.\.)([^"]+\.(?:png|jpg|jpeg|gif|svg|webp))"', rf'src="../{dir_path}/\1"', content)
                
                out.write(content.strip())
                out.write('\n\n')
                
if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Uso: python compiler.py <dir_path> <doc_name> <output_dir>")
        sys.exit(1)
    compile_markdown(sys.argv[1], sys.argv[2], sys.argv[3])


