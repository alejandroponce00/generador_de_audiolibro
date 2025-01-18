import os
from datetime import datetime
import PyPDF2
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io

class TextProcessor:
    def __init__(self):
        self.output_dir = "processed_texts"
        self.audio_dir = "processed_audio"
        self.ensure_output_dirs()
        self.available_languages = {
            'es': 'Español',
            'en': 'Inglés',
            'fr': 'Francés',
            'de': 'Alemán',
            'it': 'Italiano',
            'pt': 'Portugués',
            'ru': 'Ruso',
            'ja': 'Japonés',
            'ko': 'Coreano',
            'zh-CN': 'Chino Mandarín'
        }
    
    def ensure_output_dirs(self):
        """Crear directorios de salida si no existen"""
        for directory in [self.output_dir, self.audio_dir]:
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def show_available_languages(self):
        """Mostrar los idiomas disponibles"""
        print("\nIdiomas disponibles:")
        for code, name in self.available_languages.items():
            print(f"- {code}: {name}")
    
    def validate_pdf(self, pdf_path):
        """Validar si el archivo es un PDF válido"""
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError("El archivo debe tener extensión .pdf")
        
        if not os.path.exists(pdf_path):
            raise FileNotFoundError("El archivo PDF no existe")
        
        if os.path.getsize(pdf_path) == 0:
            raise ValueError("El archivo PDF está vacío")
    
    def read_pdf(self, pdf_path):
        """Leer y extraer texto de un archivo PDF"""
        try:
            # Primero validamos el PDF
            self.validate_pdf(pdf_path)
            
            with open(pdf_path, 'rb') as file:
                # Intentamos crear el lector PDF
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    # Verificamos si el PDF está encriptado
                    if pdf_reader.is_encrypted:
                        raise ValueError("El PDF está encriptado y no se puede leer")
                    
                    # Verificamos si tiene páginas
                    if len(pdf_reader.pages) == 0:
                        raise ValueError("El PDF no contiene páginas")
                    
                    text = ""
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        try:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text
                            else:
                                print(f"Advertencia: La página {page_num} está vacía o no contiene texto extraíble")
                        except Exception as e:
                            print(f"Advertencia: No se pudo extraer texto de la página {page_num}: {str(e)}")
                    
                    if not text.strip():
                        raise ValueError("No se pudo extraer ningún texto del PDF")
                    
                    return text
                
                except PyPDF2.PdfReadError as e:
                    raise ValueError(f"El archivo PDF está dañado o no es válido: {str(e)}")
                
        except Exception as e:
            raise Exception(f"Error al procesar el archivo PDF: {str(e)}")
    
    def text_to_speech(self, text, language='es'):
        """Convertir texto a audio y reproducirlo"""
        try:
            if language not in self.available_languages:
                raise ValueError(f"Idioma '{language}' no soportado")
            
            # Crear un objeto gTTS
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Guardar el audio en un archivo temporal
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_path = f"{self.audio_dir}/audio_{timestamp}_{language}.mp3"
            tts.save(audio_path)
            
            # Cargar y reproducir el audio
            audio = AudioSegment.from_mp3(audio_path)
            play(audio)
            
            return audio_path
        except Exception as e:
            raise Exception(f"Error en la conversión de texto a voz: {str(e)}")
    
    def process_pdf(self, pdf_path, language='es'):
        """Procesar el archivo PDF y convertirlo a audio"""
        # Extraer texto del PDF
        text = self.read_pdf(pdf_path)
        
        # Procesar el texto
        processed_text = text.strip()
        words = len(processed_text.split())
        chars = len(processed_text)
        
        # Generar estadísticas
        stats = f"""Estadísticas del texto:
        Palabras: {words}
        Caracteres: {chars}
        Caracteres (sin espacios): {len(processed_text.replace(' ', ''))}
        Idioma seleccionado: {self.available_languages[language]}
        """
        
        # Guardar texto procesado
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_filename = f"{self.output_dir}/texto_{timestamp}_{language}.txt"
        
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(f"Texto Original:\n{processed_text}\n\n{stats}")
        
        # Convertir a audio
        audio_path = self.text_to_speech(processed_text, language)
        
        return text_filename, audio_path, stats

def main():
    processor = TextProcessor()
    
    while True:
        print("\n=== Procesador de PDF a Audio ===")
        pdf_path = input("\nIngresa la ruta del archivo PDF (o 'q' para salir): ")
        
        if pdf_path.lower() == 'q':
            print("¡Hasta luego!")
            break
        
        # Mostrar idiomas disponibles y solicitar selección
        processor.show_available_languages()
        language = input("\nSelecciona el código del idioma (por defecto 'es'): ").strip()
        
        # Si no se selecciona ningún idioma, usar español por defecto
        if not language:
            language = 'es'
        
        # Verificar si el idioma es válido
        if language not in processor.available_languages:
            print(f"Idioma '{language}' no válido. Usando español por defecto.")
            language = 'es'
        
        try:
            text_file, audio_file, stats = processor.process_pdf(pdf_path, language)
            print("\n=== Proceso completado con éxito ===")
            print(f"Archivo de texto guardado en: {text_file}")
            print(f"Archivo de audio guardado en: {audio_file}")
            print("\n" + stats)
        except FileNotFoundError as e:
            print(f"\nError: {str(e)}")
            print("Por favor, verifica que la ruta del archivo sea correcta.")
        except ValueError as e:
            print(f"\nError: {str(e)}")
            print("Por favor, asegúrate de que el archivo sea un PDF válido y no esté dañado.")
        except Exception as e:
            print(f"\nError inesperado: {str(e)}")
            print("Si el problema persiste, verifica que el archivo PDF no esté corrupto o protegido.")

if __name__ == "__main__":
    main()