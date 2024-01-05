{ pkgs ? import (builtins.fetchTarball https://github.com/NixOS/nixpkgs/archive/057f9ae.tar.gz) {} }:

let
  pythonPath = with pkgs.python3Packages; [
    numpy
    # Add any other required Python dependencies here
  ];
  PATH_SEPARATOR = ":";  # Define the PATH_SEPARATOR variable
in
pkgs.mkShell {
  buildInputs = [
    pkgs.python3Packages.opencv-python
    pkgs.libGL
    pkgs.python3Packages.requests
    pkgs.python3Packages.numpy
    pkgs.python3Packages.discord.py_2_3_2
    pkgs.python3Packages.pyproject-toml_0_0_10
    pkgs.python3Packages.colorama_0_4_6
    pkgs.python3Packages.moviepy
    pkgs.python3Packages.huggingface_hub
    pkgs.python3Packages.unidecode
    # Add any other required dependencies here
  ];
  shellHook = ''export PYTHONPATH=$PYTHONPATH${PATH_SEPARATOR}${pythonPath.join(":")}''; 
}
