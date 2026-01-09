{
  description = "Python devShell with lib.";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    nix-vscode-extensions.url = "github:nix-community/nix-vscode-extensions";
  };

  outputs =
    {
      nixpkgs,
      self,
      ...
    }@inputs:
    let
      system = "aarch64-darwin";

      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
        overlays = [
          inputs.nix-vscode-extensions.overlays.default
        ];
      };

      pkgsX86 =
        if system == "aarch64-darwin" then
          import pkgs.path {
            system = "x86_64-darwin";
            config = pkgs.config;
          }
        else
          null;

      effectivePkgsX86 = if pkgsX86 != null then pkgsX86 else pkgs;

      pyShellHook =
        python3env: venv-config:
        let
          pipkgs-format = pkgs.lib.concatStringsSep "\n" venv-config.pipkgs;

          venv-name = ".venv_" + venv-config.name;
        in
        ''
          cat > .requirements.txt <<EOF
          ${pipkgs-format}
          EOF

          cat > .zsh-shell <<'EOF'
          export spmt='\033[38;5;5;1m> \033[0m\033[48;5;0m' # >_
          export sqes='\033[48;5;0;38;5;8m[\033[38;5;4m?\033[38;5;8m]\033[0m' # [?]
          export scac='\033[48;5;0;38;5;8m[\033[38;5;1mx\033[38;5;8m]\033[0m' # [x]
          export sexc='\033[48;5;0;38;5;8m[\033[38;5;2mo\033[38;5;8m]\033[0m' # [o]
          export smak='\033[48;5;0;38;5;8m[\033[38;5;5m+\033[38;5;8m]\033[0m' # [+]
          export swrn='\033[48;5;0;38;5;8m[\033[38;5;3m!\033[38;5;8m]\033[0m' # [!]
          export syon='(\033[38;5;2;1my\033[38;5;0m/\033[38;5;1;1mn\033[0m)' # (y/n)

          for file in $(find ./ -name '.venv*'); do
            if [[ $file != ./${venv-name} ]]; then
              echo "$scac Removing other venv $file"
              rm -rf $file
            fi
          done

          # If venv is outdated, recreate
          if [[ ! -f "$(readlink -f ./${venv-name}/bin/python)" ]] && [[ -d ./${venv-name} ]]; then 
            echo -e "$swrn Removing outdated venv"
            rm -rf ./${venv-name}/
          fi 

          # Create venv if not present
          [[ -d ./${venv-name} ]] || ( python -m venv ./${venv-name} && echo -e "$smak Created venv ./${venv-name}" )

          pydir=$(ls ${python3env}/lib/ | grep "^python")

          # Clean old links
          for file in $(find ./${venv-name}/lib/''${pydir}/site-packages -maxdepth 1 -type l); do # Find all links in site-packages
            target="$(readlink "$file")" # If target file is not in current derivation, delete
            if ! echo $target | grep "${python3env}" >/dev/null;then 
              rm -rf $file
            fi
          done
          echo -e "$swrn Cleaned old dependencies"

          # Links dependencies
          for file in ${python3env}/lib/''${pydir}/site-packages/*; do
            ln -s $file ./${venv-name}/lib/''${pydir}/site-packages/ 1>/dev/null 2>&1 
          done
          echo -e "$smak Linked site-packages"

          # Activate
          source ./${venv-name}/bin/activate
          echo -e "$sexc Activated venv"
          pip install -r .requirements.txt
          echo -e "$smak Installed requirements"

          # On exit deactivate
          TRAPEXIT() { 
            echo -e "$scac Deactivated venv"
            rm -rf .zsh-shell .requirements.txt
            deactivate
          }
          EOF

          exec ${pkgs.zsh}/bin/zsh --rcs -i -c "source .zsh-shell; ${pkgs.zsh}/bin/zsh -i"
        '';
      /*
        # Configure pypkgs override
        packageOverrides = pkgs.callPackage ./python-packages.nix { };
        python3 = pkgs.python3.override { inherit packageOverrides; };
      */
    in
    {
      # Maybe ditch flake.nix for devenv.nix see https://devenv.sh

      devShells."${system}" = {
        default =
          let
            venv-packages = [ ];

            python3env = pkgs.python3.withPackages (
              p: with p; [
                pip
              ]
            );
          in
          pkgs.mkShell {
            packages = [
              python3env
            ];

            shellHook = pyShellHook python3env {
              pipkgs = venv-packages;
              name = "default";
            };
          };

        pillow =
          let
            venv-packages = [
              #"matplotlib==3.10.7"
              "pillow==12.0.0"
            ];

            python3env = pkgs.python3.withPackages (
              p: with p; [
                pip
                tkinter
              ]
            );
          in
          pkgs.mkShell {
            packages = [
              python3env
              # pyxel # for pyxel no python import
            ];

            shellHook = pyShellHook python3env {
              pipkgs = venv-packages;
              name = "pillow";
            };
          };
      };
    };
}
