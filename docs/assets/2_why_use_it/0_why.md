<a data-id="logo" href="https://geographic.texas.gov"
style="font-size: 16px;" class="r-hstack gap">
<img src="./assets/z_general/TxGIO_Primary_Horizontal.png" alt="txgio logo"
    style="height: 40px; background: transparent;" class="logo">
Exploring CNG | Part 2: Why CNG?
</a>

<h2>Why CNG?</h2>
<ol class="fragment">
    <li>
        Storage Costs
    </li>
    <li class="fragment">
        Compute and Infrastructure Costs
    </li>
    <li class="fragment">
        Maintenance Costs
    </li>
    <li class="fragment">
        User / Customer Experience
    </li>
</ol>

<aside class="notes">
Okay, so, hopefully y'all have a general sense of what CNG is, but why would we want to use it?

Well,
<ol>
    <li>
        Storage Costs - Since specific portions of a CNG file can be requested based on attribute values
        or geographic queries, a user can get back only the portions of files that they want, sometimes with
        only one query across many files. In the case of my organization, TxGIO, we pre-chunk our files by multiple different
        administrative boundaries so that a user can download data in many different tiling schemes based on their needs (example, by county, qquad, or quad). In terms of storage and cost, this leads to data duplication in cloud storage,
        resulting in greater costs in both GB/month and also egress fees when users download more data than they need.
        Providing users with a method to download only the content they need directly from storage allows us to reduce data duplication.
    </li>
    <li class="fragment">
        Compute and Infrastructure Costs - Typically, to retrieve some geographic data from a file via a query or WMS or WFS, an intermediate server must be stood up, and software must be installed and possibly purchased to allow query access to the
        data source. This often involves a database server as well as compute instances, adding additional costs on top of storage costs. Using CNG can alleviate the need to provide such intermediary services since data can be accessed and
        queried directly from file storage using CNG technologies. This reduces overall cloud costs and complexity costs incurred by standing up such services.
    </li>
    <li class="fragment">
        Maintenance Costs - Leading into maintenance costs, removing data duplication and cloud infrastructure from our technology portfolios also reduces the amount of technology our teams need to maintain within our cloud environment. By reducing the number of host server instances and software installed on these servers, we both reduce maintenance costs and also improve our cybersecurity posture, freeing time for our developers to provide user interfaces that can be hosted statically without the need for compute instances. The compute is partially offloaded to the end user, whos personal computers are often more capable than a server whos compute power is shared by hundreds and thousands of users.
    </li>
    <li class="fragment">
        User / Customer Experience - By allowing our users to retrieve only the data they need directly from storage, we can create experiences superior to our click-tile-to-download interfaces. Imagine, for instance, a user wants to download lidar data from four neighboring (or not neighboring) quarter-quad tile files. Using existing methods, a user would have to download the entirety of all four tiles, whereas with CNG data formats, they can draw a bounding box to retrieve data across only the regions of each tile that intersect their drawn region. This offers potential for a significant improvement in user experience.
    </li>
</ol>
</aside>
