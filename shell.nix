# shell.nix
let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.beautifulsoup4
      python-pkgs.dash
      python-pkgs.google-cloud-storage
      python-pkgs.matplotlib
      python-pkgs.notebook
      python-pkgs.numpy
      python-pkgs.pandas
      python-pkgs.requests
    ]))
  ];

  GOOGLE_APPLICATION_CREDENTIALS = "/home/grant/projects/batting/secrets/batting-a57cfa164993.json";
}
