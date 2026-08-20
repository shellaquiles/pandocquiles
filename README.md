# PanDocquiles 🌮📄

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg?style=flat-square)](./CHANGELOG.md) [![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)](./LICENSE) [![Python](https://img.shields.io/badge/python-3.8%2B-3776AB.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/) [![Node](https://img.shields.io/badge/node-%3E%3D16-339933.svg?style=flat-square&logo=nodedotjs&logoColor=white)](https://nodejs.org/) [![Ecosystem](https://img.shields.io/badge/shellaquiles-ecosystem-9D2449.svg?style=flat-square)]()

PanDocquiles es una herramienta (de la familia de proyectos de Shellaquiles) creada con un propósito muy práctico: **convertir tu documentación escrita en Markdown a PDF e HTML/Docs, y subirla automáticamente a Google Drive.**

### ¿Por qué existe esto?

Si trabajas escribiendo documentación técnica en Markdown, seguro te ha pasado: llega el momento de compartir los manuales o especificaciones con un cliente, auditor o alguien del equipo no técnico, y terminas perdiendo un buen rato convirtiendo archivos a PDF o pegando texto en procesadores para que los puedan leer y ajustar.

PanDocquiles automatiza todo ese proceso:
- **Ensambla tus archivos Markdown** (como los capítulos en `docs/`).
- **Renderiza los diagramas de Mermaid** a imágenes para que no se rompan al exportar.
- **Aplica estilos CSS** para generar un **PDF** profesional y un **HTML** compatible con Google Docs.
- **Sube todo a Google Drive**, y si el archivo ya existía en la nube, lo actualiza manteniendo el mismo enlace para que nadie pierda acceso.

---

## 🛠️ Requisitos del Sistema

Para ejecutar PanDocquiles en tu entorno local o en tu servidor de CI/CD, asegúrate de contar con:

- **Node.js** (v16+): Utilizado por `npx` para ejecutar `md-to-pdf` y `@mermaid-js/mermaid-cli`.
- **Python 3**: Ejecuta los módulos de ensamblaje, formateo HTML y subida a la nube.
- **Pandoc**: Motor de conversión de documentos.
- **Exiftool**: Reescribe metadatos oficiales (autor, productor, título) en las propiedades internas del PDF.

---

## 📚 Documentación Completa (`/docs`)

El proyecto incluye su propia documentación oficial estructurada en la carpeta [`docs/`](./docs/), la cual además sirve como prueba en vivo del sistema (*Dogfooding*):

1. 🏛️ **[Arquitectura e Inspección del Sistema](./docs/01-arquitectura.md)**: Detalla la interacción entre el orquestador Bash, los módulos de Python y el Webhook de Google Apps Script.
2. ⚙️ **[Configuración y Personalización](./docs/02-configuracion.md)**: Explicación completa de las variables de entorno (`.env`), personalización CSS y plantillas corporativas.
3. 📖 **[Guía de Uso y Estructuración](./docs/03-uso.md)**: Reglas de nomenclatura de capítulos, alertas de GitHub y sintaxis Mermaid compatible.
4. 🔌 **[Integración en Proyectos Existentes y CI/CD](./docs/04-integracion.md)**: Cómo incluir PanDocquiles como submódulo Git o script NPM e integrarlo en GitHub Actions / GitLab CI.

---

## ⚡ Inicio Rápido

### 1. Clonar y Configurar Entorno

```bash
cp .env.example .env
```

Edita `.env` para personalizar los títulos de tu organización y la URL de tu Webhook de Google Drive.

### 2. Compilar Documentación

Por defecto, PanDocquiles compilará su propia documentación situada en `docs/`:

```bash
./bin/build.sh
```

O especifica la ruta de cualquier directorio de documentación personalizado:

```bash
./bin/build.sh ruta/a/mi-documentacion
```

Los resultados finales se guardarán en el directorio `documentacion/` (`pandocquiles.pdf`, `pandocquiles.html` y `pandocquiles.docx`).

---

## 🔌 Integración en Tu Proyecto

Si quieres sumar PanDocquiles a un repositorio ya existente para compilar su documentación, puedes agregarlo fácilmente como submódulo Git:

```bash
git submodule add https://github.com/shellaquiles/pandocquiles.git tools/pandocquiles
```

Y luego compilar tus archivos en cualquier momento:

```bash
./tools/pandocquiles/bin/build.sh docs
```

Para ver la guía avanzada sobre automatización en **GitHub Actions**, **GitLab CI** o scripts de `package.json`, revisa [`docs/04-integracion.md`](./docs/04-integracion.md).

---

## 📄 Comunidad y Licencia

Desarrollado bajo la licencia MIT como parte del ecosistema de proyectos de **Shellaquiles Org**.

- 📜 [Licencia MIT](./LICENSE)
- 📋 [Historial de Cambios (Changelog)](./CHANGELOG.md)
- 🤝 [Guía de Contribución](./CONTRIBUTING.md)
- 🛡️ [Política de Seguridad](./SECURITY.md)
- 📜 [Código de Conducta](./CODE_OF_CONDUCT.md)

### 🌟 Agradecimientos Especiales

Un reconocimiento especial a **[@m1gl0](https://github.com/m1gl0)** por su aportación en el desarrollo e integración del Sincronizador Autónomo a Google Drive y el Webhook de Google Apps Script con conversión inteligente a Google Docs.

