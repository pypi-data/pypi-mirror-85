# Statistical Summary For Neuroscience
A statistical summary commandline tool for Axios raw data files.
Right now it create several plots:
* low passed PSD
* spike raster
* spike traces
* population spiking vector
* PSD of the population spiking vector
* spike traces of the population spiking vector

## Installation
1. [Follow these instructions to install the Python engine for Matlab](https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html)
2. Run `python setup.py install`
## How To Use
```
neurosum (Raw file or folder name containing .raws)
```
It will output its plots into a folder titled `(Name of raw file)_processed`


