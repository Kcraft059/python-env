{ pkgs, fetchurl, fetchgit, fetchhg }:

self: super: {
  "certifi" = super.buildPythonPackage rec {
    pname = "certifi";
    version = "2025.8.3";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/e5/48/1549795ba7742c948d2ad169c1c8cdbae65bc450d6cd753d124b17c8cd32/certifi-2025.8.3-py3-none-any.whl";
      sha256 = "198pyad6jy7x5wx5v3ln8ik5vijhjfprb19jzyi6pc5iry9j9hgn";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "charset-normalizer" = super.buildPythonPackage rec {
    pname = "charset-normalizer";
    version = "3.4.3";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/83/2d/5fd176ceb9b2fc619e63405525573493ca23441330fcdaee6bef9460e924/charset_normalizer-3.4.3.tar.gz";
      sha256 = "054d0r8rimd5wrcph6p7p2dblcni614llpa6f75nykr4022lpkkg";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "idna" = super.buildPythonPackage rec {
    pname = "idna";
    version = "3.10";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/76/c6/c88e154df9c4e1a2a66ccf0005a88dfb2650c1dffb6f5ce603dfbd452ce3/idna-3.10-py3-none-any.whl";
      sha256 = "1lw72a5swas501zvkpd6dsryj5hzjijqxs3526kbp7151md1jvcl";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
  "requests" = super.buildPythonPackage rec {
    pname = "requests";
    version = "2.32.5";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/1e/db/4254e3eabe8020b458f1a747140d32277ec7a271daf1d235b70dc0b4e6e3/requests-2.32.5-py3-none-any.whl";
      sha256 = "1dpz38b6lnn8fcad7kfiagagbc3djy3f35a24qrdakx36x3gjqi4";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [
      self."certifi"
      self."charset-normalizer"
      self."idna"
      self."urllib3"
    ];
  };
  "urllib3" = super.buildPythonPackage rec {
    pname = "urllib3";
    version = "2.5.0";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a7/c2/fe1e52489ae3122415c51f387e221dd0773709bad6c6cdaa599e8a2c5185/urllib3-2.5.0-py3-none-any.whl";
      sha256 = "1p7hrw2cc75zyqbb49diqi371gxkis07225mfkii6spsq1ridc76";
    };
    format = "wheel";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
}

# nix-run github:nix-community/pip2nix -- generate <pkgName> // currently broken on macos

# example https://pypi.org/project/numpy/2.3.2/#files

/*
  "numpy202" = super.buildPythonPackage rec {
    pname = "numpy";
    version = "2.0.2";
    src = fetchurl {
      url = "https://files.pythonhosted.org/packages/a9/75/10dd1f8116a8b796cb2c737b674e02d02e80454bda953fa7e65d8c12b016/numpy-2.0.2.tar.gz";
      sha256 = "0y3fcd268cnrc8ipcmj1c082an4j4a4wj3dbcjlf500qxryrhg48";
    };
    format = "setuptools";
    doCheck = false;
    buildInputs = [];
    checkInputs = [];
    nativeBuildInputs = [];
    propagatedBuildInputs = [];
  };
*/
