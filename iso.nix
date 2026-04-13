{ config, pkgs, lib, ... }:

let
  # ---------------------------------------------------------------------------
  # Fichiers de configuration des applications (pas d'écran d'accueil/MAJ)
  # ---------------------------------------------------------------------------

  # ---------------------------------------------------------------------------
  # Base dconf binaire pré-compilée pour l'utilisateur
  # (prioritaire sur la base système, garantit l'application sur live USB)
  # ---------------------------------------------------------------------------
  dconfKeyfile = pkgs.writeText "dconf-cinnamon-settings" ''
    [org/cinnamon]
    panels-autohide=['1:intel']
    enabled-applets=['panel1:left:0:menu@cinnamon.org', 'panel1:left:1:separator@cinnamon.org', 'panel1:left:2:grouped-window-list@cinnamon.org:3', 'panel1:right:0:systray@cinnamon.org', 'panel1:right:1:xapp-status@cinnamon.org', 'panel1:right:2:notifications@cinnamon.org', 'panel1:right:3:printers@cinnamon.org', 'panel1:right:4:removable-drives@cinnamon.org', 'panel1:right:5:keyboard@cinnamon.org', 'panel1:right:6:network@cinnamon.org', 'panel1:right:7:sound@cinnamon.org', 'panel1:right:8:power@cinnamon.org', 'panel1:right:9:calendar@cinnamon.org:9', 'panel1:right:10:cornerbar@cinnamon.org']

    [org/cinnamon/desktop/session]
    idle-delay=uint32 0

    [org/cinnamon/desktop/screensaver]
    idle-activation-enabled=false
    lock-enabled=false

    [org/cinnamon/settings-daemon/plugins/power]
    sleep-display-ac=0
    sleep-display-battery=0
    idle-dim-ac=false
    idle-dim-battery=false

    [org/nemo/preferences]
    default-folder-viewer='list-view'
  '';

  dconfDb = pkgs.runCommand "dconf-user-db" {
    nativeBuildInputs = [ pkgs.dconf ];
  } ''
    mkdir keyfiles
    cp ${dconfKeyfile} keyfiles/cinnamon
    dconf compile $out keyfiles/
  '';

  libreofficeReg = pkgs.writeText "libreoffice-registrymodifications.xcu" ''
    <?xml version="1.0" encoding="UTF-8"?>
    <oor:items xmlns:oor="http://openoffice.org/2001/registry"
               xmlns:xs="http://www.w3.org/2001/XMLSchema"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
      <!-- Désactiver le job de vérification de mise à jour -->
      <item oor:path="/org/openoffice/Office/Jobs/Jobs/com.sun.star.office.Jobs:Name='UpdateCheck'">
        <prop oor:name="Active" oor:op="fuse">
          <value xsi:type="xs:boolean">false</value>
        </prop>
      </item>
      <!-- Marquer l'assistant premier lancement comme terminé -->
      <item oor:path="/org/openoffice/Setup/Office">
        <prop oor:name="FirstStartWizardCompleted" oor:op="fuse">
          <value xsi:type="xs:boolean">true</value>
        </prop>
      </item>
    </oor:items>
  '';

  audacityCfg = pkgs.writeText "audacity.cfg" ''
    [GUI]
    ShowSplashScreen=0
    WelcomeScreenLastVersion=3.7.7
  '';

  # Arduino IDE 2 : désactiver la vérification automatique de mise à jour
  arduinoSettings = pkgs.writeText "arduino-ide-settings.json" ''
    {
      "arduino.ide.autoCheckForUpdates": false,
      "arduino.checkForUpdates": false
    }
  '';

  # ---------------------------------------------------------------------------
  # Contenu de /home/user
  # ---------------------------------------------------------------------------
  homeDir = pkgs.runCommand "home-user" { } ''
    mkdir -p $out

    cp -r ${./fichiers_arduino} $out/fichiers_arduino
    cp -r ${./fichiers_python}  $out/fichiers_python

    mkdir -p $out/Videos
    cp -r ${./videos_relatif}          $out/Videos/videos_relatif
    cp -r ${./videos_vecteurs_vitesse} $out/Videos/videos_vecteurs_vitesse

    mkdir -p $out/.config/dconf
    cp ${dconfDb} $out/.config/dconf/user

    mkdir -p $out/.config
    cp -r ${./.config/helix} $out/.config/helix
    cp -r ${./.config/kitty} $out/.config/kitty
    cp -r ${./.config/yazi}  $out/.config/yazi

    # LibreOffice : pas de mise à jour, pas d'assistant premier lancement
    mkdir -p "$out/.config/libreoffice/4/user"
    cp ${libreofficeReg} "$out/.config/libreoffice/4/user/registrymodifications.xcu"

    # Audacity : pas d'écran de bienvenue
    mkdir -p "$out/.config/audacity"
    cp ${audacityCfg} "$out/.config/audacity/audacity.cfg"

    # Arduino IDE : pas de vérification de mise à jour
    mkdir -p "$out/.config/arduino-ide"
    cp ${arduinoSettings} "$out/.config/arduino-ide/settings.json"

    # Taskbar : apps épinglées
    mkdir -p "$out/.config/cinnamon/spices/grouped-window-list@cinnamon.org"
    echo '{"pinned-apps":{"type":"generic","value":["nemo.desktop","firefox.desktop","kitty.desktop","audacity.desktop","arduino-ide.desktop","calc.desktop","jupyterlab.desktop"]}}' \
      > "$out/.config/cinnamon/spices/grouped-window-list@cinnamon.org/3.json"

    # Horloge Cinnamon : format personnalisé
    mkdir -p "$out/.config/cinnamon/spices/calendar@cinnamon.org"
    echo '{"use-custom-format":{"type":"switch","value":true},"custom-format":{"type":"entry","value":"%A %e %B, %H:%M:%S"}}' \
      > "$out/.config/cinnamon/spices/calendar@cinnamon.org/9.json"

    # JupyterLab : répertoire de démarrage
    mkdir -p "$out/.jupyter"
    echo 'c.ServerApp.root_dir = "/home/user/fichiers_python"' \
      > "$out/.jupyter/jupyter_server_config.py"

    # JupyterLab : langue fr_FR, pas d'annonces ni de mise à jour
    mkdir -p "$out/.local/share/jupyter/lab/user-settings/@jupyterlab/translation-extension"
    echo '{ "locale": "fr_FR" }' \
      > "$out/.local/share/jupyter/lab/user-settings/@jupyterlab/translation-extension/plugin.jupyterlab-settings"

    mkdir -p "$out/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension"
    echo '{ "fetchNews": "false", "checkForUpdates": false }' \
      > "$out/.local/share/jupyter/lab/user-settings/@jupyterlab/apputils-extension/announcements.jupyterlab-settings"
  '';
