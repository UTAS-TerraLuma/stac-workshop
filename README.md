# STAC Workshop

Clone this repo

```
git clone https://github.com/UTAS-TerraLuma/stac-workshop.git
# or vai the github cli
gh repo clone UTAS-TerraLuma/stac-workshop
# or use the Desktop app 🤷

# Change into directory
cd stac-workshop
```


Create an environment. Pixi is the easiest, [install instructions here](https://pixi.prefix.dev/latest/installation/#__tabbed_1_2). Then run 

```
pixi install
```

Alternatively via conda

```
conda env create -f environment.yml -n stac-workshop
conda activate stac-workshop
```

Run marimo

```
# If using pixi
pixi run edit

# if using conda
conda activate stac-workshop
marimo edit stac_notebook.py
```
