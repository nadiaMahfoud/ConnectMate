{ pkgs }: {
  deps = [
    pkgs.rustc
    pkgs.libiconv
    pkgs.cargo
    pkgs.sqlite.bin
    pkgs.python39Packages.requests
  ];
}