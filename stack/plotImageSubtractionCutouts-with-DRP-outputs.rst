#########################################
Generating image cutouts with DRP outputs
#########################################

To generate image cutouts using the `plotImageSubtractionCutouts` task from `analysis_ap` you need to use the
code listed below.

Note, the code differs from its general implementation when using DRP outputs, since you
are required to iterate through each of the references individually, retrieve the diaSources (using the
`goodSeeingDiff_diaSrcTable` not `goodSeeingDiff_diaSrc` to have data in the correct format for this task).

.. code-block:: text

    repo = /repo/main
    collections = /path/to/your/DRP/collection
    butler = dafButler.Butler(repo, collections=collections)

    cutoutConfigDrp = PlotImageSubtractionCutoutsConfig()
    cutoutTaskDrp = PlotImageSubtractionCutoutsTask(
        config=cutoutConfigDrp, output_path=output
    )

    data_refs = butler.query_datasets(
        "goodSeeingDiff_diaSrcTable", where=where, limit=limit
    )

    for ref in data_refs:
        try:
            dv_diaSourceTable = butler.get(ref)
        except:
            print(f"Could not load diaSource table for {ref.dataId}")
            continue
        else:
            dv_diaSourceTable["instrument"] = "LSSTComCam"
            cutoutTaskDrp.run(dv_diaSourceTable, butler)
