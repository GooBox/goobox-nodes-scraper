# goobox-nodes-scraper

Scraper for gathering all available nodes for goobox.

## Getting started
To run _Goobox Nodes Scraper_ you need previously to install the requirements and you can either use public docker 
image or build it from sources.

### Requirements
1. *Docker*: Install it following [official docs](https://docs.docker.com/engine/installation/).

### Use public image
You can use public docker image to run the service: 

    docker run goobox/goobox-nodes-scraper:latest

### Build from sources
To build _Goobox Nodes Scraper_ from sources you need to clone this project and build the image.

    git clone https://github.com/goobox/goobox-nodes-scraper.git & cd goobox-nodes-scraper
    docker build -t goobox/goobox-nodes-scraper:latest .

Once build is completed you can run the scraper using ``scrapy`` command from the entry point.

    docker run goobox/goobox-nodes-scraper:latest scrapy

### Help
The entry point has a self-describing help that can be queried.

    docker run goobox/goobox-nodes-scraper:latest -h

Also, each command has its own help.

    docker run goobox/goobox-nodes-scraper:latest scrapy -h
    
### Usage example
To run the scraper for collecting Storj nodes first create a directory to keep the output.

    mkdir output

The scraper is going to gather Storj node information, generate a csv file and put it into the previous directory. If 
you prefer to generate a different kind of export you can use a different format as specified by 
[Scrapy's Feed exports](https://doc.scrapy.org/en/latest/topics/feed-exports.html).

    docker run -v `pwd`/output:/srv/apps/goobox-nodes-scraper/output goobox/goobox-nodes-scraper:latest scrapy crawl storj_nodes -o $OUTPUTDIR/out.csv -t csv

Once the scraper has finished you can get the output csv file.

## License

[GNU GPL v3](https://github.com/GooBox/goobox-nodes-scraper/blob/master/LICENSE)

## Credits

This product includes GeoLite2 data created by [MaxMind](http://www.maxmind.com).
