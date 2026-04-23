#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="lumen"
iso_label="LUMEN_$(date +%Y%m)"
iso_publisher="Lumen Project <https://github.com/lumen-os/lumen>"
iso_application="Lumen Live/Installation CD"
install_dir="lumen"
buildmodes=('iso')
bootmodes=('bios.syslinux.mbr' 'bios.syslinux.eltorito' 'uefi-ia32.grub.esp' 'uefi-x64.grub.esp' 'uefi-ia32.grub.eltorito' 'uefi-x64.grub.eltorito')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86')
file_permissions=(
  ["/etc/shadow"]="0:0:400"
  ["/root"]="0:0:750"
  ["/root/.automated_script.sh"]="0:0:755"
  ["/usr/local/bin/choose-mirror"]="0:0:755"
  ["/usr/local/bin/Installation_Guide"]="0:0:755"
  ["/usr/local/bin/livecd-sound"]="0:0:755"
)
