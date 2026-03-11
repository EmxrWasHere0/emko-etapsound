systemctl --user stop pipewire.socket pipewire-pulse.socket wireplumber
systemctl --user mask pipewire.service pipewire.socket pipewire-pulse.service pipewire-pulse.socket wireplumber.service

sudo apt install pulseaudio

systemctl --user unmask pulseaudio.service pulseaudio.socket
systemctl --user enable pulseaudio.service pulseaudio.socket

sudo sed -i 's/load-module module-udev-detect/load-module module-udev-detect tsched=0/g' /etc/pulse/default.pa

rm -rf ~/.config/pulse

sudo sed -i 's/; autospawn = yes/autospawn = yes/g' /etc/pulse/client.conf

pactl info 