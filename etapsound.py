import subprocess
import socket
import sys

def run_cmd(step_text, command, shell=False):
    """Komutu çalıştırır, hata varsa programı kapatır."""
    print(f"{step_text}...")
    # shell=True karmaşık komutlar (sed, && vb.) için gerekli
    result = subprocess.run(command, capture_output=True, shell=shell, text=True)
    
    if result.returncode != 0:
        print(f"\nHATA: {step_text} başarısız oldu!")
        print(f"Detay: {result.stderr.strip()}")
        input("\nÇıkmak için [ENTER] tuşuna basın.")
        sys.exit(1)
    return result

def main():
    print("""
        ==============================
        =====   EMKO-ETAPSound   =====
        ==============================\n""")

    # 1. Sistem Kontrolü
    if socket.gethostname() != "pardus":
        print("Bu yazılım sadece Pardus cihazlarda çalışır.")
        input("Çıkmak için [ENTER] tuşuna basın.")
        return

    # 2. İnternet Kontrolü (URL değil sadece domain yazılır)
    run_cmd("İnternet bağlantısı kontrol ediliyor", "ping -c 2 depo.pardus.org.tr")

    print("EMKO-ETAPSound Çalıştırılıyor...\n" + "="*42)

    # 3. Sıralı Komut Listesi (Adım Adı, Komut)
    steps = [
        ("Sürücüler durduruluyor", "systemctl --user stop pipewire.socket pipewire-pulse.socket wireplumber"),
        ("Kütüphaneler maskeleniyor", "systemctl --user mask pipewire.service pipewire.socket pipewire-pulse.service pipewire-pulse.socket wireplumber.service"),
        ("[SUDO] PulseAudio indiriliyor", "sudo apt install -y pulseaudio"),
        ("Sürücülerin maskesi kaldırılıyor", "systemctl --user unmask pulseaudio.service pulseaudio.socket"),
        ("Sürücüler etkinleştiriliyor", "systemctl --user enable pulseaudio.service pulseaudio.socket"),
        ("Lokal dosyalar yapılandırılıyor", "sudo sed -i 's/load-module module-udev-detect/load-module module-udev-detect tsched=0/g' /etc/pulse/default.pa && rm -rf ~/.config/pulse && sudo sed -i 's/; autospawn = yes/autospawn = yes/g' /etc/pulse/client.conf")
    ]

    # Tüm adımları döngüyle çalıştır
    for step_name, command in steps:
        run_cmd(step_name, command, shell=True)

    print("\nEMKO-ETAPSound sihirbazı tamamlandı. PulseAudio bilgileri yazdırılıyor.")
    subprocess.run("pactl info", shell=True)
    input("\nBitti! Çıkmak için [ENTER] tuşuna basın.")

if __name__ == "__main__":
    main()