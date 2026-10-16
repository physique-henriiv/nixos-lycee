# Tracker 6.3.5 — outil d'analyse et de modélisation vidéo (Open Source Physics).
#
# Non empaqueté dans nixpkgs. Emballage à partir de la jar officielle (9,7 Mo) +
# moteur vidéo Xuggle (natives Linux x86_64 embarquées) + jars logback/slf4j
# requises par Xuggle, le tout lancé par le JRE Temurin 21.
# Attention : Xuggle embarque un ffmpeg statique ancien ; s'il pose problème à
# l'exécution, seul l'affichage des images restera possible sans moteur vidéo.
final: prev:
let
  base =
    "https://raw.githubusercontent.com/OpenSourcePhysics/video-engines/3201ef5fa54043d763617e92bc41cae8041d49d4/libraries";

  src = prev.fetchurl {
    url =
      "https://opensourcephysics.github.io/tracker-website/archives/tracker-6.3.5.jar";
    sha256 = "3b655f4370613afa5c4224c8e2e435d21a1f1fdcc28274937890feb90e1460d0";
  };

  xuggle = prev.fetchurl {
    url = "${base}/xuggle-xuggler.jar";
    sha256 = "98d2a7429e7229c9c3c0dd30e9e484568596ab45112847f2d25b6f38045406fa";
  };

  slf4j = prev.fetchurl {
    url = "${base}/slf4j-api.jar";
    sha256 = "1212418dbc2cc148e221f52a8f3027e8b96e0a05eb93048498e9d5210e518fa9";
  };

  logback-classic = prev.fetchurl {
    url = "${base}/logback-classic.jar";
    sha256 = "252796054cf529d76d37f33cd3f5677f65599c238a7cea9f35862b3935d3f6e1";
  };

  logback-core = prev.fetchurl {
    url = "${base}/logback-core.jar";
    sha256 = "3e22c0389824fa20282a1eb93ee179c21916e01ed2583583392d14e15389a9b3";
  };
in {
  tracker = prev.stdenv.mkDerivation {
    pname = "tracker";
    version = "6.3.5";

    inherit src xuggle;

    nativeBuildInputs = [ prev.makeWrapper ];

    dontUnpack = true;
    dontBuild = true;

    installPhase = ''
      runHook preInstall
      mkdir -p $out/share/tracker
      install ${src} $out/share/tracker/tracker.jar
      install ${xuggle} $out/share/tracker/xuggle-xuggler.jar
      install ${slf4j} $out/share/tracker/slf4j-api.jar
      install ${logback-classic} $out/share/tracker/logback-classic.jar
      install ${logback-core} $out/share/tracker/logback-core.jar
      runHook postInstall
    '';

    postFixup = ''
      makeWrapper ${prev.temurin-jre-bin-21}/bin/java $out/bin/tracker \
        --prefix PATH : ${prev.temurin-jre-bin-21}/bin \
        --prefix LD_LIBRARY_PATH : ${prev.stdenv.cc.cc.lib}/lib \
        --set DISPLAY :0 \
        --set NEW_INSTALL 1 \
        --add-flags "-cp $out/share/tracker/tracker.jar:$out/share/tracker/xuggle-xuggler.jar:$out/share/tracker/slf4j-api.jar:$out/share/tracker/logback-classic.jar:$out/share/tracker/logback-core.jar" \
        --add-flags "-Dswing.defaultlaf=javax.swing.plaf.nimbus.NimbusLookAndFeel" \
        --add-flags "--add-opens=java.base/java.lang=ALL-UNNAMED" \
        --add-flags "--add-opens=java.desktop/java.awt=ALL-UNNAMED" \
        --add-flags "org.opensourcephysics.cabrillo.tracker.Tracker"
    '';

    meta = {
      description =
        "Tracker : outil gratuit d'analyse et de modelisation video (Open Source Physics)";
      homepage = "https://opensourcephysics.github.io/tracker-website/";
      license = prev.lib.licenses.gpl3Plus;
      platforms = [ "x86_64-linux" ];
      mainProgram = "tracker";
    };
  };
}