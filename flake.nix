{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};

    fhs = pkgs.buildFHSUserEnv {
      name = "fhs-shell";
      targetPkgs = pkgs: with pkgs; [micromamba zsh];
      runScript = ''
        zsh -c '
          export MAMBA_ROOT_PREFIX=.mamba
          eval $(micromamba shell activate env1 --shell bash)
          exec zsh
        '
      '';
    };
  in {
    devShells.${system}.default = fhs.env;
  };
}
