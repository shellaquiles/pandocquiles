# 4. Integración en Proyectos Existentes

PanDocquiles fue diseñado para integrarse sin esfuerzo en cualquier repositorio o proyecto de software existente (JavaScript/TypeScript, Python, Go, Java, etc.) como una herramienta autónoma de documentación.

---

## 1. Estrategias de Integración

Existen dos formas principales de incorporar PanDocquiles en un proyecto:

### Opción A: Como Submódulo Git (Recomendado)
Puedes vincular PanDocquiles como un submódulo dentro de tu repositorio principal en la carpeta `tools/pandocquiles`:

```bash
git submodule add https://github.com/tu-usuario/pandocquiles.git tools/pandocquiles
```

### Opción B: Inclusión Directa
Puedes copiar la estructura ligera de PanDocquiles (`bin/`, `config/`, `src/`) directamente dentro de la carpeta `tools/` o `scripts/` de tu proyecto.

---

## 2. Integración con Scripts de Proyectos (ej. Node.js `package.json`)

Si tu proyecto utiliza `npm` o `yarn`, puedes agregar comandos de compilación directamente en tu `package.json`:

```json
{
  "name": "mi-proyecto",
  "scripts": {
    "docs:build": "./tools/pandocquiles/bin/build.sh docs",
    "docs:build:custom": "./tools/pandocquiles/bin/build.sh ruta/a/mi-manual"
  }
}
```

De esta forma, cualquier miembro del equipo puede compilar la documentación oficial ejecutando simplemente:

```bash
npm run docs:build
```

---

## 3. Automatización en Pipelines de CI/CD

PanDocquiles puede integrarse en pipelines de Integración Continua (CI/CD) para compilar y publicar la documentación automáticamente en cada `push` o lanzamiento de versión.

### Ejemplo en GitHub Actions (`.github/workflows/docs.yml`):

```yaml
name: Compilar y Publicar Documentación

on:
  push:
    branches: [ main ]
    paths:
      - 'docs/**'

jobs:
  build-docs:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout del Repositorio
        uses: actions/checkout@v3

      - name: Configurar Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Instalar Dependencias del Sistema (Pandoc y Exiftool)
        run: |
          sudo apt-get update
          sudo apt-get install -y pandoc exiftool

      - name: Ejecutar Compilación de PanDocquiles
        env:
          DRIVE_WEBHOOK_URL: ${{ secrets.DRIVE_WEBHOOK_URL }}
          PDF_SUBTITLE: "Documentación Oficial de API"
          PDF_TOP_HEADER: "Mi Organización Org"
          PDF_ORG_NAME="MIORGANIZACION.ORG"
        run: |
          chmod +x ./bin/build.sh
          ./bin/build.sh docs

      - name: Subir Archivos Generados como Artefacto de CI
        uses: actions/upload-artifact@v3
        with:
          name: documentacion-oficial
          path: documentacion/
```

---

## 4. Estructura Limpia de Repositorio Objetivo

Al integrar PanDocquiles en tu proyecto existente, tu repositorio mantendrá una separación clara entre el código fuente de tu aplicación y la documentación:

```text
mi-proyecto-existente/
├── .github/
│   └── workflows/
│       └── docs.yml           <-- Pipeline de automatización
├── src/                       <-- Código fuente de tu aplicación
├── docs/                      <-- Documentación fuente (Markdown)
│   ├── README.md
│   ├── 01-inicio.md
│   └── 02-api.md
├── documentacion/             <-- Artefactos generados (.pdf y .html)
├── .env                       <-- Variables locales (ignorado)
├── package.json
└── bin/
    └── build.sh               <-- Orquestador PanDocquiles
```
