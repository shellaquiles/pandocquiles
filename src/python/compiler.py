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
import base64
import mimetypes
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
    
    # Estrategia genérica de detección de archivos Markdown:
    # 1. Si existe un manual consolidado maestro (*_COMPLETO.md, *_MASTER.md, *_BOOK.md)
    master_candidates = sorted(
        glob.glob(os.path.join(dir_path, '*[Cc][Oo][Mm][Pp][Ll][Ee][Tt][Oo]*.md')) +
        glob.glob(os.path.join(dir_path, '*[Mm][Aa][Ss][Tt][Ee][Rr]*.md')) +
        glob.glob(os.path.join(dir_path, '*[Bb][Oo][Oo][Kk]*.md'))
    )
    if master_candidates:
        files = [master_candidates[0]]
    else:
        files = []
        readme_path = os.path.join(dir_path, 'README.md')
        if os.path.exists(readme_path):
            files.append(readme_path)
            
        chapter_files = sorted(glob.glob(os.path.join(dir_path, '[0-9]*.md')))
        if chapter_files:
            files.extend(chapter_files)
        elif not files:
            files = sorted(glob.glob(os.path.join(dir_path, '*.md')))
    
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
        
        # Intentar extraer el título real del primer archivo
        if files:
            with open(files[0], 'r', encoding='utf-8') as f_first:
                content_first = f_first.read()
                # Extraer título de YAML frontmatter si existe
                m_title = re.search(r'^title:\s*\"([^\"]+)\"', content_first, re.MULTILINE)
                m_sub = re.search(r'^subtitle:\s*\"([^\"]+)\"', content_first, re.MULTILINE)
                if m_title:
                    main_title = m_title.group(1).strip()
                    if m_sub:
                        subtitle = m_sub.group(1).strip()
                else:
                    lines = content_first.split('\n')
                    for l in lines:
                        if l.startswith('# '):
                            raw_title = l[2:].strip()
                            if ' — ' in raw_title:
                                main_title, subtitle = raw_title.split(' — ', 1)
                            elif ' - ' in raw_title:
                                main_title, subtitle = raw_title.split(' - ', 1)
                            else:
                                main_title = raw_title
                                subtitle = os.environ.get('PDF_SUBTITLE', 'Documentación del Proyecto')
                            break

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

                # Si es el README o Manual Maestro consolidado, quitar el H1 principal porque ya lo pusimos en la portada
                if 'README.md' in file or (master_candidates and file in master_candidates):
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
                
                # Calcular ruta relativa desde output_dir hacia dir_path para imágenes
                rel_assets = os.path.relpath(os.path.abspath(dir_path), os.path.abspath(output_dir))
                
                # Arreglar cualquier imagen local (ej. img/test.png -> ../../documentacion/img/test.png)
                content = re.sub(r'\]\((?:\./)?(?!http|#|/|\.\.)([^)]+\.(?:png|jpg|jpeg|gif|svg|webp))\)', rf']({rel_assets}/\1)', content)
                content = re.sub(r'src="(?:\./)?(?!http|/|\.\.)([^"]+\.(?:png|jpg|jpeg|gif|svg|webp))"', rf'src="{rel_assets}/\1"', content)
                
                out.write(content.strip())
                out.write('\n\n')
                
def embed_images_in_markdown(md_path: str, search_dirs: list):
    """
    Convierte todas las rutas de imágenes en un archivo Markdown a datos Base64
    incrustados directamente (data:image/png;base64,...), garantizando que
    md-to-pdf y los motores de PDF las rendericen sin fallos de rutas relativas.
    """
    if not os.path.exists(md_path):
        return
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()

    import mimetypes

    def repl_md(match):
        alt = match.group(1)
        src = match.group(2).strip()
        if src.startswith('data:') or src.startswith('http://') or src.startswith('https://'):
            return match.group(0)

        found_file = None
        for sdir in search_dirs:
            candidate = os.path.join(sdir, src)
            if os.path.isfile(candidate):
                found_file = candidate
                break
            clean_name = os.path.basename(src)
            for root, _, files in os.walk(sdir):
                if clean_name in files:
                    found_file = os.path.join(root, clean_name)
                    break
            if found_file:
                break

        if found_file and os.path.exists(found_file):
            mime, _ = mimetypes.guess_type(found_file)
            if not mime:
                mime = 'image/png'
            with open(found_file, 'rb') as img_f:
                b64 = base64.b64encode(img_f.read()).decode('ascii')
            return f'![{alt}](data:{mime};base64,{b64})'
        return match.group(0)

    new_text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', repl_md, text)

    def repl_html(match):
        prefix = match.group(1)
        src = match.group(2).strip()
        suffix = match.group(3)
        if src.startswith('data:') or src.startswith('http://') or src.startswith('https://'):
            return match.group(0)
        found_file = None
        for sdir in search_dirs:
            candidate = os.path.join(sdir, src)
            if os.path.isfile(candidate):
                found_file = candidate
                break
            clean_name = os.path.basename(src)
            for root, _, files in os.walk(sdir):
                if clean_name in files:
                    found_file = os.path.join(root, clean_name)
                    break
            if found_file:
                break
        if found_file and os.path.exists(found_file):
            mime, _ = mimetypes.guess_type(found_file)
            if not mime:
                mime = 'image/png'
            with open(found_file, 'rb') as img_f:
                b64 = base64.b64encode(img_f.read()).decode('ascii')
            return f'<img {prefix}src="data:{mime};base64,{b64}"{suffix}>'
        return match.group(0)

    new_text = re.sub(r'<img\s+([^>]*?)src="([^"]+)"([^>]*?)>', repl_html, new_text)

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_text)


if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[1] == '--embed':
        embed_images_in_markdown(sys.argv[2], sys.argv[3:])
        sys.exit(0)
        
    if len(sys.argv) < 4:
        print("Uso: python compiler.py <dir_path> <doc_name> <output_dir>")
        sys.exit(1)
    compile_markdown(sys.argv[1], sys.argv[2], sys.argv[3])


