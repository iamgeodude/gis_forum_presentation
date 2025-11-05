<section data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)">
    <a data-id="logo" href="https://geographic.texas.gov" style="font-size: 16px;" class="r-hstack gap">
        <img src="./assets/z_general/TxGIO_Primary_Horizontal.png" alt="txgio logo"
            style="height: 40px; background: transparent;" class="logo">
        Exploring CNG | Part 1: What is CNG?
    </a>
    <h2>What is CNG?</h2>
    <ol>
        <li class="fragment">Partial reads</li>
        <li class="fragment">Parallel reads</li>
        <li class="fragment">File metadata in one read</li>
        <li class="fragment">Addressable</li>
        <li class="fragment">Capable of partitioning and tiling</li>
        <li class="fragment">Accessible over HTTP using byte-range requests</li>
    </ol>

<aside class="notes">
So, what is Cloud Native Geospatial, or CNG? Well, in the abstract, any geospatial file that

1. Allows partial reads
2. Allows parallel reads (multiple partials or entire reads in parallel)
3. File metadata is retrievable in one read (this is important)
4. The data in a file is addressable
5. The files are capable of partitioning (split between multiple files) and tiling (split and indexed based on geo attributes)
6. The files are accessible over HTTP(S) using byte-range requests

The metadata being retrievable in one read enables capabilities 4-6 by allowing reading of indexes and addresses of data
from the metadata of a file. This acts similar to paging and indexing of a transactional database like
MySQL or PostgreSQL. However, it is important to note that CNG files are read-only and that transactional operations are not possible without reading and overwriting an entire file. This means that, if your data requires frequent write operations, a traditional transactional database will likely suit your needs more directly. However, for read-only, download-oriented operations, CNG is a very promising option.
</aside>
</section>

<section data-auto-animate data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)">
    <a data-id="logo" href="https://geographic.texas.gov" style="font-size: 16px;" class="r-hstack gap">
        <img src="./assets/z_general/TxGIO_Primary_Horizontal.png" alt="txgio logo"
            style="height: 40px; background: transparent;" class="logo">
        Exploring CNG | Part 1: What is CNG? - Standards and Community
    </a>
    <h3>
        Standards and Community
    </h3>
</section>

<section data-background-iframe="https://cloudnativegeo.org/about/" data-background-interactive
    data-background-color="white" data-auto-animate
    data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)">
    <h4 style="padding: 8px; background: #191919; color: white;">Cloud Native Geospatial Forum</h4>
<aside class="notes">
Not to be confused with CNG file formats, there is a community dedicated to advancing CNG data and
related technologies and tools called the Cloud Native Geospatial Forum. They hold an annual conference
which I attended last year, and I highly recommend watching their videos which are posted to YouTube,
or attending their event in-person. The next CNG Conference is on October 6-9, 2026 in Snowbird, Utah.
It's a beautifully organized event and I highly recommend it to anyone interested in the concepts and techologies
presented in this presentation.

It's important to note that CNG Forum is NOT a standards organization but a place for geospatial practitioners
to coordinate and collaborate on the future of geospatial technology. CNG Forum defers to the OGC, or Open Geospatial Consortium, for standards, although some contributing members of CNG Forum are also contributing members of the OGC.
</aside>
</section>

<section data-background-iframe="https://ogc.org/who-we-are" data-background-interactive
    data-background-color="white" data-auto-animate
    data-auto-animate-easing="cubic-bezier(0.770, 0.000, 0.175, 1.000)">
    <h4 style="padding: 8px; background: #191919; color: white;">Open Geospatial Consortium</h4>
<aside class="notes">
The Open Geospatial Consortium is a group of professionals in the GIS industry that collaborate
to produce stable standards and specifications for geospatial technologies and tooling. The OGC
also produces proofs-of-concept for new standards and technologies based upon those standards,
serving as a governing body to provide stability and stable progress to the geospatial industry.
</aside>
</section>
