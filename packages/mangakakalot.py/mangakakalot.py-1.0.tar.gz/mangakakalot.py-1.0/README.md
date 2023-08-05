# mangakakalot.py

mangakakalot unofficial python API \
https://mangakakalotpy.readthedocs.io/en/latest/


## usage

you can use this package like this:
```
python -m mangakakalot -l mangakakalot-link -c chapter-number -o pdf-output-file (optional)
```

or in a python project by importing it:

```
from mangakakalot import Manga as mg

toradora = mg.Manga("https://mangakakalot.com/read-gq3vy158504921722")
chapters = toradora.get_chapters()
chapters[-1].download_as_pdf("test.pdf")
```

required packages: `requests, Pillow, BeautifulSoup4`
