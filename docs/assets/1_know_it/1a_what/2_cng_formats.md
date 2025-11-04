
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
### Cloud Optimized Geotiff Website <!-- .element: style="background: #19191980; padding: 8px; color: white;" -->

<div class="r-hstack gap fragment fade-in-then-out" style="background: #fff;">
        <ul>
            <li>Internal file directories</li>
            <li>Metadata used to get only data needed</li>
            <li>Provides data addresses for byte_range requests</li>
        </ul>
        <img src="./assets/1_know_it/1a_what/cog.png" style="max-height: 400px;" />
</div>

<aside class="notes">
COGs store raster data types and can be viewed as a replacement for
GeoTIFF, .IMG, .MrSID, so on and so forth. COGs are an established OGC standard and are commonly adopted by the USGS, Planet, Maxar, OpenAerialMap, and many other data providers.
COGs are also compatible with many softwares and libraries such as ArcPro, QGIS, GDAL, GeoServer, Mapserver, and much more.

Next, for your vector data (points, polygons, lines, etc), you have geoparquet/parquet and flatgeobuf.
</aside>

---

<!-- .slide: data-background-iframe="https://geoparquet.org/#:~:text=Releases-,About,-Apache%20Parquet%20is" data-background-interactive data-background-color="white" data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)" -->
### Geoparquet <!-- .element: style="background: #19191980; padding: 8px; color: white;" -->

<aside class="notes">
Next, for your vector data (points, polygons, lines, etc), you have geoparquet/parquet and flatgeobuf.
</aside>

---

<!-- .slide: data-background-iframe="https://viewer.copc.io?state=476d92915719fc3c1aa1082532cffc565ea61ff69f5861a24c0908c3c4336b95" data-background-interactive data-background-color="white" data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)" -->
### Cloud Optimized Point Cloud <!-- .element: style="background: #19191980; padding: 8px; color: white;" -->

<aside class="notes">
Finally, for 3D Point Cloud data, you have COPC/LAZ. This file format allows for efficient partial reads from remote sources
as well, such as Amazon S3 or Cloudflare R2.
</aside>