in
{
  imports = [
    <nixpkgs/nixos/modules/installer/cd-dvd/iso-image.nix>
    ./common.nix
  ];

  boot.loader.timeout = lib.mkForce 0;

  # Support matériel universel (machines différentes, GPU variés)
  hardware.enableRedistributableFirmware = true;
  services.xserver.videoDrivers = [ "modesetting" "fbdev" ];
  boot.initrd.kernelModules = [ "amdgpu" "i915" ];

  isoImage.makeEfiBootable     = true;
  isoImage.makeUsbBootable     = true;
  image.fileName               = "henriiv-live.iso";
  isoImage.squashfsCompression = "zstd -Xcompression-level 19";

  # Peuple /home/user depuis le store Nix à chaque démarrage.
  # Comme la racine est un overlayfs (tmpfs), tout repart à zéro à l'extinction.
  systemd.services.populate-home = {
    description = "Populate /home/user with default content";
    wantedBy    = [ "multi-user.target" ];
    before      = [ "display-manager.service" ];
    after       = [ "local-fs.target" ];
    serviceConfig = {
      Type            = "oneshot";
      RemainAfterExit = true;
    };
    script = ''
      rm -rf /home/user
      cp -r ${homeDir} /home/user
      chmod -R u+rwX /home/user
      chown -R user:users /home/user
    '';
  };

  system.stateVersion = "25.11";
}
