# Changelog

Todos los cambios notables en este proyecto se documentarán en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/) y este proyecto se adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
