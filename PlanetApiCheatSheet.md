---
Title : Planet API Cheat sheet  
Author : Phillip Parton  
Date : 15 Sept 2017  
---

A cheat sheet for using the Planet Command Line interface. Mostly drawn from [Planet](https://planetlabs.github.io/planet-client-python/cli/examples.html), their [GitHub](https://github.com/planetlabs/planet-client-python) and trial and error.

## To log in
To log in to the Planet API  
`planet init`

Your email and password are then requested

## To search for products
To search for all items within an AoI.  
`planet data search --item-type pso* --geom aoi.geojson`

And to add a `date` criteria to the search  
`planet data search --item-type pso* --date acquired gt 2017-07-30 --date acquired lt 2017-08-10 --geom aoi.geojson`

## Download products

Command line input for searching for all PSScene Analytic products between the specified dates and a given AoI  
`planet data download --item-type pss* --asset-type analytic --date acquired gt 2017-07-30 --date acquired lt 2017-08-10 --geom leggetts.geojson`

## Flag a verbose output

Placement of `Verbose` flag during download for detailed information of what the API is doing  
`planet --verbose data download --item-type pss* --asset-type visual --date acquired gt 2017-07-30 --date acquired lt 2017-08-10 --geom aoi.geojson`

## Write search results to file

Send the results of a search to a JSON file to be used in other applications or as an input. `limit` specifies the number of files returned.  
`planet data search --limit 10 --item-type pss* --geom tbu.geojson > list.json`

## Using a `filter` for download

Use the `planet data filter` commands to define filters that can be exported to a json file for further use. *The `filter` API will also create the `redding.json` used in previous bulk download scripts*.  
`planet data filter --date acquired gt 2017-07-01 --date acquired lt 2017-07-31 --range cloud_cover lt .1 --geom daandineGeom.geojson > test.json`

#### Input options
* `--date acquired xxxx` to set date constraints
* `--string-in strip_id xxxx` to select scenes that were acquired by a single satellite during a single pass; where `xxxx` is the `strip_id`. The `strip_id` can be found in the metadata of the scene
* `--range cloud_cover lt xxxx` to set the upper limit of acceptable cloud cover in a scene; where `xxxx` is the percentage allowable cloud cover ie `.05` = 5%, `.9` = 90%
    * `gt` `lt` `gte` `lte` stand for  *'greater than'*, *'lower than'*, *'greater than or equal'*, and *'lower than or equal'* respectively

#### Create a saved search

`planet data create-search --item-type pso* --asset-type visual --name search --filter-json test.json`

#### Download the saved search

`planet data download --asset-type visual --search-id 2ca41723fe8b4510aa4dc7aa1eb587d3`

## API version info

Check the installed version of the Planet API  
`planet --version`

## Update CLI

To update the version of the CLI to incorporate new changes. Run version check to verify it install properly.
`pip install planet -U`

## Set max allowable concurrent downloads

Use the `workers` flag to change the max number of concurrent downloads, the default is 4  
`planet --workers 10 data download --item-type pss* --asset-type visual --date acquired gt 2017-07-30 --date acquired lt 2017-08-10 --geom aoi.geojson`
