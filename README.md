# Whisper App Windows

Este proyecto permite transcribir y traducir archivos de audio y video usando Whisper, con una interfaz gráfica amigable y un instalador automático de dependencias.

## Estructura del proyecto

```
python-installer
├── src
│   ├── whisper_gui.py        # Interfaz gráfica principal
│   ├── installer.py          # Verifica e instala Python si es necesario
│   ├── python_installer.py   # Lógica para descargar e instalar Python
│   └── utils
│       └── check_python.py   # Utilidades para verificar Python
├── requirements.txt          # Dependencias del proyecto
├── .gitignore                # Ignora archivos generados
└── README.md                 # Documentación
```

## Instalación y uso

1. **Clona el repositorio:**
   ```
   git clone https://github.com/caponte/whisper-app-windows.git
   cd whisper-app-windows
   ```

2. **Instala las dependencias:**
   Se recomienda usar un entorno virtual.
   ```
   python -m venv .venv
   .venv\Scripts\activate  # En Windows
   pip install -r requirements.txt
   ```

3. **Genera el ejecutable:**
   ```
   pyinstaller --onefile --name carloscoding src/whisper_gui.py
   ```
   El ejecutable se creará en la carpeta `dist` como `carloscoding.exe`.

4. **Ejecuta la aplicación:**
   - Puedes ejecutar `carloscoding.exe` directamente. El programa:
     - Verifica e instala Python si es necesario.
     - Verifica e instala FFmpeg y Whisper-CLI usando Chocolatey.
     - Lanza la interfaz gráfica para transcribir archivos.

## Requisitos
- Windows 10/11
- Permisos de administrador para instalar dependencias
- Chocolatey (si no está instalado, la app intentará instalarlo)

## Notas importantes
- Si copias solo el `.exe` a otra PC, asegúrate de tener permisos de administrador y acceso a internet para instalar dependencias.
- El instalador no incluye FFmpeg ni Whisper-CLI, pero los instala automáticamente si faltan.

## Contribuir
¡Las contribuciones son bienvenidas! Abre un issue o pull request para sugerencias o mejoras.

## Licencia
MIT License.