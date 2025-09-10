import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import tempfile

class WhisperGUI:
  def __init__(self):
    self.window = tk.Tk()
    self.window.title("Transcriptor Whisper by carloscoding")
    self.window.geometry("600x450")

    # Variables
    self.input_file = tk.StringVar()
    self.output_dir = tk.StringVar()
    self.language = tk.StringVar(value="es")
    self.translate = tk.BooleanVar(value=False)
    self.ffmpeg_installed = tk.BooleanVar(value=False)
    self.whisper_installed = tk.BooleanVar(value=False)

    self.setup_gui()
    self.check_dependencies()

  def setup_gui(self):
    # Vista de dependencias
    frame_dep = ttk.LabelFrame(self.window, text="Dependencias", padding="10")
    frame_dep.pack(fill=tk.X, padx=10, pady=10)

    self.ffmpeg_label = ttk.Label(frame_dep, text="FFmpeg: Verificando...")
    self.ffmpeg_label.pack(anchor=tk.W)
    self.whisper_label = ttk.Label(frame_dep, text="Whisper: Verificando...")
    self.whisper_label.pack(anchor=tk.W)

    # Selector de archivo
    frame_file = ttk.Frame(self.window, padding="10")
    frame_file.pack(fill=tk.X)

    ttk.Label(frame_file, text="Archivo:").pack(side=tk.LEFT)
    ttk.Entry(frame_file, textvariable=self.input_file, width=50).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_file, text="Seleccionar", command=self.select_file).pack(side=tk.LEFT)

    # Selector de carpeta de salida
    frame_out = ttk.Frame(self.window, padding="10")
    frame_out.pack(fill=tk.X)

    ttk.Label(frame_out, text="Carpeta de salida:").pack(side=tk.LEFT)
    ttk.Entry(frame_out, textvariable=self.output_dir, width=40).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_out, text="Seleccionar", command=self.select_output_dir).pack(side=tk.LEFT)

    # Selección de idioma
    frame_lang = ttk.Frame(self.window, padding="10")
    frame_lang.pack(fill=tk.X)

    ttk.Label(frame_lang, text="Idioma:").pack(side=tk.LEFT)
    langs = ["es", "en", "fr", "de", "it", "pt"]
    ttk.Combobox(frame_lang, textvariable=self.language, values=langs).pack(side=tk.LEFT, padx=5)

    # Opción de traducción (al inglés)
    frame_trans = ttk.Frame(self.window, padding="10")
    frame_trans.pack(fill=tk.X)

    ttk.Checkbutton(frame_trans, text="Traducir al inglés", variable=self.translate).pack(side=tk.LEFT)

    # Botón de iniciar
    self.start_button = ttk.Button(self.window, text="Iniciar", command=self.process_file, state=tk.DISABLED)
    self.start_button.pack(pady=20)

  def update_dependencies_view(self):
    self.ffmpeg_label.config(
      text=f"FFmpeg: {'Instalado' if self.ffmpeg_installed.get() else 'No instalado'}"
    )
    self.whisper_label.config(
      text=f"Whisper: {'Instalado' if self.whisper_installed.get() else 'No instalado'}"
    )
    if self.ffmpeg_installed.get() and self.whisper_installed.get():
      self.start_button.config(state=tk.NORMAL)
    else:
      self.start_button.config(state=tk.DISABLED)

  def check_dependencies(self):
    self.ffmpeg_installed.set(self.is_ffmpeg_installed())
    self.whisper_installed.set(self.is_whisper_installed())
    self.update_dependencies_view()

    if not self.ffmpeg_installed.get():
      if messagebox.askyesno("Dependencia faltante", "FFmpeg no está instalado. ¿Desea instalarlo?"):
        self.install_ffmpeg()
        self.ffmpeg_installed.set(self.is_ffmpeg_installed())
        self.update_dependencies_view()

    if not self.whisper_installed.get():
      if messagebox.askyesno("Dependencia faltante", "Whisper no está instalado. ¿Desea instalarlo?"):
        self.install_whisper()
        self.whisper_installed.set(self.is_whisper_installed())
        self.update_dependencies_view()

  def is_ffmpeg_installed(self):
    try:
      subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, encoding="utf-8")
      return True
    except FileNotFoundError:
      return False

  def is_whisper_installed(self):
    try:
      subprocess.run(["whisper", "--help"], capture_output=True, text=True, encoding="utf-8")
      return True
    except FileNotFoundError:
      return False

  def install_ffmpeg(self):
    try:
      subprocess.run([
        "powershell.exe",
        "-Command",
        "Set-ExecutionPolicy Bypass -Scope Process -Force; "
        "[System.Net.ServicePointManager]::SecurityProtocol = "
        "[System.Net.ServicePointManager]::SecurityProtocol -bor 3072; "
        "iex ((New-Object System.Net.WebClient).DownloadString("
        "'https://community.chocolatey.org/install.ps1'))"
      ], capture_output=True, text=True, encoding="utf-8")

      subprocess.run(["choco", "install", "ffmpeg", "-y"], capture_output=True, text=True, encoding="utf-8")
      messagebox.showinfo("Éxito", "FFmpeg instalado correctamente")
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo instalar FFmpeg: {str(e)}")

  def install_whisper(self):
    try:
      subprocess.run(["choco", "install", "whisper-cli", "-y"], capture_output=True, text=True, encoding="utf-8")
      messagebox.showinfo("Éxito", "Whisper instalado correctamente")
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo instalar Whisper: {str(e)}")

  def select_file(self):
    file_path = filedialog.askopenfilename(
      filetypes=[
      ("Video files", "*.mp4 *.mkv *.avi"),
      ("Audio files", "*.mp3 *.wav *.ogg")
      ]
    )
    if file_path:
      self.input_file.set(file_path)

  def select_output_dir(self):
    dir_path = filedialog.askdirectory()
    if dir_path:
      self.output_dir.set(dir_path)

  def extract_audio(self, video_path):
    audio_path = str(Path(video_path).with_suffix(".mp3"))
    print(f"Extrayendo audio de: {video_path}")
    try:
      # Abrir ffmpeg en una terminal separada y esperar a que termine
      if sys.platform == "win32":
        # En Windows, usar start para abrir cmd y esperar
        cmd = [
          "cmd", "/c", "start", "/wait", "ffmpeg",
          "-i", video_path,
          "-vn",
          "-acodec", "mp3",
          audio_path
        ]
        subprocess.run(cmd)
      else:
        # En otros sistemas, abrir en xterm
        cmd = [
          "xterm", "-e", "ffmpeg",
          "-i", video_path,
          "-vn",
          "-acodec", "mp3",
          audio_path
        ]
        subprocess.run(cmd)
      print(f"Audio extraído en: {audio_path}")
      return audio_path
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo extraer el audio: {str(e)}")
      return None

  def transcribe_audio(self, audio_path, output_dir):
    args = [
      "whisper",
      audio_path,
      "--language", self.language.get(),
    ]
    if self.translate.get():
      args.extend(["--task", "translate"])
    args.extend(["--output_dir", output_dir])
    print(f"Transcribiendo audio: {audio_path}")
    print(f"Comando: {' '.join(args)}")
    try:
      # Ejecuta el comando en una terminal visible y espera a que termine
      if sys.platform == "win32":
        # En Windows, abrir cmd y esperar
        cmd = [
          "cmd", "/c", "start", "/wait", "whisper",
          audio_path,
          "--language", self.language.get(),
        ]
        if self.translate.get():
          cmd.extend(["--task", "translate"])
        cmd.extend(["--output_dir", output_dir])
        subprocess.run(cmd)
        print("Transcripción completada.")
        return True
      else:
        # En otros sistemas, abrir en xterm
        cmd = [
          "xterm", "-e", "whisper",
          audio_path,
          "--language", self.language.get(),
        ]
        if self.translate.get():
          cmd.extend(["--task", "translate"])
        cmd.extend(["--output_dir", output_dir])
        subprocess.run(cmd)
        print("Transcripción completada.")
        return True
    except Exception as e:
      messagebox.showerror("Error", f"No se pudo transcribir el audio: {str(e)}")
      return None

  def process_file(self):
    if not self.input_file.get():
      messagebox.showwarning("Advertencia", "Seleccione un archivo primero")
      return
    if not self.output_dir.get():
      messagebox.showwarning("Advertencia", "Seleccione la carpeta de salida")
      return

    file_path = self.input_file.get()
    output_dir = self.output_dir.get()

    print("==== INICIO DEL PROCESO ====")
    print(f"Archivo seleccionado: {file_path}")
    print(f"Carpeta de salida: {output_dir}")

    try:
      # Extraer audio si es un video
      if file_path.lower().endswith(('.mp4', '.mkv', '.avi')):
        audio_path = self.extract_audio(file_path)
        if audio_path:
          result = self.transcribe_audio(audio_path, output_dir)
          if result:
            messagebox.showinfo("Resultado", "Transcripción completada. Archivo guardado en la carpeta de salida.")
      else:
        result = self.transcribe_audio(file_path, output_dir)
        if result:
          messagebox.showinfo("Resultado", "Transcripción completada. Archivo guardado en la carpeta de salida.")
    finally:
      print("==== FIN DEL PROCESO ====")

  def cleanup_temp_files(self):
    temp_dir = Path(tempfile.gettempdir())
    for file in temp_dir.glob("*.mp3"):
      try:
        file.unlink()
      except OSError:
        pass

  def run(self):
    try:
      self.window.mainloop()
    finally:
      self.cleanup_temp_files()

if __name__ == "__main__":
  # Ejecutar el installer antes de lanzar la GUI
  try:
    from src.installer import main as installer_main
    installer_main()
  except Exception as e:
    print(f"Error ejecutando el installer: {e}")
  app = WhisperGUI()
  app.run()
