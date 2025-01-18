# Generador de Audiolibro 📚🔊

¡Bienvenido al Generador de Audiolibro! Este proyecto te permite convertir documentos PDF en audiolibros utilizando tecnologías de texto a voz (TTS). 🎧

## Características ✨

- **Extracción de texto**: Obtiene el contenido de archivos PDF.
- **Conversión a audio**: Convierte el texto extraído en archivos de audio utilizando la biblioteca `gTTS` (Google Text-to-Speech).
- **Reproducción de audio**: Reproduce el audio generado directamente desde la aplicación.

## Requisitos 🛠️

- Python 3.x
- Bibliotecas de Python:
  - `PyPDF2`
  - `gTTS`
  - `pydub`

Puedes instalar las bibliotecas necesarias utilizando `pip`:

```bash
pip install PyPDF2 gTTS pydub

Uso 🚀
Procesar un PDF: Extrae el texto de un archivo PDF especificando su ruta.

Guardar el texto: Almacena el texto extraído en un archivo de texto para su posterior uso.

Convertir texto a audio: Utiliza gTTS para transformar el texto guardado en un archivo de audio en formato MP3.

Reproducir el audio: Reproduce el archivo de audio generado directamente desde la aplicación.

Ejemplo de uso 📄➡️🔊
from text_to_speech import TextProcessor

# Crear una instancia del procesador de texto
processor = TextProcessor()

# Procesar el archivo PDF
processor.process_pdf('ruta/al/archivo.pdf')

# Guardar el texto extraído
processor.save_text('nombre_del_archivo.txt')

# Convertir el texto a audio
processor.text_to_speech('nombre_del_archivo.txt')

# Reproducir el audio generado
processor.play_audio('nombre_del_archivo.mp3')
