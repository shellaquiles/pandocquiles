#!/bin/bash

# ==============================================================================
# PanDocquiles v1.1.1 - Orquestador de Compilación
# Script principal que coordina la generación de PDFs, HTMLs y DOCX a partir de MD.
# ==============================================================================

set -e

# Asegurar que se ejecuta en la raíz del proyecto
cd "$(dirname "$0")/.."

# Cargar variables de entorno si existe .env
if [ -f ".env" ]; then
  set -a
  . ./.env
  set +a
fi

# Variables de configuración por defecto
DEFAULT_INPUT_DIRS="${INPUT_DIRS:-docs}"
OUTPUT_DIR="${OUTPUT_DIR:-documentacion}"
CSS_PDF_THEME="${CSS_PDF_THEME:-config/css/theme-pdf.css}"
CSS_GDOCS_THEME="${CSS_GDOCS_THEME:-config/css/theme-gdocs.css}"
PDF_ONLY="${PDF_ONLY:-false}"
if [ "${OUTPUT_FORMATS:-}" = "pdf" ]; then
    PDF_ONLY=true
fi

# Determinar argumentos y opciones
TARGET_DIRS=()
for arg in "$@"; do
    case $arg in
        --theme=*)
            export COLOR_THEME="${arg#*=}"
            ;;
        -t=*)
            export COLOR_THEME="${arg#*=}"
            ;;
        --pdf-only|--pdf)
            PDF_ONLY=true
            ;;
        -t)
            # El siguiente argumento será el tema si se usa espacio
            ;;
        *)
            if [ "$PREV_ARG" = "-t" ]; then
                export COLOR_THEME="$arg"
                PREV_ARG=""
            else
                TARGET_DIRS+=("$arg")
            fi
            ;;
    esac
    PREV_ARG="$arg"
done

