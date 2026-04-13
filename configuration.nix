{ config, pkgs, ... }:

{
  imports = [
    ./hardware-configuration.nix
    ./common.nix
  ];

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;

  system.stateVersion = "25.11";
}
