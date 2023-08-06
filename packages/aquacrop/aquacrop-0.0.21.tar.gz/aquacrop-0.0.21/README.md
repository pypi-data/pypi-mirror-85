# AquaCrop-OSP
> Crop-water model based on AquaCrop-OS


## Install

`pip install aquacrop`

AquaCrop-OS, an open source version of FAO’s multi-crop model, AquaCrop. AquaCrop-OS was released in August 2016 and is the result of collaboration between researchers at the University of Manchester, Water for Food Global Institute, U.N. Food and Agriculture Organization, and Imperial College London.

AquaCropOS is an environment built for the design and testing of irrigation stratgeies. We are still in early development and so ensure you have downloaded the latest version.

It is built upon the AquaCropOS crop-growth model (written in Matlab `link`) which itself itself is based on the FAO AquaCrop model. Comparisons to both base models are shown in `link`

## Quickstart

Run tutorials instantly on Google Colab:

<a href="https://colab.research.google.com/github/thomasdkelly/aquacrop/blob/master/tutorials/01_basics.ipynb">1: Basics</a>

<a href="https://colab.research.google.com/github/thomasdkelly/aquacrop/blob/master/tutorials/02_irrigation.ipynb">2: Irrigation</a>

#### dev to do:
    
 - improve names - Paramstrcut/Clockstruct/initcondclass
    
 - tut: optimisation
 
 - tut: calibration
 
 - tut: custom irrigation decisions
 
 - env.gym style wrapper
 
 - add a display_full_outputs arg so we dont create a pandas dataframe after each model end
 
 - add all calibrated crops and test
  
 - add __repr__
 
 - add export and import crop feature
 
 - add test for irrigation - gW
