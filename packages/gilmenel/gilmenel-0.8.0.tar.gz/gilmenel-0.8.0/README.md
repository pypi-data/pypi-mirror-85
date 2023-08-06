# Gilmenel

Sindarin. _noun_. meaning _Star of the Heavens_

!["Gilmenel"](docs/gilmenel-logo.png)

(Sindarin Elvish as created by _J. R. R. Tolkien_)

A framework for selecting stars in a target field that meet complex criteria defined by a telescope or instrument.

Given coordinates on-sky and a basic definition of a science instrument (basic instruments, along with some from the Southern African Large Telescope are included) stars can be selected for a specific purpose. The example is the output of the `salt_guidestars.py` script when pointed at the Jewel Box and with the `--png` flag enabled.

![Diagram of the Jewel Box](docs/jewel_box.gif)

## Installation

    pip install gilmenel

## Dependencies

For Ubuntu 18.04 and Python3:

    # apt-get install python3-dev

    $ sudo -H pip install -U pipenv

Libraries that might be required are:

    # apt-get install default-libmysqlclient-dev
    # apt-get install libssl-dev

Primary Python packages:
* astropy
* astroquery
* sqlalchemy
* matplotlib

Install DS9 for additional debugging:

    # apt-get install saods9

## Setup

    $ make install

Place the config file 'docs/config.py' into the main project directory.
Edit the file as required.

## Removal

    $ make uninstall

## Testing

To run unit tests, execute:

    $ make check

To run unit tests on source code change, execute:

    $ make watch-check

To run coverage test, execute:

    $ make coverage

## Examples

Minimal example:

    from astropy import units as u
    from astropy.coordinates import SkyCoord

    from gilmenel import gilmenel
    from gilmenel import salt

    gilmenel.init()

    tarantula = SkyCoord(
        '05h 38m 38s', '−69:05.7', unit=(u.hourangle, u.deg)
    )  # Tarantula Nebula

    instr = salt.fif
    instr.point_to(tarantula, pa=0 * u.deg)

    stars = gilmenel.view_sky(instr)
    guide_stars = gilmenel.find_best_stars(instr, stars)

    print(guide_stars)

A full usage example can be found in salt_guidestars.py

Usage:

    salt_guidestars.py field [OPTIONS] [jewel_box|near_jewel|somewhere|bootes_void|
    unittest|regular|centre|offset|null|mbxgpS201906130009|mbxgpP201906130039|tarantula|
    sunflower|m83] PA [pfgs|fif]

eg:

    $ ./salt_guidestars.py field jewel_box 0 pfgs

## DS9

When using ds9 for debugging, there appears to be two different versions that interpret
the command string differently.

    ds9 -dsseso "00:42:44.404 +41:16:08.78"

Versus

    ds9 -dsseso coord "00:42:44.404 +41:16:08.78"

The code might need to be changed to reflect the version locally installed.

# Catalogue

Asteria is designed to be run for a local or remote catalogue.

To download the whole-sky catalogue for SALT, run the command below. Please note that this is not recommended as A LOT of data (we're talking gigabytes here) will be downloaded.

    $ ./catalogue/drop_db.sky
    $ ./catalogue/create_db.py
    $ ./catalogue/download_sky.py
    $ ./catalogue/prepare_db.py

Should the catalogue download fail part-way through, inspect the files `succeeded.tsv` and `failed.tsv` for more details. Additional arguments can be passed to `download_sky.py` to begin in the correct place. Note that since data is downloaded and only committed to the database every 30 000 sources, a simple select query WHICH MUST INCLUDE THE `LIMIT` KEYWORD will show the last sources committed.

To view an image of the local catalogue, run:

    $ ./catalogue/view_sky.py

To run the view command on remote machines without displays:

    $ export MPLBACKEND="agg"

## Database Operations

To see a summary of duplicates

    select dup_count, count(dup_count) as row_count from (select count(source_id) as dup_count from Sources group by source) t group by dup_count order by dup_count;

To delete duplicate rows

    delete from Sources where source_id not in (select min(source_id) from Sources group by source);

## Commits

As of v0.4.0, this project will use the git commit message format outlined below:

    [optional breaking ]<type>[ optional (<scope>)]: <description>

    [optional body]

`<type>` is recommended to be one of:

    fix
    feat
    build
    chore
    ci
    docs
    style
    refactor
    perf
    test

`<scope>` is recommended to be a module, file, or folder name as appropiate.

This is a simpler version of https://www.conventionalcommits.org/

## Versions

This project uses Semantic Versioning, for more details see https://semver.org/
