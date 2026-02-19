import marimo

__generated_with = "0.19.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exploring a static catalog
    """)
    return


@app.cell
def _():
    import json

    from pystac import Catalog, get_stac_version

    return (Catalog,)


@app.cell
def _(Catalog):
    catalog = Catalog.from_file(
        "https://object-store.rc.nectar.org.au/v1/AUTH_4df2f67c2eed48a2aaeeed008a4bf0de/naturescan-assets/stac/catalog.json"
    )
    catalog.describe()
    return (catalog,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Crawl the catalog with `get_child`
    """)
    return


@app.cell
def _(catalog):
    rgb_colleciton = catalog.get_child("naturescan-rgb")
    rgb_colleciton.to_dict()
    return (rgb_colleciton,)


@app.cell
def _(rgb_colleciton):
    ntafin0013 = rgb_colleciton.get_item(id="20240925_NTAFIN0013_m3m_50mAGL_ortho_RGB")
    ntafin0013.to_dict()
    return (ntafin0013,)


@app.cell
def _(ntafin0013):
    ntafin0013.get_assets()
    return


@app.cell
def _(mo, ntafin0013):
    mo.image(ntafin0013.get_assets()["thumbnail"].href)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Exploring a dynamic catalog
    """)
    return


@app.cell
def _():
    from pystac_client import Client

    client = Client.open("https://stacapi.tern-dronescape.cloud.edu.au/")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
