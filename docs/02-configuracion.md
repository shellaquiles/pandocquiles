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
| `DRIVE_WEBHOOK_URL` | URL de tu despliegue web de Google Apps Script. | `""` (Omitido) |
| `PDF_SUBTITLE` | Subtítulo principal que aparecerá en la portada oficial. | `"Documentación del Proyecto"` |
| `PDF_TOP_HEADER` | Encabezado superior en mayúsculas (membrete) de la portada. | `"Organización"` |
| `PDF_ORG_NAME` | Nombre corto de tu organización usado en encabezados y pies de página. | `"Organización"` |
| `PDF_AUTHOR` | Metadato del autor insertado en las propiedades del archivo PDF. | `"Organización"` |
| `PDF_CREATOR` | Metadato de la herramienta creadora del PDF. | `"Organización"` |
| `PDF_PRODUCER` | Metadato del productor del documento PDF. | `"Generador de PDF"` |
| `INPUT_DIRS` | Directorios por defecto a compilar si no se pasan argumentos por CLI. | `"docs"` |
| `OUTPUT_DIR` | Directorio de destino para guardar los archivos `.pdf` y `.html`. | `"documentacion"` |
| `CSS_PDF_THEME` | Ruta a la hoja de estilo CSS usada para el motor de generación PDF. | `"config/css/theme-pdf.css"` |
| `CSS_GDOCS_THEME` | Ruta a la hoja de estilo CSS usada por Pandoc para el archivo HTML. | `"config/css/theme-gdocs.css"` |

---

## 2. Personalización Visual (CSS)

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

