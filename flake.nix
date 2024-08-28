{
  description = "Experimental flake for docker container";

  inputs = {
    nixpkgs.url = "nixpkgs/nixos-23.11";
    #nixpkgs-unstable.url = "nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
  let
    system = "x86_64-linux";
    pkgs = nixpkgs.legacyPackages.${system};
    python3Packages = pkgs.python3.pkgs;

    pkg-rrdtool = (py : py.buildPythonPackage rec {
      pname = "rrdtool";
      version = "0.1.16";
      #pyproject = true;
      doCheck = false;

      src = py.fetchPypi {
        inherit pname version;
        hash = "sha256-Xwr/iz4KD3AWUvqIv2BaVL6eayX7pSoTtnxx97NaFFE=";
      };
      build-system = [
        py.setuptools
        py.setuptools-scm
      ];
      buildInputs = [
        pkgs.rrdtool
      ];
      meta = {
        #changelog = "https://github.com/pytest-dev/pytest/releases/tag/${version}";
        description = "Python bindings for RRDtool for Python 2 and 3";
        homepage = "https://pythonhosted.org/rrdtool";
        #license = lib.licenses.gpl2;
      };
    }) pkgs.python3Packages;
    deps = [
      pkgs.sqlite
      pkgs.rrdtool
      (pkgs.python3.withPackages (ps:
        [ ps.django pkg-rrdtool ps.setuptools ]))
    ];
    contUtils = [
      pkgs.busybox
      #pkgs.bash
      pkgs.dockerTools.binSh
    ];
    devUtils = [
      pkgs.tcsh
      pkgs.git
    ];

    # sdist = pkgs.runCommand "make-sdist"
    #   { buildInputs = [pkgs.python3]; }
    #   ''
    #      mkdir src
    #      cp -r ${./.}/* src
    #      cd src
    #      python setup.py sdist -d $out
    #   '';

    myApp = pkgs.python3.pkgs.buildPythonPackage {
      pname = "rrd_view";
      version = "1.0.1";
      #pyproject = true;

      src = ./.;
      build-system = with python3Packages; [
        setuptools
        wheel
      ];
      dependencies = deps;

      # has no tests
      doCheck = false;

      meta = {
        description = "Django server for time-series collection/display";
        #license = lib.licenses.bsd3;
        license = ./LICENSE;
      };
    };

  in {
    # packages.${system}.default = pkgs.ociTools.buildContainer {
    #   args = [
    #     (pkgs.lib.getExe pkgs.bash)
    #   ];
    #   #mounts = {};
    #   readonly = false;
    # };

    #packages.${system}.default = myApp;

    packages.${system}.default = pkgs.dockerTools.buildLayeredImage {
      name = "rrd_view";
      tag = "latest";
      created = "2024-08-26";
      contents = deps ++ contUtils ++ [ myApp ];
      enableFakechroot = true;
      #extraCommands = ''
      fakeRootCommands = ''
        echo myApp= ${myApp}
        echo pwd= $(pwd)
        mkdir -p /app/
        ln -s ${myApp}/lib/python3.11/site-packages /app/
        for i in site-packages/manage.py site-packages/volts \
                 /rrd_view/init-data.json /rrd_view/test_data.json \
                 /data data/db.sqlite3 data/values.rrd; do
          ln -s $i /app/
        done
        mkdir -p /data/plot
      '';
      config = {
        EntryPoint = [ "python3" "manage.py" ];
        Cmd = [ "runserver" "0.0.0.0:8000" ];
        #Cmd = [ "${pkgs.lib.getExe pkgs.bash}" ];
        WorkingDir = "/app";
        Volumes = { "/data" = { }; };
        ExposedPorts = { "8000/tcp" = { }; };
      };
    };

    devShells.${system}.default =
      pkgs.mkShellNoCC {
        name = "rrd_view";
        # nativeBuildInputs =
        packages = deps ++ devUtils ++ [ myApp ];
        shellHook = ''
          echo "Nix Dev environment (should exec tcsh)"
          echo "self= ${self}"
          # exec tcsh
        '';
      };

  };
}

