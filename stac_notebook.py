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
    from pystac import Catalog

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
    rgb_colleciton.describe()
    return (rgb_colleciton,)


@app.cell
def _(rgb_colleciton):
    ntafin0013 = rgb_colleciton.get_item(
        id="20240925_NTAFIN0013_m3m_50mAGL_ortho_RGB"
    )
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
def _(mo):
    import itertools


    def show_items(items):
        output = []
        for row in itertools.batched(items, 4):
            item_thumbnails = mo.hstack(
                [
                    mo.image(
                        item.assets["thumbnail"].href, width="24%", height=None
                    )
                    for item in row
                ],
                align="center",
            )
            output.append(item_thumbnails)
        return mo.vstack(output)

    return (show_items,)


@app.cell
def _():
    from pystac_client import Client

    client = Client.open("https://stacapi.tern-dronescape.cloud.edu.au/")
    return (client,)


@app.cell
def _(mo):
    import datetime as dt

    show_rgb = mo.ui.checkbox(label="RGB Collection", value=True)
    show_ms = mo.ui.checkbox(label="MS Collection", value=True)

    date_filter = mo.ui.date_range(
        start=dt.date(2024, 8, 12), stop=dt.date(2025, 11, 20)
    )

    show_sa = mo.ui.checkbox(label="SA", value=True)
    show_tas = mo.ui.checkbox(label="TAS", value=True)

    mo.vstack(
        [
            mo.hstack(["Collections Filter:", show_rgb, show_ms], justify="start"),
            mo.hstack(["Temporal Filter:", date_filter], justify="start"),
            mo.hstack(["Spatial Filter:", show_sa, show_tas], justify="start"),
        ]
    )
    return show_ms, show_rgb, show_sa, show_tas


@app.cell(hide_code=True)
def _(client, show_items, show_ms, show_rgb, show_sa, show_tas):
    if show_rgb.value and show_ms.value:
        collections_filter = ["naturescan-rgb", "naturescan-ms"]
    elif show_ms.value:
        collections_filter = ["naturescan-ms"]
    elif show_rgb.value:
        collections_filter = ["naturescan-rgb"]
    else:
        collections_filter = None

    sa_bbox = [129.0, -38.0, 141.0, -26.0]
    tas_bbox = [143.82, -43.75, 148.50, -39.57]
    combined_bbox = [sa_bbox[0], tas_bbox[1], tas_bbox[2], sa_bbox[3]]

    if show_sa.value and show_tas.value:
        bbox = combined_bbox
    elif show_sa.value:
        bbox = sa_bbox
    elif show_tas.value:
        bbox = tas_bbox
    else:
        bbox = None

    items = client.search(collections=collections_filter, bbox=bbox).items()


    show_items(items)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Closer look at the stac internals

    ## STAC Item

    Items are the main unit of STAC. Collections and catalogs are really just for organisation. A stac item extends the GeoJSON spec and must be a valid GeoJSON polygon object. The `geometry` key will define where this item is in WGS84, and the `properties.datetime` key will define when.
    """)
    return


@app.cell
def _(ntafin0013):
    ntafin0013.to_dict()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(rf"""
    ### Assets

    Assets are not their own item but a field within an item. A lot of information can also be stored at the asset level. The asset below is included in the item above, its just separated for convenience. Even within assets, information may further be shown at an asset level, or at a band level.
    """)
    return


@app.cell
def _(ntafin0013):
    ntafin0013.assets["main"].to_dict()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Collection

    A collection can link to items or other collections. A collection must also include it's spatial and temporal extent of its children.
    """)
    return


@app.cell
def _(rgb_colleciton):
    rgb_colleciton.to_dict()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Catalog

    A catalog is similar to a collection but without extent. It usually just serves as a very high level folder. E.g. within TerraLuma you could have a NatureScan catalog and DroneScape catalog.
    """)
    return


@app.cell
def _(catalog):
    catalog.to_dict()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Deciding what to put in STAC

    There are very few required fields for a valid stac. E.g. an item needs the geometry, a datetime, and id and that's about it. However, there are extensions that include further standardisation for specific use cases - e.g. the [earth observation (EO) extension](https://github.com/stac-extensions/eo) includes common fields on for EO data such as wavelength, FWHM, cloud or snow cover. As of stac 1.1 some of the fields from the most common extensions (raster, eo and proj) are now part of the [common metadata](https://github.com/radiantearth/stac-spec/blob/master/commons/common-metadata.md).

    With STAC's flexibility comes a bunch of decisions that need to be made around what data you want to include in your catalog, where you want to add it (i.e. at the band level, asset level, item level) and how you want to structure your catalog, collections and items.

    This is the [STAC architecture](https://github.com/UTAS-TerraLuma/naturescan-data-platform/blob/main/notebooks/cog-stac/STAC_architecture.md) I decided on for the current version of the catalog, however, I think a bunch of that will change.
    """)
    return


if __name__ == "__main__":
    app.run()
