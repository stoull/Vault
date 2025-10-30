#!/bin/bash
read -s -p "Enter sudo password: " PASSWORD
echo
scp ~/Downloads/ahut.site_nginx.zip hut@ahut.site:~/
ssh hut@ahut.site "cd ~; SUDO_PASSWORD=$PASSWORD ./scripts/update_nginx_cert.sh;"
unset SUDO_PASSWORD
ssh