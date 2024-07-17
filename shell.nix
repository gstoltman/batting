# shell.nix
let
  pkgs = import <nixpkgs> {};
in pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (python-pkgs: [
      python-pkgs.beautifulsoup4
      python-pkgs.dash
      python-pkgs.matplotlib
      python-pkgs.notebook
      python-pkgs.numpy
      python-pkgs.pandas
      python-pkgs.requests
    ]))
  ];
}
