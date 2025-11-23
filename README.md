# Compression and Progressive Decoding of 3D Model using Arbitrary Triangular Meshes

## Introduction
This README provides instructions on running the code and replicating the results of our project.
The aim of this project was to create a progressive model using the Progressive Compression of Arbitrary Triangular Meshes
method introduced by Cohen-Or, Levin and Remez in 1999.

## Requirements
To run this project, Python 3.6+ and the libraries contained in the `requirements.txt` file are required.
The libraries listed in requirements.txt can be installed by using the following command:
```
pip install -r requirements.txt
```

## Creating a progressive model
A progressive model (OBJA file) can be created by running the `decimate.py` file.
This code takes 0, 1 or 2 arguments. The first argument is for the name of the model, and the second one is for the
number of iterations. If none are given, the 'bunny' model will be compressed
over 5 iterations. 

Examples of correct usage:
```
python3 decimate.py
```
```
python3 decimate.py cow 
```
```
python3 decimate.py cow 8 
```
At the end of the compression process, the compression ratio will be displayed
in the terminal.

## Visualizing the progressive decompression
To visualize the progressive decompression of the model,
run the server.py file and go to http://localhost:8000.
A specific model can be visualized by adding "?progressive_models/progressive__(obj_model).obja" 
at the end of the adress.

Example of usage: 

To visualize the progressive decompression of the model 'cow',
first run the `server.py` file:
```
python3 server.py
```
Then, open a web browser and go to http://localhost:8000/?progressive_models/progressive__cow.obja.

## Guide for replicating the results
### Compression ratio
To compute the compression ratio obtained with our proposed solution,
run the `decimate.py` file. The compression ratio will be displayed at the end of
the execution in the terminal.

### Progressiveness
The progressiveness of our models can be evaluated by uploading
the obja files obtained in the benchmarking website http://csi-benchmark.mooo.com/.

### Compression ratio per iteration
The evolution of the compression ratio for a given model can be visualised by running the
`efficiency_iteration.py` file. This code takes 0 or 1 argument. If none are given, the results
for the model 'bunny' will be displayed.

Example:

```
python3 efficiency_iteration.py cow
```
