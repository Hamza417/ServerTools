A set of personal server tools and scripts I wrote to make my self-hosting easily manageable.

This repo may contain python scripts, cron job ideas/setups and some commands that I use
frequently or often to do things on my server or automate something.

**Note:** All subdirectories have a `DESC.md` file that describes the scripts in that directory.

## Setup

- Create a `.env` file in the root directory of this repo.
- Add the following variables to the `.env` file (troubleshoot as needed):
  ```python
  JELLYFIN_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
  USER_NAME=xxxxxxxx // Jellyfin username
  JELLYFIN_SERVER=https://xxx.xxx.xxx.xx:xxxx/ | http://localhost:xxxx/ | hosted_domain
  SERVER_IP=xxx.xxx.xxx.xx
  SERVER_USERNAME=xxxxxxxx
  SERVER_PASSWORD=xxxxxx
  ```
- Run the files/scripts as needed.

## Webpage
I have also created a homepage hosted on my homeserver.

![](Website/assets/scr_01.png)

You can visit the [homepage here](https://cloud417.space/), but it's not optimized enough 
for mobile devices yet so a PC is recommended for viewing it. I don't know much webdev
so only skimmed through the basics and made it in a few hours. Also since it's homeserver 
so it may be down most of the time.
