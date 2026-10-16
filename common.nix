{ config, pkgs, ... }:

let

  # Environnement Python dédié à marimo (applications de sciences physiques)
  marimoEnv = pkgs.python3.withPackages (ps: with ps; [
    marimo
    numpy
    scipy
    lmfit
    plotly
    pyserial
    anywidget
  ]);

  # Ki editor : version amont du flake officiel, sans patch. L'ISO live est
  # destinée à des claviers AZERTY (pas d'ergo-l), le fork ergol-layout du
  # poste de travail n'a donc pas lieu d'être ici.
  ki-editor = (builtins.getFlake "github:ki-editor/ki-editor/86fdfdf0f8923867b54cb1626ed988f1e01d8483").packages.${pkgs.stdenv.hostPlatform.system}.default;

  kitty-wrapped = pkgs.symlinkJoin {
    name = "kitty";
    paths = [ pkgs.kitty ];
    nativeBuildInputs = [ pkgs.makeWrapper ];
    postBuild = ''
      wrapProgram $out/bin/kitty --set LIBGL_ALWAYS_SOFTWARE 1
    '';
  };

  # Packages JupyterLab absents de nixpkgs, définis depuis PyPI
  jupyterPackagesExtra = ps: [
    (ps.buildPythonPackage rec {
      pname   = "jupyterlab-language-pack-fr-FR";
      version = "4.5.post3";
      format  = "wheel";
      src = pkgs.fetchurl {
        url  = "https://files.pythonhosted.org/packages/79/d2/b42fe09ae8001aa0ac56cdba19dafb25bbd44567b04361f6dcccf9055b39/jupyterlab_language_pack_fr_fr-4.5.post3-py2.py3-none-any.whl";
        hash = "sha256-n2zp1OZLNn/whKIxOvKdatigLR0IAA8+bFPihW+poR8=";
      };
      doCheck = false;
    })
    (ps.buildPythonPackage rec {
      pname   = "jupyterlab-spreadsheet-editor";
      version = "0.7.2";
      format  = "wheel";
      src = pkgs.fetchurl {
        url  = "https://files.pythonhosted.org/packages/51/0f/85269ae63f288d7f49f8626b8bcb165c2ccfe1414364440a9784ef5ba045/jupyterlab_spreadsheet_editor-0.7.2-py3-none-any.whl";
        hash = "sha256-SDnbbZxX69v0ylMHk1zbUFjPro+EvFMW8rWu1JjHo6I=";
      };
      doCheck = false;
    })
  ];
in

