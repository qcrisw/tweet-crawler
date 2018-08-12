
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

## Built With

* [Tweepy](http://www.tweepy.org/) - Twitter SDK for Python
* [PyMongo](https://api.mongodb.com/python/current/) - Python driver for MongoDB
* [MongoDB](https://www.mongodb.com/) - Database for long-term storage of tweets
* [RQ](http://python-rq.org/) - Python-based Redis Queue library
* [Redis](https://redis.io/) - In-memory DB for storing tweets

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
