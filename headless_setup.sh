src=2019-09-26-raspbian-buster-lite.img
boot=/media/diarmuid/boot
rootfs=/media/diarmuid/rootfs
hostname=pisensor
ip=192.168.1.57

dd if=$src bs=4M | pv --size 4G | sudo dd of=/dev/sdi bs=4M
echo "Unplug sd card"
read varname

touch $boot/ssh
cat >$boot/wpa_supplicant.conf << EOF 
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=IE

network={
	ssid="LONGWOODPARKHIGHSPEED"
	psk="ANYLPDDN"
}
EOF
# Sudo su and run this
cat >>$rootfs/etc/dhcpcd.conf << EOF
interface wlan0
static ip_address=$ip/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.200

EOF

echo $hostname | sudo tee $rootfs/etc/hostname
cd
sudo umount $boot $rootfs

ssh pi@$ip
# Enable i2c
sudo raspi-config 
sudo apt update
sudo apt upgrade -y
sudo apt install -y git python i2c-tools python-pip samba python3-distutils vim
sudo smbpasswd -a pi
# Make user account writeablea
sudo vim /etc/samba/smb.conf 

sudo i2cdetect -y 1
git clone https://github.com/diarmuid/mqtt_client.git
cd mqtt_client