{
  nixpkgs.overlays = [
    (import ./tracker-pkg.nix)
  ];

  networking.hostName = "nixos";
  networking.networkmanager.enable = true;

  time.timeZone = "Europe/Paris";

  i18n.defaultLocale = "fr_FR.UTF-8";
  i18n.extraLocaleSettings = {
    LC_ADDRESS        = "fr_FR.UTF-8";
    LC_IDENTIFICATION = "fr_FR.UTF-8";
    LC_MEASUREMENT    = "fr_FR.UTF-8";
    LC_MONETARY       = "fr_FR.UTF-8";
    LC_NAME           = "fr_FR.UTF-8";
    LC_NUMERIC        = "fr_FR.UTF-8";
    LC_PAPER          = "fr_FR.UTF-8";
    LC_TELEPHONE      = "fr_FR.UTF-8";
    LC_TIME           = "fr_FR.UTF-8";
  };

  services.xserver.enable = true;
  services.xserver.displayManager.lightdm.enable = true;
  environment.etc."xdg/autostart/numlockx.desktop".text = ''
    [Desktop Entry]
    Type=Application
    Name=NumLock
    Exec=${pkgs.numlockx}/bin/numlockx on
    NoDisplay=true
    X-GNOME-Autostart-enabled=true
  '';
  services.xserver.desktopManager.cinnamon.enable = true;
  services.displayManager.autoLogin.enable = true;
  services.displayManager.autoLogin.user = "user";

  services.xserver.xkb = {
    layout = "fr";
    variant = "";
  };

  console.keyMap = "fr";

  services.printing.enable = true;

  services.samba = {
    enable = true;
    openFirewall = true;
    settings = {
      global = {
        "workgroup"    = "WORKGROUP";
        "server string" = "nixos";
        "security"     = "user";
        "guest account" = "nobody";
        "map to guest" = "bad user";
      };
      "Public" = {
        "path"           = "/home/user/Public";
        "browseable"     = "yes";
        "read only"      = "no";
        "guest ok"       = "yes";
        "create mask"    = "0644";
        "directory mask" = "0755";
      };
    };
  };

  systemd.tmpfiles.rules = [
    "d /home/user/Public 0755 user users -"
  ];

  services.pulseaudio.enable = false;
  security.rtkit.enable = true;
  services.pipewire = {
    enable = true;
    alsa.enable = true;
    alsa.support32Bit = true;
    pulse.enable = true;
  };

  security.sudo.wheelNeedsPassword = false;

  users.users.user = {
    isNormalUser = true;
    description = "user";
    password = "";
    extraGroups = [ "networkmanager" "wheel" "audio" "video" "dialout" ];
    createHome = false;
  };

  # Kitty comme terminal par défaut dans Cinnamon + pas de veille/verrouillage
  environment.sessionVariables.TERMINAL = "kitty";

  programs.dconf.enable = true;
  environment.etc."dconf/db/local.d/00-terminal".text = ''
    [org/cinnamon/desktop/default-applications/terminal]
    exec='${kitty-wrapped}/bin/kitty'
    exec-arg='''
  '';

  # PDF : ouverture par défaut avec le visionneur de documents Xreader
  # (fourni par Cinnamon) plutôt qu'avec LibreOffice Draw, qui s'enregistre
  # lui aussi pour application/pdf et gagnait sinon l'association.
  xdg.mime.defaultApplications."application/pdf" = "xreader.desktop";

  # Désactiver veille et verrouillage au niveau Cinnamon
  environment.etc."dconf/db/local.d/01-power".text = ''
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
  '';

  # Nemo : affichage en liste par défaut
  environment.etc."dconf/db/local.d/02-nemo".text = ''
    [org/nemo/preferences]
    default-folder-viewer='list-view'
  '';

  # Raccourcis dans la barre des tâches (côté gauche)
  environment.etc."dconf/db/local.d/03-panel".text = ''
    [org/cinnamon]
    panels-autohide = ['1:intel']
    enabled-applets = ['panel1:left:0:menu@cinnamon.org', 'panel1:left:1:separator@cinnamon.org', 'panel1:left:2:grouped-window-list@cinnamon.org:3', 'panel1:right:0:systray@cinnamon.org', 'panel1:right:1:xapp-status@cinnamon.org', 'panel1:right:2:notifications@cinnamon.org', 'panel1:right:3:printers@cinnamon.org', 'panel1:right:4:removable-drives@cinnamon.org', 'panel1:right:5:keyboard@cinnamon.org', 'panel1:right:6:network@cinnamon.org', 'panel1:right:7:sound@cinnamon.org', 'panel1:right:8:power@cinnamon.org', 'panel1:right:9:calendar@cinnamon.org:9', 'panel1:right:10:cornerbar@cinnamon.org']
  '';

  # Désactiver DPMS et blanking au niveau X11
  services.xserver.extraConfig = ''
    Section "ServerFlags"
      Option "BlankTime"   "0"
      Option "StandbyTime" "0"
      Option "SuspendTime" "0"
      Option "OffTime"     "0"
    EndSection
  '';

  # allowUnfree est passé à l'import du nixpkgs (default.nix) : l'instance
  # pkgs étant externe à l'évaluation nixos, l'option nixpkgs.config
  # provoquerait une assertion du module système.

  environment.systemPackages = with pkgs; [
    appimage-run
    kitty-wrapped
    (pkgs.writeShellScriptBin "x-terminal-emulator" ''exec kitty "$@"'')
    ki-editor
    yazi
    typst
    tinymist
    arduino-ide
    geogebra6
    libreoffice-fresh
    audacity
    git
    wget
    gparted
    curl
    fritzing
    gromit-mpx
    vlc
    # marimo : environnement Python pour les applications de sciences physiques
    marimoEnv
    # JupyterLab dans un environnement Python complet
    (python3.withPackages (ps: with ps; [
      jupyterlab
      # Calcul scientifique
      numpy
      scipy
      matplotlib
      lmfit
      # Widgets interactifs et backend matplotlib (%matplotlib widget)
      ipywidgets
      ipympl
      # Graphiques interactifs Plotly (FigureWidget temps réel) : anywidget
      # est requis par plotly 6 pour le rendu FigureWidget dans JupyterLab.
      plotly
      anywidget
      # Communication série Arduino
      pyserial
      # Utilitaires notebooks
      nbformat
      nbconvert
      # Interface en français + éditeur CSV (définis via PyPI ci-dessus)
    ] ++ jupyterPackagesExtra ps))
    tracker
    (pkgs.makeDesktopItem {
      name = "tracker";
      desktopName = "Tracker";
      exec = "tracker";
      categories = [ "Education" "Science" ];
      comment = "Video Analysis and Modeling Tool";
    })
  ];

  programs.firefox = {
    enable = true;
    policies = {
      DisplayBookmarksToolbar = "always";
      TranslateEnabled        = false;
      DisableTelemetry        = true;
      DisableFirefoxStudies   = true;
      DisableAppUpdate        = true;
      Preferences = {
        "browser.sessionstore.resume_from_crash" = { Value = false; Status = "locked"; };
      };
      OverrideFirstRunPage    = "";
      OverridePostUpdatePage  = "";
      DefaultSearchEngine     = "DuckDuckGo";
      Homepage = {
        URL    = "https://henri-iv-beziers.mon-ent-occitanie.fr/";
        Locked = true;
      };
      ManagedBookmarks = [
        { name = "TableauNoir";      url = "https://tableaunoir.github.io/"; }
        { name = "LeLivreScolaire";  url = "https://lelivrescolaire.fr"; }
        { name = "Tracker";          url = "https://opensourcephysics.github.io/tracker-online/index_ff.html"; }
        { name = "JupyterLab";       url = "https://mybinder.org/v2/gh/physique-henriiv/fichiers_python/main?urlpath=lab"; }
        { name = "TI83";             url = "https://maclasseti.fr/calculatrice"; }
        { name = "numworks";         url = "https://www.numworks.com/fr/emulateur/graphique/"; }
        { name = "mathGraph+";       url = "https://casio-education.eu/fr/calculatrices-en-ligne"; }
        { name = "Geogebra";         url = "https://www.geogebra.org/calculator"; }
        { name = "Framacalc";        url = "https://framacalc.org/abc/fr/"; }
        { name = "Livechart";        url = "https://nds.iaea.org/relnsd/vcharthtml/VChartHTML.html"; }
        { name = "PTable";           url = "https://ptable.com/?lang=fr#Propriétés"; }
        { name = "Ephemerides";      url = "https://ssp.imcce.fr/forms"; }
        { name = "Labolycee";        url = "https://labolycee.org"; }
        { name = "Chrono";           url = "https://www.online-stopwatch.com/french/"; }
        { name = "Molview";          url = "https://app.molview.com"; }
        { name = "Chemix";           url = "https://chemix.org"; }
        { name = "Cristallographie"; url = "https://www.rruff.net"; }
        { name = "Phet";             url = "https://phet.colorado.edu/fr/simulations/browse"; }
        { name = "Ostralo";          url = "https://www.ostralo.net"; }
      ];
    };
  };
}
