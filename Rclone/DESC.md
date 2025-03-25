## Rclone

Scripts to make using Rclone easier.

### browser.py

Python script to quickly run Rclone browser in any python environment. I use it to run 
this in Windows if I'm not in an SSH session.

### browser.sh
Same as `.py` script but in a
Shell format to run Rclone browser in a Linux environment. I use this in my SSH sessions.

You can move this script into your /usr/bin/ directory to run it from anywhere.

```shell
sudo mv browser.sh /usr/local/bin/
chmod +x /usr/local/bin/browser.sh
browser.sh
```

Rename the script to whatever you want to call it for your convenience.