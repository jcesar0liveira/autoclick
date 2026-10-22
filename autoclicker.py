import threading
import time
import tkinter as tk
from pynput import keyboard
import pyautogui


class AutoClickerApp:

  def __init__(self, root):
    self.root = root
    self.root.title("Auto Clicker [PARADO]")
    self.root.geometry("320x330")
    self.root.resizable(False, False)

    self.running = False

    # Instrução visual
    self.instruction_label = tk.Label(
        root,
        text=(
            "Defina suas teclas de atalho:\n(Ex: f6, f7, space, a, b, etc.)"
        ),
        fg="#0056b3",
        font=("Arial", 9, "bold"),
    )
    self.instruction_label.pack(pady=8)

    # Campo Tecla Iniciar
    self.lbl_start = tk.Label(root, text="Tecla para INICIAR:")
    self.lbl_start.pack(pady=1)
    self.entry_start = tk.Entry(root, justify="center")
    self.entry_start.insert(0, "f6")  # Padrão F6 para iniciar
    self.entry_start.pack(pady=2)

    # Campo Tecla Parar
    self.lbl_stop = tk.Label(root, text="Tecla para PARAR:")
    self.lbl_stop.pack(pady=1)
    self.entry_stop = tk.Entry(root, justify="center")
    self.entry_stop.insert(0, "f7")  # Padrão F7 para parar
    self.entry_stop.pack(pady=2)

    # Campo de Intervalo
    self.label = tk.Label(root, text="Intervalo entre cliques (segundos):")
    self.label.pack(pady=1)
    self.entry_interval = tk.Entry(root, justify="center")
    self.entry_interval.insert(0, "0.1")
    self.entry_interval.pack(pady=2)

    # Botões manuais
    self.start_btn = tk.Button(
        root,
        text="Iniciar",
        command=self.start_clicking,
        bg="#28a745",
        fg="white",
        width=16,
        font=("Arial", 9, "bold"),
    )
    self.start_btn.pack(pady=2)

    self.stop_btn = tk.Button(
        root,
        text="Parar",
        command=self.stop_clicking,
        bg="#dc3545",
        fg="white",
        width=16,
        font=("Arial", 9, "bold"),
    )
    self.stop_btn.pack(pady=2)

    pyautogui.FAILSAFE = True

    # Inicializa o ouvinte global de teclado
    self.listener = keyboard.Listener(on_press=self.on_press)
    self.listener.daemon = True
    self.listener.start()

  def matches_key(self, key, key_str):
    key_str = key_str.strip().lower()
    if not key_str:
      return False
    try:
      # Verifica se é uma tecla especial (f1-f12, space, etc.)
      special_key = getattr(keyboard.Key, key_str, None)
      if special_key and key == special_key:
        return True
    except AttributeError:
      pass

    # Verifica se é uma letra ou número comum
    if hasattr(key, "char") and key.char and key.char.lower() == key_str:
      return True
    return False

  def on_press(self, key):
    try:
      start_key = self.entry_start.get()
      stop_key = self.entry_stop.get()

      if self.matches_key(key, start_key):
        if not self.running:
          self.root.after(0, self.start_clicking)
      elif self.matches_key(key, stop_key):
        if self.running:
          self.root.after(0, self.stop_clicking)
    except Exception as e:
      print(f"Erro no atalho: {e}")

  def click_loop(self):
    try:
      interval = float(self.entry_interval.get())
    except ValueError:
      interval = 0.1

    while self.running:
      pyautogui.click()
      time.sleep(interval)

  def start_clicking(self):
    if not self.running:
      self.running = True
      self.thread = threading.Thread(target=self.click_loop)
      self.thread.daemon = True
      self.thread.start()
      self.root.title("Auto Clicker [RODANDO]")

  def stop_clicking(self):
    self.running = False
    self.root.title("Auto Clicker [PARADO]")


if __name__ == "__main__":
  root = tk.Tk()
  app = AutoClickerApp(root)
  root.mainloop()