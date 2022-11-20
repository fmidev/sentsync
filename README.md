# Downloading Sentinel files from Sentinel hubs in scenes (time and area definition) for NRT and case studies

# Usage in --help

# Example config file: config_example.json

# Credentials file format in file: credentials_example

# Use a config file for nrt and send it to background using nohup

nohup path_to_python_in_env_bin sentsync.py --config-file config_example.json 2>>/dev/null 1>>/dev/null &

# Packages in conda environment tested with:

Name                    Version                   Build  Channel

_libgcc_mutex             0.1                 conda_forge    conda-forge

_openmp_mutex             4.5                       2_gnu    conda-forge

brotlipy                  0.7.0           py311hd4cff14_1005    conda-forge

bzip2                     1.0.8                h7f98852_4    conda-forge

ca-certificates           2022.9.24            ha878542_0    conda-forge

certifi                   2022.9.24          pyhd8ed1ab_0    conda-forge

cffi                      1.15.1          py311h409f033_2    conda-forge

charset-normalizer        2.1.1              pyhd8ed1ab_0    conda-forge

click                     8.1.3           unix_pyhd8ed1ab_2    conda-forge

colorama                  0.4.6              pyhd8ed1ab_0    conda-forge

cryptography              38.0.3          py311h42a1071_0    conda-forge

geojson                   2.5.0                      py_0    conda-forge

geomet                    0.3.0              pyhd3deb0d_0    conda-forge

html2text                 2020.1.16                  py_0    conda-forge

idna                      3.4                pyhd8ed1ab_0    conda-forge

ld_impl_linux-64          2.39                 hc81fddc_0    conda-forge

libblas                   3.9.0           16_linux64_openblas    conda-forge

libcblas                  3.9.0           16_linux64_openblas    conda-forge

libffi                    3.4.2                h7f98852_5    conda-forge

libgcc-ng                 12.2.0              h65d4601_19    conda-forge

libgfortran-ng            12.2.0              h69a702a_19    conda-forge

libgfortran5              12.2.0              h337968e_19    conda-forge

libgomp                   12.2.0              h65d4601_19    conda-forge

liblapack                 3.9.0           16_linux64_openblas    conda-forge

libnsl                    2.0.0                h7f98852_0    conda-forge

libopenblas               0.3.21          pthreads_h78a6416_3    conda-forge

libsqlite                 3.39.4               h753d276_0    conda-forge

libstdcxx-ng              12.2.0              h46fd767_19    conda-forge

libuuid                   2.32.1            h7f98852_1000    conda-forge

libzlib                   1.2.13               h166bdaf_4    conda-forge

ncurses                   6.3                  h27087fc_1    conda-forge

numpy                     1.23.4          py311h7d28db0_1    conda-forge

openssl                   3.0.7                h166bdaf_0    conda-forge

pandas                    1.5.1           py311h8b32b4d_1    conda-forge

pip                       22.3.1             pyhd8ed1ab_0    conda-forge

pycparser                 2.21               pyhd8ed1ab_0    conda-forge

pyopenssl                 22.1.0             pyhd8ed1ab_0    conda-forge

pysocks                   1.7.1              pyha2e5f31_6    conda-forge

python                    3.11.0          ha86cf86_0_cpython    conda-forge

python-dateutil           2.8.2              pyhd8ed1ab_0    conda-forge

python_abi                3.11                    2_cp311    conda-forge

pytz                      2022.6             pyhd8ed1ab_0    conda-forge

readline                  8.1.2                h0f457ee_0    conda-forge

requests                  2.28.1             pyhd8ed1ab_1    conda-forge

sentinelsat               1.1.1              pyhd8ed1ab_0    conda-forge

setuptools                65.5.1             pyhd8ed1ab_0    conda-forge

six                       1.16.0             pyh6c4a22f_0    conda-forge

tk                        8.6.12               h27826a3_0    conda-forge

tqdm                      4.64.1             pyhd8ed1ab_0    conda-forge

tzdata                    2022f                h191b570_0    conda-forge

urllib3                   1.26.11            pyhd8ed1ab_0    conda-forge

wheel                     0.38.3             pyhd8ed1ab_0    conda-forge

xz                        5.2.6                h166bdaf_0    conda-forge
