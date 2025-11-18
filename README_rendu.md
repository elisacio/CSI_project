# Compression and Progressive Decoding of 3D Model using Arbitrary Triangular Meshes

This README file provides instructions on running the code and replicating the results.

## Creating an OBJA from a OBJ file
Run the decimate.py file followed by the name of the OBJ model.
example : "python3 .\decimate.py bunny"

## Visualizing the stream
Run the server.py file and go to http://localhost:8000.
A specific model can be visualized by adding "?example/<obja_file_name>.obja" at the end of the adress.
example: to vizualize the model "cow", use go to http://localhost:8000/?example/progressive_cow.obja.