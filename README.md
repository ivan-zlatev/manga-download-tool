# manga-download-tool

A LUI tool for downloading manga from http://mangareader.net/ and creating cbz archives from a group of downloaded chapters.

usage: download-manga.py [-h] -s START -f FINISH -m MANGA [-p PATH] [-g GROUP] [-c]

  -h, --help            show this help message and exit
  -s START, --start START
                        An integer argument for first chapter to download.
  -f FINISH, --finish FINISH
                        An integer argument for last chapter to download.
  -m MANGA, --manga MANGA
                        A string agrument for the name of the manga to be
                        downloaded. Should be taken from the url in
                        http://mangareader.net
  -p PATH, --path PATH  An optional string argument for download path. If not
                        given, the manga will be downloaded at /home/izlatev
                        /download-manga/<MANGA>
  -g GROUP, --group GROUP
                        An optional argument for grouping the downloaded
                        chapter in cbz archives. If not given, the manga will
                        be grouped in 5 chapter archives.
  -c, --clear           An optional argument for clearing the images after
                        grouping in cbz archives.

