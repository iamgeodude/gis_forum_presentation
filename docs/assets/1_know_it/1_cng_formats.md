
<a data-id="logo" href="https://geographic.texas.gov"
style="font-size: 16px;" class="r-hstack gap">
<img src="./assets/z_general/TxGIO_Primary_Horizontal.png" alt="txgio logo"
    style="height: 40px; background: transparent;" class="logo">
Exploring CNG | Part 1: What is CNG? - Data Types - Standards
</a>

<table>
    <tr>
        <th>formats</th><th>data type</th><th>replace</th><th>standards status</th><th></th>
    </tr>
    <tr class="fragment">
        <td>Cloud-Optimized GeoTIFF (COG)</td><td>Raster</td><td>GeoTIFF, .img</td><td>OGC standard</td><td></td>
    </tr>
    <tr class="fragment">
        <td>Geoparquet, FlatGeobuf</td><td>Vector</td><td>.shp, .gdb, .geojson</td><td>OGC Incubating Standard</td><td></td>
    </tr>
    <tr class="fragment">
        <td>Cloud-Optimized Point Cloud (COPC)</td><td>Point Cloud</td><td>.laz, .las</td><td>No OGC standard</td><td></td>
    </tr>
</table>

<aside class="notes">
What is cloud native geospatial data? Well, in the abstract, any geospatial file format that follows
the specifications mentioned previously. In practice, there are some primary contenders within a sea of options.
The following are some of the most prominent options being adopted by geospatial professionals and practitioners
and within the tech industry.
</aside>

---

<!-- .slide: data-background-iframe="https://cogeo.org" data-background-interactive data-background-color="white" data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)" -->
### Cloud Optimized Geotiff <!-- .element: style="background: #19191980; padding: 8px; color: white;" -->

<div class="r-hstack gap fragment fade-in-then-out" style="background: #fff; border: solid 1px #191919;">
        <ul>
            <li>Internal file directories (IFDs)</li>
            <li>Metadata used to get only data needed by indexing IFDs</li>
            <li>Provides data addresses for byte_range requests</li>
        </ul>
        <img src="./assets/1_know_it/cog.png" style="max-height: 400px;" />
</div>

<aside class="notes">
COGs store raster data types and can be viewed as a replacement for
GeoTIFF, .IMG, .MrSID, so on and so forth. COGs are an established OGC standard and are commonly adopted by the USGS, Planet, Maxar, OpenAerialMap, and many other data providers.

Cloud Optimized Geotiffs work by providing:
<ul>
    <li>Internal file directories (IFDs)</li>
    <li>Metadata used to get only data needed by indexing IFDs</li>
    <li>Provides data addresses for byte_range requests</li>
</ul>
Libraries, software, and tools offering COG support ArcPro, QGIS, GDAL, GeoServer, Mapserver, FME, and more.
</aside>

---

<!-- .slide: data-background-iframe="https://geoparquet.org/#:~:text=Releases-,About,-Apache%20Parquet%20is" data-background-interactive data-background-color="white" data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)" -->
### Geoparquet <!-- .element: style="background: #19191980; padding: 8px; color: white;" -->

<aside class="notes">
Next, for your vector data (points, polygons, lines, etc), you have geoparquet/parquet and flatgeobuf. I am most familiar with geoparquet, and since it is fully compatible with the existing and ubiquitous parquet file format, it also seems to be the most popular among CNG adopters. So I will focus on Parquet in this presentation. Parquet and other CNG formats work in similar ways to the COG, I won't get too deep into the nitty gritty. However, geoparquet has some unique characteristics. First, parquet is a columnar file database format, not row-oriented. This means that when you query a geoparquet file, you can retrieve data from specified columns. This can drastically reduce query response time as well as the response byte-size of data returned from a given query. As of February 2025, parquet offers native geometry and geography column types for vector data, and raster column type support is in active development.

Many big names in the industry have adopted geoparquet in production workloads, including Element84, Carto, Microsoft, Planet, Apache Sedona, Overture Maps Foundation, Whereobots, Snowflake, AWS, Google, and many more.

Libraries, software, and tools offering geoparquet support include ArcPro, QGIS, Mapserver, GeoServer, GDAL, geopandas, DuckDB, Snowflake, FME, and more.
</aside>

---

<!-- .slide: data-background-iframe="https://viewer.copc.io?state=476d92915719fc3c1aa1082532cffc565ea61ff69f5861a24c0908c3c4336b95" data-background-interactive data-background-color="white" data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)" -->
### Cloud Optimized Point Cloud <!-- .element: style="background: #19191980; padding: 8px; color: white;" -->

<aside class="notes">
Finally, for 3D Point Cloud data, you have COPC/LAZ. This file format allows for efficient partial reads from remote sources
as well, such as Amazon S3 or Cloudflare R2. COPC are fully backwards compatible with software that is capable of reading .LAZ files as it is based upon the LAZ 1.4 specification. There are also products for web-based views of COPC data from remote sources, as you may notice in the background of this slide, I have loaded around 12 copc tiles into view and filtered the points based on classification. These are streamed and queried direct from object storage in Cloudflare R2, a service compatible with the AWS S3 specification.

Although support for the specifically cloud-native features of COPC appear to be experiencing slower adoption than other CNG formats, the USGS, Natural Resources Canada, National Geographic Institute of France, Hobu Inc, Safe Software (FME) and others have either adopted COPC in the capacity as data providers or in support of read/write.

Libraries, software, and tools offering support for reading and/or writing COPC files include QGIS, PDAL, FME, and LAStools, among others.
</aside>
