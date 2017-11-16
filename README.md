# EZDoomJukebox
**Recommended additional programs**:
 -  [MP3Gain](http://mp3gain.sourceforge.net/) to adjust music volume, target 89db for good results
 -  [MP3Tag](https://www.mp3tag.de/en/) if your music lacks tags, this can add them relatively easily

You'll need [Python 3](https://www.python.org/downloads/) for this to work, so get that (latest is 3.6.3 at time of writing).

Then you'll need tinytag, so open a command line window and type
`pip install tinytag`
and it should auto-download.

From there, just stick your music into the \Music\ subfolder and double click ezdoombox.py. You should see some output, and a pk3 will be made.
Enjoy your new jukebox! Also make sure your music has some kind of tagging, doesn't matter what version. The tool determines what is and isn't music by the presence of tagging, so anything lacking tags won't work (yet).
