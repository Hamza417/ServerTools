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
  YOUTUBE_API_KEY=AIza....
  ```
- Run the files/scripts as needed.

## Webpage
The main domain redirects to a CasaOS mainpage [here](https://cloud417.space/).

The [old page was moved here](https://old.cloud417.space). It's not optimized
for mobile devices yet so a PC is recommended for viewing it. I don't know much webdev
so only skimmed through the basics and made it in a less than an hour.

![](Website/assets/scr_01.png)

I like both of them but second could use some improvements.
Lastly, since it's a
homeserver, it will likely be down most of the time.

## List of Active Domains

- [CasaOS](https://cloud417.space)
- [3D Earth Homepage](https://old.cloud417.space)
- [Jellyin](https://jellyfin.cloud417.space)
- [qBittorrent](https://torrent.cloud417.space)
- [PiHole](https://pihole.cloud417.space)
- [File Manager](https://files.cloud417.space)
- [Speedtest](https://speedtest.cloud417.space)