if [ ${#TARGET_DIRS[@]} -eq 0 ]; then
    read -r -a TARGET_DIRS <<< "$DEFAULT_INPUT_DIRS"
fi

# Crear directorio de salida si no existe
mkdir -p "$OUTPUT_DIR/"

for DIR in "${TARGET_DIRS[@]}"; do
    # Remover barra al final si la tiene
    DIR="${DIR%/}"
    
    if [ ! -d "$DIR" ]; then
        echo "⚠️ El directorio '$DIR' no existe. Omitiendo..."
        continue
    fi

    # Validar que existan archivos Markdown en el directorio
    if ls "$DIR"/*.md 1> /dev/null 2>&1; then
        DOC_NAME="$(basename "$DIR")"
        if [ "$DOC_NAME" = "docs" ]; then
            DOC_NAME="pandocquiles"
        fi
        
        echo "============================================================"
        echo "📘 Construyendo: $DOC_NAME ($DIR)"
        echo "============================================================"
        
        # 1. Unir capítulos, generar portada y configuración de PDF (Python)
        echo "🧩 Ensamblando capítulos de Markdown..."
        python3 src/python/compiler.py "$DIR" "$DOC_NAME" "$OUTPUT_DIR"
        
        # 2. Renderizar Mermaid a PNG (Google Docs no acepta SVG)
        echo "🎨 Renderizando diagramas Mermaid..."
        npx -y @mermaid-js/mermaid-cli -i "$OUTPUT_DIR/$DOC_NAME.md" -o "$OUTPUT_DIR/TEMP_MERMAID.md" -e png -s 2 -b white
        
        # Mover las imágenes PNG generadas por mermaid al directorio de salida
        mv TEMP_MERMAID-*.png "$OUTPUT_DIR/" 2>/dev/null || true
        
        # 3. Preparar archivo PDF con imágenes Base64 embebidas directamente
        echo "🖼️ Incrustando recursos gráficos en el Markdown del PDF..."
        cp "$OUTPUT_DIR/TEMP_MERMAID.md" "$OUTPUT_DIR/TEMP_PDF.md"
        python3 src/python/compiler.py --embed "$OUTPUT_DIR/TEMP_PDF.md" "$OUTPUT_DIR" "$DIR" .
        
        if [ "$PDF_ONLY" = false ]; then
            # 4. Construir HTML (para Google Docs) con imágenes incrustadas en Base64
            echo "🌐 Construyendo HTML con recursos embebidos..."
            pandoc "$OUTPUT_DIR/TEMP_MERMAID.md" -o "$OUTPUT_DIR/$DOC_NAME.html" \
                --self-contained \
                --css="$CSS_GDOCS_THEME" \
                --resource-path="$DIR:.:$OUTPUT_DIR"
            
            # Formatear el HTML generado para que las imágenes respeten anchos (Python)
            echo "🪄 Aplicando correcciones visuales al HTML..."
            python3 src/python/html_formatter.py "$OUTPUT_DIR/$DOC_NAME.html"

            # 5. Construir documento Microsoft Word (.docx) a partir del HTML formateado
            echo "📝 Compilando documento Word ($DOC_NAME.docx)..."
            REF_DOC_OPTION=""
            if [ -f "config/templates/referencia.docx" ]; then
                REF_DOC_OPTION="--reference-doc=config/templates/referencia.docx"
            elif [ -f "config/templates/referencia_modificada.docx" ]; then
                REF_DOC_OPTION="--reference-doc=config/templates/referencia_modificada.docx"
            fi

            pandoc "$OUTPUT_DIR/$DOC_NAME.html" -o "$OUTPUT_DIR/$DOC_NAME.docx" \
                $REF_DOC_OPTION
        fi

        # 6. Construir PDF usando theme-pdf.css
        echo "📄 Compilando PDF final ($DOC_NAME.pdf)..."
        npx -y md-to-pdf "$OUTPUT_DIR/TEMP_PDF.md" \
            --stylesheet "$CSS_PDF_THEME" \
            --config-file "$OUTPUT_DIR/pdf_config.json"
        
        # Reescribir metadatos del PDF si se generó el título exitosamente
        if [ -f "$OUTPUT_DIR/title.txt" ]; then
            MAIN_TITLE=$(cat "$OUTPUT_DIR/title.txt")
            echo "📝 Escribiendo metadatos PDF oficiales..."
            exiftool -Title="$MAIN_TITLE" \
                     -Author="${PDF_AUTHOR:-Organización}" \
                     -Creator="${PDF_CREATOR:-Organización}" \
                     -Producer="${PDF_PRODUCER:-Generador de PDF}" \
                     -overwrite_original "$OUTPUT_DIR/TEMP_PDF.pdf"
            rm "$OUTPUT_DIR/title.txt"
        fi
        
        # 7. Mover y limpiar dentro de OUTPUT_DIR
        mv "$OUTPUT_DIR/TEMP_PDF.pdf" "$OUTPUT_DIR/$DOC_NAME.pdf"
        rm "$OUTPUT_DIR/TEMP_MERMAID.md" "$OUTPUT_DIR/TEMP_PDF.md" 2>/dev/null || true
        rm "$OUTPUT_DIR"/TEMP_MERMAID-*.png 2>/dev/null || true
        rm TEMP_MERMAID-*.png 2>/dev/null || true
        rm "$OUTPUT_DIR/pdf_config.json" 2>/dev/null || true
        rm "$OUTPUT_DIR/$DOC_NAME.md" 2>/dev/null || true
        
        if [ "$PDF_ONLY" = true ]; then
            echo "✅ Completado: $OUTPUT_DIR/$DOC_NAME.pdf"
        else
            echo "✅ Completado: $OUTPUT_DIR/$DOC_NAME.html, $OUTPUT_DIR/$DOC_NAME.docx y $OUTPUT_DIR/$DOC_NAME.pdf"
        fi
    else
        echo "⚠️ No se encontraron archivos Markdown (.md) en '$DIR'. Omitiendo..."
    fi
done

echo "☁️ Sincronizando resultados con Google Drive..."
python3 src/python/uploader.py

echo "🎉 ¡Compilaciones finalizadas y subidas con éxito!"

