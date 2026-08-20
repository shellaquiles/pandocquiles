# Guía de Contribución 🤝

¡Gracias por tu interés en hacer de **PanDocquiles** una herramienta aún mejor! 

## 🛠️ ¿Cómo contribuir?

1. Haz un **Fork** del repositorio.
2. Crea una rama para tu característica o corrección:
   ```bash
   git checkout -b feature/mi-nueva-caracteristica
   ```
3. Realiza tus cambios asegurándote de mantener el código limpio y documentado.
4. Ejecuta la compilación de prueba para validar que todo funcione sin errores:
   ```bash
   ./bin/build.sh
   ```
5. Haz commit de tus cambios y envía un **Pull Request**.

## 📝 Convenciones de Código

- **Python**: Estándar PEP 8 con *Docstrings* explicativos en cada módulo y función.
- **Bash**: Usar `set -e` al inicio y definir fallbacks para variables de entorno.
- **Documentación**: Mantener los archivos Markdown libres de clichés o modismos automatizados.
