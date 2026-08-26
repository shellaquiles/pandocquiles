# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.1] - 2026-08-26

### Añadido
- **Modo de compilación exclusiva PDF (`--pdf-only` / `--pdf`)**: Nueva bandera de CLI y variable de entorno `OUTPUT_FORMATS=pdf` para omitir la generación de HTML y DOCX cuando únicamente se requiere el PDF, acelerando el tiempo de compilación hasta en un 50%.
- **Incrustador automático de imágenes Base64 (`--embed`)**: Nuevo módulo en `compiler.py` que convierte rutas de imágenes relativas y diagramas Mermaid a `data:image/png;base64,...`, garantizando un renderizado 100% confiable en Chromium/Puppeteer sin fallos de resolución de rutas locales.
- **Soporte y estilos dedicados para Badges e Insignias (`shields.io`, `badge`)**: Reglas CSS específicas para alinear insignias inline en una sola fila compacta y horizontal, evitando que se muestren como imágenes en bloque verticales centradas con sombras.
- **Detección genérica de libros consolidados y capítulos**: Soporte para manuales maestros (`*COMPLETO*.md`, `*MASTER*.md`, `*BOOK*.md`), capítulos numerados (`[0-9]*.md`) y colecciones de archivos Markdown sin acoplamiento a nombres fijos.

### Mejorado
- **Resolución dinámica de recursos gráficos**: Uso de `os.path.relpath(dir_path, output_dir)` para calcular rutas relativas dinámicas hacia subdirectorios de imágenes (`img/`, `assets/`, `media/`).
- **Extracción resiliente de títulos y subtítulos**: Búsqueda del primer encabezado H1 en las primeras líneas del archivo Markdown para generar la portada oficial, tolerando líneas previas con comentarios, insignias o bloques vacíos.
- **Desacoplamiento total**: Eliminación de cualquier condición o nombre de archivo hardcodeado en `build.sh` y `compiler.py`.

## [1.1.0] - 2026-08-26

### Añadido
- **Paginación semántica y control anti-huérfanos en PDF**: Reglas CSS puras para inicio limpio de capítulos (`h1`), portada (`break-before: auto`) y clases de salto manual (`.page-break`, `.salto-pagina`).
- **Escala tipográfica optimizada**: Rediseño de proporciones (`h1`: `1.45em`, `h2`: `1.22em`, `h3`: `1.08em`, `code` en títulos: `0.88em`) para evitar desbordes y cortes de línea en títulos técnicos.
- **Tablas con ancho fijo y ajuste de palabras**: `table-layout: fixed !important;` con `word-break` y `overflow-wrap` para prevenir desbordes laterales.
- **Bloques de código compactos**: Eliminación de dobles cajas de fondo en `pre code` con tipografía monoespaciada de alta legibilidad (`SFMono-Regular`, `Consolas`).
- **Listas e insignias CDMX compactas**: Reducción de márgenes y tamaño de insignias numéricas a `20px × 20px`.
- **Dimensionamiento seguro de imágenes y diagramas**: Límites verticales y horizontales (`img`: máx 75% ancho / 105mm alto; `svg`: máx 85% / 120mm) con bordes suaves y sombras sutiles.
- **Sanitización de Frontmatter YAML**: Detección y remoción automática de bloques frontmatter `--- ... ---` en archivos Markdown para evitar texto residual en PDFs.
- **Slugificación de enlaces internos**: Normalización Unicode para anclas y referencias cruzadas entre capítulos.

### Modificado
- `bin/build.sh`: Inyección directa del stylesheet oficial `theme-pdf.css` y limpieza automática de imágenes intermedias de Mermaid.
- `src/python/compiler.py`: Eliminación de saltos de página artificiales repetidos en HTML/MD que causaban hojas en blanco intermedias.

## [1.0.0] - 2026-08-20

### Añadido
- Arquitectura modular desacoplada con orquestador Bash (`bin/build.sh`).
- Motor de ensamblaje en Python (`src/python/compiler.py`).
- Formateador HTML para optimización de imágenes en Base64 (`src/python/html_formatter.py`).
- Sincronizador autónomo a Google Drive (`src/python/uploader.py`).
- Webhook de Google Apps Script con conversión inteligente a Google Docs (`src/webhooks/drive_webhook.js`).
- Compilación simultánea a tres formatos principales: PDF, HTML y Microsoft Word (.docx).
- Documentación oficial auto-compilable bajo el paradigma *Dogfooding* en `docs/`.
- Archivos de estándares de código abierto (`LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`).

### Agradecimientos Especiales
- Un agradecimiento especial a **[@m1gl0](https://github.com/m1gl0)** por su valiosa aportación en el diseño e implementación del Sincronizador Autónomo a Google Drive y el Webhook de Google Apps Script con conversión inteligente a Google Docs.

