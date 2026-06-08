let
  pkgs = import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-26.05.tar.gz") {};
in
  (pkgs.lib.evalModules {
    modules = [ 
      ./iso.nix 
      ({ config, pkgs, lib, ... }: {
        system.nixos.release = "26.05";
      })
    ];
    args = { 
      inherit pkgs; 
    };
  }).config.system.build.isoImage













