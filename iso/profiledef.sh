#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="lumen"
iso_label="LUMEN_ALPHA"
iso_publisher="Lumen Project <https://github.com/lumen-os/lumen>"
iso_application="Lumen Live/Installation CD"
install_dir="lumen"
buildmodes=('iso')
bootmodes=('bios.syslinux' 'uefi.grub')
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86')
file_permissions=(
  ["/usr/bin/lumen-overlay"]="0:0:755"
)
