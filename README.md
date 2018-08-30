

# Tweet Crawler

Tweet Crawler is a command-line utility that automatically collects tweet data from the Twitter Streaming API. Using this program, you can collect data about specific user-defined topics on Twitter (e.g. "programming", "qatar", "world cup", etc.), tweets from specific locations (e.g. San Francisco, New York, etc.), or just listen to a sample of all the tweets in a given language (e.g. English, Arabic, etc.).

In addition to displaying the collected tweets on the command-line, this utility also stores the JSON for these tweets within a database (MongoDB).

## Getting Started

Installing  and running Tweet Crawler on your machine should be a pretty straightforward process. In order to do so, you first need to install suitable versions of Docker and Docker Compose.

Making use of Docker (and Docker Compose) greatly simplifies the Tweet Crawler setup process and will make it easier for you to run this program on the platform of your choice.

If you already have up-to-date versions of these programs, feel free to skip straight to the [Install and Run](https://github.com/qcrisw/tweet-crawler/#install-and-run) section.

### Prerequisites

We've included links below to installation instructions for Docker Community Edition on three popular platforms: Windows, Mac, and Ubuntu (Linux).

After following these instructions, you will be able to directly run the commands in the [Install and Run](https://github.com/qcrisw/tweet-crawler/#install-and-run) section.

#### Windows

 1. Visit the [Install Docker for Windows](https://docs.docker.com/docker-for-windows/install/) page
 2. Follow the instructions listed in the section called [Install Docker for Windows Desktop App](https://docs.docker.com/docker-for-windows/install/#install-docker-for-windows-desktop-app)

#### Mac

 1. Visit the [Install Docker for Mac](https://docs.docker.com/docker-for-mac/install/) page
 2. After downloading the `.dmg` file, follow the instructions listed in the section called [Install and Run Docker for Mac](https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac)

#### Ubuntu

 1. Visit the [Get Docker CE for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/) page
 2. Follow the instructions listed under the [Install Docker CE](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-docker-ce) section
 3. To install Docker Compose, visit the [Install Docker Compose](https://docs.docker.com/compose/install/) page
 4. Follow the instructions under the [Install Compose](https://docs.docker.com/compose/install/#install-compose) section
 5. Follow the Linux [post-install instructions](https://docs.docker.com/install/linux/linux-postinstall/)

### Install and Run

If you've fulfilled the above prerequisites, it's very simple to download and run Tweet Crawler from the command line (PowerShell, Terminal, etc.):

Clone the project repository from Github
```
cd ~
git clone https://github.com/qcrisw/tweet-crawler.git
cd tweet-crawler
```

#### Configuration

Before you can run Tweet Crawler, you need to provide valid credentials to access the Twitter API.

To setup these credentials, follow the [instructions here](https://www.slickremix.com/docs/how-to-get-api-keys-and-tokens-for-twitter/).

Once you've got these in hand, run the following command:

```
cp env-sample .env
```
Edit the `.env` file by inserting your Twitter app credentials and save the file.

Also, If you want to use the crawler with a proxy server, specify the proxy IP address within the `.env` file.

#### Running Tweet Crawler

##### Crawling tweets about specific topic(s)

```
docker-compose run pycrawler track <keyword1> <keyword2> ...
```

...where each `<keyword>` is a topic you're interested in streaming from Twitter.

##### Crawling all tweets in a given language

```
docker-compose run pycrawler sample <language-code>
```

...where `<language-code>` is an *optional* value drawn from the list of [Twitter - Supported Languages](https://developer.twitter.com/en/docs/twitter-for-websites/twitter-for-websites-supported-languages/overview.html).

If you leave this field empty, the crawler will sample *all* tweets posted on Twitter.

##### Crawling tweets in the given area(s)

```
docker-compose run pycrawler geo <bound-box-1> <bound-box-2> ...
```

...where each `<bound-box>` is a space-separated list of coordinates specified in the following order:

1. longitude of left edge
2. latitude of bottom edge
3. longitude of right edge
4. latitude of top edge

For example, the following will crawl all tweets from the United States (minus Alaska & Hawaii):

```
docker-compose run pycrawler geo -125.2 25.6 -66.9 49.6
```

In addition to a single area, it's possible to crawl tweets from multiple, disjoint areas by specifying multiple bounding boxes.

For example, the following will crawl all tweets from South Korea and the United States (minus Alaska & Hawaii):

```
docker-compose run pycrawler geo 123.7 32.7 131.1 39.0 -125.2 25.6 -66.9 49.6
```

For best results, you can use a tool like [BoundingBox](https://boundingbox.klokantech.com/), with output mode set to CSV, to fine-tune the selected bounding box.

## Contributing to the Codebase

If you are only interested in _using_ Tweet Crawler, then you can simply ignore this section.

However, if you would like to modify the source code and/or contribute to the project, reading this section is essential to building the source code on your development machine.

### Development process

At a high level, the Tweet Crawler development process consists of three main steps, which are repeated many times:

 1. Update the source code with new changes
 2. Build Docker images for the updated version of project
 3. Run project to test updated codebase

The source code can be updated using any IDE or editor of your choice.

We've already covered how to _run_ Tweet crawler in the [Running the Tweet Crawler](https://github.com/qcrisw/tweet-crawler#running-tweet-crawler) section.

As such, we will only give detailed instructions on how to _build_ the Docker images required to run a development version of the Tweet Crawler.

### Build process

 1. Add the`build` key to the `pycrawler` service in `docker-compose.yaml`
```
pycrawler:
  build: .
  image: qcrisw/pycrawler:latest
  <rest of service definition>
```
 2. Update the `image` key for the `pycrawler` service in `docker-compose.yaml`
```
pycrawler:
  build: .
  image: <your-org-name-here>/pycrawler:latest
  <rest of service definition>
```
 3. Clone the [`qcrisw/task-worker`](https://github.com/qcrisw/task-worker) repository
```
git clone https://github.com/qcrisw/task-worker.git
```
 4. Add the `build` key to the `rqworker` service in `docker-compose.yaml`
```
rqworker:
  build: ./task-worker
  image: qcrisw/rqworker:latest
  <rest of service definition>
```
 5. Update the `image` key for the `rqworker` service in `docker-compose.yaml`
```
rqworker:
  build: ./task-worker
  image: <your-org-name-here>/rqworker:latest
  <rest of service definition>
```
 6. Run `docker-compose build` from the project directory
 7. Wait until the build process is complete

At this point, you can run the Tweet Crawler project using the newly built Docker images, as outlined in the [Running the Tweet Crawler](https://github.com/qcrisw/tweet-crawler#running-tweet-crawler) section.

If you want to re-build the project after updating the source code, simply re-run the `docker-compose build` command from the main project directory.

### Development FAQs

* How do I add new types of tasks to the message queue?
  1. Define a new task function in the `mq/tasks.py` file
  2. Add any new dependencies to `requirements.txt`
  3. Run `cp mq/tasks.py task-worker/mq/tasks.py` from the main project directory
  4. Run `cp requirements.txt task-worker/requirements.txt` from the main project directory

 * Why does Docker still run my old code even after I update the source code?
    * By default, running `docker-compose run` will **not** build the newly updated Docker images
    * In order to run the updated code, you need to run `docker-compose build` followed by `docker-compose run`

* Where can I find the collected tweet data?
  * The collected tweet data is stored as a set of "daily collections" named using "Year_Month_Day" format (UTC) in MongoDB
  * To access the tweet objects stored in these collections, use the following steps:
    1. Run `docker-compose ps` to see the full list of running containers
    2. Find the name of the running `mongo` container (e.g. `tweet-crawler_mongo_1`)
    3. Run `docker exec -it <name-of-mongo-container> bash`, followed by `mongo social-analytics`
    4. You can use the [Mongo Shell Command Reference](https://docs.mongodb.com/manual/reference/mongo-shell/) to query & access the data contained in MongoDB

* How can I export the raw data outside MongoDB?
    1. Run `docker-compose ps` to see the full list of running containers on the host machine
    2. Find the name of the running `mongo` container (e.g. `tweet-crawler_mongo_1`)
    3. Run `docker exec -it <name-of-mongo-container> bash`
    4. Run `mongoexport --db=social_analytics --collection=<daily-collection-name> --out=<output-file-name>`
    5. Wait until the export process is completed
    6. `exit` from the `rqworker` container
    7. From the host machine, run `docker container cp tweet-crawler_mongo_1:<output-file-name> <output-file-name>`
    8. At this point, a dump of the raw tweet data is present on your host machine with the given `<output-file-name>`

* How can I start up MongoDB without starting up the crawler?
  1. To stop all running containers in the Tweet Crawler project, run `docker-compose down`
  2. To start up only MongoDB, run `docker-compose run --detach mongo`

* Why can't I see the logs of `rqworker` containers using `docker logs`?
  * Due to certain implementation issues, the logs of each `rqworker` are not accessible via `docker logs`
  * However, you can still access the `rqworker` logs using the following steps:
    1. Run `docker-compose ps` to list all running containers
    2. Find the name of a running `rqworker` container (e.g. `tweet-crawler_rqworker_1`)
    3. Run `docker exec -it <name-of-rqworker-container> bash`
    4. Run `cat logs.txt` to view the logs generated by the worker

## Built With

* [Tweepy](http://www.tweepy.org/) - Twitter SDK for Python
* [PyMongo](https://api.mongodb.com/python/current/) - Python driver for MongoDB
* [MongoDB](https://www.mongodb.com/) - Database for long-term storage of tweets
* [RQ](http://python-rq.org/) - Python-based Redis Queue library
* [Redis](https://redis.io/) - In-memory DB for storing tweets

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
