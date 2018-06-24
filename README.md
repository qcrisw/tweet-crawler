
# Tweet Crawler

Tweet Crawler is a command-line utility that automatically collects tweet data from the Twitter Streaming API. Using this program, you can collect data about specific user-defined topics on Twitter (e.g. "programming", "qatar", "world cup", etc.).

In addition to displaying the collected tweets on the command-line, this utility also stores the JSON for these tweets within a database (MongoDB).

## Getting Started

Building and running Tweet Crawler on your machine should be a pretty straightforward process. In order to do so, you first need to install suitable versions of Docker and Docker Compose.

Making use of Docker (and Docker Compose) greatly simplifies the Tweet Crawler setup process and will make it easier for you to run this program on the platform of your choice.

If you already have up-to-date versions of these programs, feel free to skip straight to the [Configuration](https://github.com/qcrisw/tweet-crawler/#configuration) section.

### Prerequisites

We've included links below to installation instructions for Docker Community Edition on three popular platforms: Windows, Mac, and Ubuntu (Linux).

Furthermore, we've also included instructions to configure the Twitter access credentials for Tweet Crawler.

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

### Configuration

Before you can start using Tweet Crawler, you need to supply the script with credentials to access the Twitter API.

To setup these credentials, follow the [instructions here](http://docs.inboundnow.com/guide/create-twitter-application/).

Once you've got these in hand, run the following command:

```
cp env-sample .env
```
Edit the `.env` file by inserting your Twitter app credentials and save the file.

### Install and Run

If you've fulfilled the above prerequisites, it's very simple to download and run Tweet Crawler from the command line (PowerShell, Terminal, etc.):

Clone the project repository from Github
```
cd ~
git clone https://github.com/qcrisw/tweet-crawler.git
cd tweet-crawler
```

Now, run the following command to build Tweet Crawler:
```
docker-compose build
```

#### Running Tweet Crawler

Simply enter the following command at the terminal:

```
docker-compose run pycrawler <keyword1> <keyword2> ...
```

...where each `<keyword>` is a topic you're interested in streaming from Twitter.

## Built With

* [Tweepy](http://www.tweepy.org/) - Twitter SDK for Python
* [PyMongo](https://api.mongodb.com/python/current/) - Python driver for MongoDB
* [MongoDB](https://www.mongodb.com/) - Database for storing tweets

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
