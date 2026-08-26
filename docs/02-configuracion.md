# 2. Configuración y Personalización

PanDocquiles es una herramienta segura, agnóstica y altamente configurable. Toda la información específica de tu organización (nombres, títulos, metadatos y webhook) se gestiona a través de variables de entorno, mientras que la apariencia visual se controla mediante hojas de estilo y plantillas.

---

## 1. Variables de Entorno (`.env`)

Para comenzar, crea tu archivo `.env` basándote en el archivo de plantilla `.env.example`:

```bash
cp .env.example .env
```

> [!IMPORTANT]
> **Seguridad**: El archivo `.env` contiene credenciales e información sensible. Nunca debe ser subido al control de versiones (ya está ignorado en `.gitignore`).

### Referencia de Variables Disponibles:

| Variable | Descripción | Valor por Defecto |
| :--- | :--- | :--- |
| `COLOR_THEME` | Tema de color predefinido (`blue`, `cdmx`, `emerald`, `purple`, `amber`, `slate`). | `"blue"` |
| `COLOR_PRIMARY` | (Opcional) Color primario en formato HEX para títulos y acentos principales. | Derivado del tema |
| `COLOR_ACCENT` | (Opcional) Color secundario / de contraste. | Derivado del tema |
| `COLOR_BG_SUBTLE` | (Opcional) Fondo sutil para bloques de alerta y cabeceras de tablas. | Derivado del tema |
| `COLOR_TEXT_SUBTLE` | (Opcional) Color de texto para llamadas de atención. | Derivado del tema |
| `DRIVE_WEBHOOK_URL` | URL de tu despliegue web de Google Apps Script. | `""` (Omitido) |
| `PDF_SUBTITLE` | Subtítulo principal que aparecerá en la portada oficial. | `"Documentación del Proyecto"` |
| `PDF_TOP_HEADER` | Encabezado superior en mayúsculas (membrete) de la portada. | `"Organización"` |
| `PDF_ORG_NAME` | Nombre corto de tu organización usado en encabezados y pies de página. | `"Organización"` |
| `PDF_AUTHOR` | Metadato del autor insertado en las propiedades del archivo PDF. | `"Organización"` |
| `PDF_CREATOR` | Metadato de la herramienta creadora del PDF. | `"Organización"` |
| `PDF_PRODUCER` | Metadato del productor del documento PDF. | `"Generador de PDF"` |
| `INPUT_DIRS` | Directorios por defecto a compilar si no se pasan argumentos por CLI. | `"docs"` |
| `OUTPUT_DIR` | Directorio de destino para guardar los archivos `.pdf` y `.html`. | `"documentacion"` |
| `OUTPUT_FORMATS` | Formatos de salida a generar (`"all"` para PDF+HTML+DOCX, o `"pdf"` para solo PDF). | `"all"` |
| `CSS_PDF_THEME` | Ruta a la hoja de estilo CSS usada para el motor de generación PDF. | `"config/css/theme-pdf.css"` |
| `CSS_GDOCS_THEME` | Ruta a la hoja de estilo CSS usada por Pandoc para el archivo HTML. | `"config/css/theme-gdocs.css"` |

---

## 2. Paletas de Colores Predefinidas

PanDocquiles incluye una selección de paletas visuales listas para usar que armonizan tipografía, portada, encabezados, tablas, listas y cajas de texto:

