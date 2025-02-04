import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import psutil
import time
import os
from datetime import datetime
import webbrowser
import random
import threading
import customtkinter as ctk

class MonitorizareLaptop:
    def __init__(self):
        # Setări customtkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Creare fereastră principală
        self.root = ctk.CTk()
        self.root.title("Monitorizare Laptop - Creat de Alecs")
        self.root.geometry("900x700")
        
        # Variabile pentru monitorizare
        self.running = True
        self.monitoring_thread = None
        self.volume_max = True
        self.clock_running = True
        self.color_animation_running = True
        
        # Creare interfață
        self.create_gui()
        
        # Pornire monitorizare, ceas și animație
        self.start_monitoring()
        self.update_clock()
        self.animate_author_color()

    def create_gui(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame pentru ceas digital
        clock_frame = ctk.CTkFrame(self.main_frame, fg_color="#2B2B2B")
        clock_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Label pentru dată
        self.date_label = ctk.CTkLabel(clock_frame, 
                                     text="", 
                                     font=("Consolas", 24, "bold"))
        self.date_label.pack(pady=2)
        
        # Label pentru ceas
        self.clock_label = ctk.CTkLabel(clock_frame, 
                                      text="", 
                                      font=("Consolas", 48, "bold"))
        self.clock_label.pack(pady=2)

        # Titlu și autor
        title_frame = ctk.CTkFrame(self.main_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title = ctk.CTkLabel(title_frame, 
                            text="Monitorizare Sistem",
                            font=("Helvetica", 24, "bold"))
        title.pack(pady=5)
        
        # Label pentru autor cu animație
        self.author_label = ctk.CTkLabel(title_frame,
                                       text="Creat de Alecs",
                                       font=("Helvetica", 24, "bold"))
        self.author_label.configure(text_color="#FF0000")  # Culoare inițială roșie
        self.author_label.pack(pady=10)

        # Frame pentru informații sistem
        info_frame = ctk.CTkFrame(self.main_frame)
        info_frame.pack(fill=tk.X, padx=10, pady=5)

        # Informații baterie
        self.battery_label = ctk.CTkLabel(info_frame, 
                                        text="Baterie: Verificare...",
                                        font=("Helvetica", 14))
        self.battery_label.pack(pady=5)

        # Informații RAM
        self.ram_label = ctk.CTkLabel(info_frame, 
                                    text="RAM: Verificare...",
                                    font=("Helvetica", 14))
        self.ram_label.pack(pady=5)

        # Frame pentru butoane
        button_frame = ctk.CTkFrame(self.main_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=10)

        # Butoane
        ctk.CTkButton(button_frame, 
                     text="Verifică Sistem",
                     command=self.check_system,
                     font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(button_frame, 
                     text="Redă Muzică",
                     command=self.play_music,
                     font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)
        
        # Buton pentru control volum
        self.volume_button = ctk.CTkButton(button_frame, 
                                         text="Volum MAX",
                                         command=self.toggle_volume,
                                         font=("Helvetica", 12))
        self.volume_button.pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(button_frame, 
                     text="Curăță Log",
                     command=self.clear_log,
                     font=("Helvetica", 12)).pack(side=tk.LEFT, padx=5)

        # Frame pentru log
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Zonă de log
        self.log_area = scrolledtext.ScrolledText(log_frame, 
                                                height=10,
                                                font=("Consolas", 11),
                                                bg="#2B2B2B",
                                                fg="#FFFFFF")
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def animate_author_color(self):
        if self.color_animation_running:
            # Alternează între roșu și verde
            current_color = "#FF0000" if self.author_label.cget("text_color") == "#00FF00" else "#00FF00"
            self.author_label.configure(text_color=current_color)
            self.root.after(1000, self.animate_author_color)

    def update_clock(self):
        if self.clock_running:
            current_time = datetime.now()
            
            # Formatează data și ora în română
            time_string = current_time.strftime("%H:%M:%S")
            date_string = current_time.strftime("%d %B %Y").replace(
                "January", "Ianuarie").replace(
                "February", "Februarie").replace(
                "March", "Martie").replace(
                "April", "Aprilie").replace(
                "May", "Mai").replace(
                "June", "Iunie").replace(
                "July", "Iulie").replace(
                "August", "August").replace(
                "September", "Septembrie").replace(
                "October", "Octombrie").replace(
                "November", "Noiembrie").replace(
                "December", "Decembrie")
            
            self.clock_label.configure(text=time_string)
            self.date_label.configure(text=date_string)
            
            self.root.after(1000, self.update_clock)

    def toggle_volume(self):
        try:
            if self.volume_max:
                os.system("powershell (Get-WmiObject -Class Win32_SoundDevice).SetVolume(20)")
                self.volume_button.configure(text="Volum MIN")
                self.update_log("Volum setat la 20%")
            else:
                os.system("powershell (Get-WmiObject -Class Win32_SoundDevice).SetVolume(100)")
                self.volume_button.configure(text="Volum MAX")
                self.update_log("Volum setat la 100%")
            
            self.volume_max = not self.volume_max
        except Exception as e:
            self.update_log(f"Eroare control volum: {str(e)}")
            messagebox.showerror("Eroare", "Nu s-a putut modifica volumul")

    def play_music(self):
        try:
            melodii = [
                "https://www.youtube.com/watch?v=nsI3pevjryw&list=PL2205E90B31FB3818",  # Sofia Vicoveanca
            ]
            melodie = random.choice(melodii)
            
            # Setează volumul la maxim
            os.system("powershell (Get-WmiObject -Class Win32_SoundDevice).SetVolume(100)")
            self.volume_max = True
            self.volume_button.configure(text="Volum MAX")
            
            webbrowser.open(melodie)
            self.update_log("Melodie populară pornită cu volum maxim")
        except Exception as e:
            self.update_log(f"Eroare redare muzică: {str(e)}")

    def update_log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_area.insert(tk.END, f"{timestamp} [Alecs System]: {message}\n")
        self.log_area.see(tk.END)

    def check_system(self):
        self.check_battery()
        self.check_ram()
        self.update_log("Verificare sistem completă")

    def check_battery(self):
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                power = "Conectat" if battery.power_plugged else "Pe baterie"
                status = f"Baterie: {percent}% ({power})"
                self.battery_label.configure(text=status)
                self.update_log(f"Nivel baterie: {percent}%")
        except Exception as e:
            self.update_log(f"Eroare verificare baterie: {str(e)}")

    def check_ram(self):
        try:
            ram = psutil.virtual_memory()
            status = f"RAM: {ram.percent}% utilizat"
            self.ram_label.configure(text=status)
            self.update_log(f"Utilizare RAM: {ram.percent}%")
        except Exception as e:
            self.update_log(f"Eroare verificare RAM: {str(e)}")

    def clear_log(self):
        self.log_area.delete(1.0, tk.END)
        self.update_log("Log curățat")

    def start_monitoring(self):
        def monitor():
            while self.running:
                self.check_system()
                time.sleep(300)  # Verifică la fiecare 5 minute

        self.monitoring_thread = threading.Thread(target=monitor, daemon=True)
        self.monitoring_thread.start()

    def on_closing(self):
        if messagebox.askokcancel("Monitorizare Laptop - Alecs", "Sigur vrei să închizi aplicația?"):
            self.running = False
            self.clock_running = False
            self.color_animation_running = False
            self.root.destroy()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    print("Aplicație creată de Alecs")
    print("Inițializare sistem...")
    app = MonitorizareLaptop()
    app.run()