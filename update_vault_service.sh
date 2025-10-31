#!/bin/bash
read -s -p "Enter sudo password: " PASSWORD
echo
ssh hut@ahut.site "cd ~; SUDO_PASSWORD=$PASSWORD ./scripts/update_vault_service.sh;"
unset $PASSWORD