| Tema | Alias | Muestra | Primario | Acento | Fondo Sutil | Ideal para |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **`blue` (Por defecto)** | `corporate`, `tech` | <span style="background-color:#1E40AF;color:#1E40AF;border-radius:3px;padding:2px 10px;border:1px solid #1E40AF;">■</span> <span style="background-color:#2563EB;color:#2563EB;border-radius:3px;padding:2px 10px;border:1px solid #2563EB;">■</span> <span style="background-color:#EFF6FF;color:#EFF6FF;border-radius:3px;padding:2px 10px;border:1px solid #cbd5e1;">■</span> | `#1E40AF` | `#2563EB` | `#EFF6FF` | Empresas tech, manuales técnicos y SaaS |
| **`cdmx`** | `guinda` | <span style="background-color:#9D2449;color:#9D2449;border-radius:3px;padding:2px 10px;border:1px solid #9D2449;">■</span> <span style="background-color:#B32850;color:#B32850;border-radius:3px;padding:2px 10px;border:1px solid #B32850;">■</span> <span style="background-color:#FDF4F6;color:#FDF4F6;border-radius:3px;padding:2px 10px;border:1px solid #cbd5e1;">■</span> | `#9D2449` | `#B32850` | `#FDF4F6` | Gobierno de la CDMX e institucional |
| **`emerald`** | `forest`, `green` | <span style="background-color:#065F46;color:#065F46;border-radius:3px;padding:2px 10px;border:1px solid #065F46;">■</span> <span style="background-color:#059669;color:#059669;border-radius:3px;padding:2px 10px;border:1px solid #059669;">■</span> <span style="background-color:#ECFDF5;color:#ECFDF5;border-radius:3px;padding:2px 10px;border:1px solid #cbd5e1;">■</span> | `#065F46` | `#059669` | `#ECFDF5` | Sostenibilidad, ecología y salud |
| **`purple`** | `violet` | <span style="background-color:#6B21A8;color:#6B21A8;border-radius:3px;padding:2px 10px;border:1px solid #6B21A8;">■</span> <span style="background-color:#7C3AED;color:#7C3AED;border-radius:3px;padding:2px 10px;border:1px solid #7C3AED;">■</span> <span style="background-color:#FAF5FF;color:#FAF5FF;border-radius:3px;padding:2px 10px;border:1px solid #cbd5e1;">■</span> | `#6B21A8` | `#7C3AED` | `#FAF5FF` | Diseño moderno, creativos y startups |
| **`amber`** | `warm`, `orange` | <span style="background-color:#9A3412;color:#9A3412;border-radius:3px;padding:2px 10px;border:1px solid #9A3412;">■</span> <span style="background-color:#EA580C;color:#EA580C;border-radius:3px;padding:2px 10px;border:1px solid #EA580C;">■</span> <span style="background-color:#FFF7ED;color:#FFF7ED;border-radius:3px;padding:2px 10px;border:1px solid #cbd5e1;">■</span> | `#9A3412` | `#EA580C` | `#FFF7ED` | Documentos ejecutivos, avisos y auditorías |
| **`slate`** | `minimal`, `gray` | <span style="background-color:#334155;color:#334155;border-radius:3px;padding:2px 10px;border:1px solid #334155;">■</span> <span style="background-color:#475569;color:#475569;border-radius:3px;padding:2px 10px;border:1px solid #475569;">■</span> <span style="background-color:#F8FAFC;color:#F8FAFC;border-radius:3px;padding:2px 10px;border:1px solid #cbd5e1;">■</span> | `#334155` | `#475569` | `#F8FAFC` | Minimalismo sobrio y elegante |


### Formas de seleccionar un tema:
1. **Vía CLI**:
   ```bash
   ./bin/build.sh --theme=emerald docs
   ```
2. **Vía `.env`**:
   ```bash
   COLOR_THEME=purple
   ```
3. **Colores Hexadecimales personalizados**:
   ```bash
   COLOR_PRIMARY="#0f766e" COLOR_ACCENT="#0d9488" ./bin/build.sh docs
   ```

---

## 3. Personalización Visual (CSS)

La identidad gráfica de tus documentos se controla mediante dos archivos CSS situados en `config/css/`:

### 📄 `config/css/theme-pdf.css` (Para PDFs impresos)
Utilizado por el motor `md-to-pdf` (Puppeteer/Chromium). Te permite personalizar:
- **Tipografías y Escala**: Fuentes del sistema o Google Fonts importadas (ej. Inter), con proporciones compactas que evitan cortes de línea en títulos largos.
- **Paginación Semántica**: Saltos automáticos limpios por `h1` y soporte para clases manuales como `.page-break` o `.salto-pagina`.
- **Protección Anti-Huérfanos**: Reglas de cohesión vertical (`break-after: avoid`, `p:has(img)` protegido).
- **Tablas Responsivas**: `table-layout: fixed` con quiebre automático de palabras en celdas con código.
- **Bloques de Código**: Presentación limpia, monoespaciada y sin dobles marcos interiores.

### 🌐 `config/css/theme-gdocs.css` (Para HTML y Google Docs)
Utilizado por Pandoc para construir el archivo `.html` incrustado. Está optimizado para:
- Pantallas digitales y compatibilidad al copiar/pegar directamente a procesadores de texto en la nube.
- Mantener las proporciones de imágenes incrustadas en Base64 sin distorsionar el diseño.

---

## 3. Plantillas de Referencia (`config/templates/`)

Si requieres exportar documentos a formatos de procesador de texto (como `.docx`) manteniendo estilos corporativos específicos, puedes colocar tus plantillas en `config/templates/`.

Pandoc permite utilizar la bandera `--reference-doc=config/templates/referencia.docx` para adoptar los estilos, encabezados y fuentes de tu plantilla oficial de Word.

---

## 4. Configuración del Webhook de Google Drive

Para habilitar la sincronización automática a Google Drive:

1. Ingresa a [Google Apps Script](https://script.google.com/) con tu cuenta de Google.
2. Crea un nuevo proyecto y reemplaza el contenido por el código de [`src/webhooks/drive_webhook.js`](file:///home/kubrick/www/pandocquiles/src/webhooks/drive_webhook.js).
3. Modifica la constante `FOLDER_ID` con el ID de la carpeta de Google Drive donde deseas almacenar los archivos.
4. **Habilita el Servicio de Drive**: En la barra lateral izquierda, da clic en **Servicios (+)** y agrega la **Drive API (v2)**.
5. Selecciona **Implementar > Nueva implementación**, elige tipo **Aplicación web**, configura "Ejecutar como: Yo" y "Quién tiene acceso: Cualquier persona".
6. Copia la URL de la implementación resultante y asígnala a `DRIVE_WEBHOOK_URL` en tu `.env`.

