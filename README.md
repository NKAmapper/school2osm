# school2osm
Extracts schools from the Norwegian National School Register (NSR)

### Usage ###

<code>python school2osm.py [outfile.osm]</code>

### Notes ###

* This program extracts primary, secondary and high schools from the National School Register (NSR) by the Norwegian Directorate for Education and Training and produces an OSM file with all schools; approx. 4000 public and private schools for the whole country.
* NSR is collecting data from the [Central Register of Establishments and Enterprises](https://ssb.no/a/metadata/om_datasamlinger/virksomhets-_og_foretaksregisteret/bof.html) as well as from other sources, such as [GSI](https://gsi.udir.no/app/#!/view/units/collectionset/1/collection/80/unit/1/). Data quality ultimatly depends on input from each school or county.
  * Coordinates without a proper address (street + house number) are very rough (postal code accuracy).
  * Schools without _capacity_ or _website_ may not be in operation yet - you may want to consult indexed search engines to discover their status.
  * A few schools are in fact just administrative offices and should not be imported to OSM.
* The directorate recommends extrating data outside of normal business hours to get a consistent set of data.
* Use [update2osm](https://github.com/osmno/update2osm) to discover differences to schools currently in OSM and to get an OSM file ready for inspection and uploading, based on the _ref:udir_nsr_ tag.

### References ###

* [Utdanningsdirektoratet - NSR](https://nsr.udir.no)
* [Utdanningsdirektoratet - Open data](https://www.udir.no/om-udir/data)
* [NSR API](https://data-nsr.udir.no/swagger/ui/index)
* [Skoleporten.no](https://skoleporten.udir.no)
* [Grunnskolenes informasjonssystem - GSI](https://gsi.udir.no/app/#!/view/units/collectionset/1/collection/80/unit/1/)
* [Virksomhets- og foretaksregisteret (VoF)](https://ssb.no/a/metadata/om_datasamlinger/virksomhets-_og_foretaksregisteret/bof.html)
