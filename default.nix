let
  # Branche nixos-26.05 épinglée : build reproductible. Pour mettre à jour,
  # changer la révision puis recalculer le hash :
  # nix-prefetch-url --unpack "https://github.com/NixOS/nixpkgs/archive/<REV>.tar.gz"
  rev = "445d861c6d31b4af0c79d8d4be2331f762a361d7";
  pkgs = import (fetchTarball {
    url = "https://github.com/NixOS/nixpkgs/archive/${rev}.tar.gz";
    sha256 = "0x126xqaw6vqz27sp0w1vl58a90whrs9y7nsa1hkvr150y8j2m0w";
  }) {
    config = { allowUnfree = true; };
  };
in
  # Évaluation nixos complète (options système : specialisation, release…)
  (import (pkgs.path + "/nixos/lib/eval-config.nix") {
    inherit pkgs;
    modules = [
      ./iso.nix
      ./common.nix
    ];
  }).config.system.build.isoImage
