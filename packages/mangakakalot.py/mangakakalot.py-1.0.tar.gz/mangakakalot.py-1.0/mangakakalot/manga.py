from bs4 import BeautifulSoup
import requests
import shutil
from PIL import Image
import tempfile
from mangakakalot import errors


class Manga:
    def __init__(self, link):
        if not link.startswith("https://mangakakalot.com"):
            raise errors.NotMangakakalot("This link is not a mangakakalot link!")

        self.link = link
        self.chapters = None

    def __str__(self):
        return str([self.link, self.chapters])

    def __repr__(self):
        return self.__str__()

    def get_chapters(self):
        output = []

        page = requests.get(self.link)
        soup = BeautifulSoup(page.content, "html.parser")

        rows = soup.find_all("div", class_="row")
        if soup.find("div", class_="row title-list-chapter") in rows:
            rows.remove(soup.find("div", class_="row title-list-chapter"))
        else:
            raise errors.WrongMangaId("The manga link you provided is not a valid one!")
        chapters = []
        titles = []

        for i in rows:
            chapters.append(i.find("a")["href"])
            titles.append(i.find("a")["title"])

        for i in range(len(chapters)):
            output.append(Chapter(titles[i], chapters[i]))

        self.chapters = output
        return output


class Chapter:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.server = None
        self.image_directory = None
        self.pages = None

    def __str__(self):
        return str([self.title, self.link, self.server, self.image_directory, self.pages])

    def __repr__(self):
        return self.__str__()

    def get_info(self):
        page = requests.get(self.link)
        soup = BeautifulSoup(page.content, "html.parser")

        images = soup.find_all("img")
        if soup.find("img", alt="Manga Online") in images:
            images.remove(soup.find("img", alt="Manga Online"))

        src_list = images[0]["src"].split("/")

        img_server = src_list[0] + "/" + src_list[1] + "/" + src_list[2]
        chapter_server = src_list[3] + "/" + src_list[4] + "/" + src_list[5] + "/" + src_list[6] + "/"

        self.server = img_server
        self.image_directory = chapter_server

        to_remove = []
        for i in images:
            if not i["src"].startswith(img_server):
                to_remove.append(i)

        for i in to_remove:
            images.remove(i)

        self.pages = len(images)

        return [img_server, chapter_server, len(images)]

    def download_as_pdf(self, pdf):
        if self.server is None:
            self.get_info()

        link = f"{self.server}/{self.image_directory}"
        img_list = []
        e = 0
        tmp_dir = tempfile.TemporaryDirectory()

        for i in range(self.pages):
            i += 1
            image_url = f"{link}/{i}.jpg"

            filename = tmp_dir.name + "/" + image_url.split("/")[-1]
            headers = {'path': f'/{self.image_directory}/{i}.jpg',
                       "referer": "https://mangakakalot.com/"}

            r = requests.get(image_url, headers=headers, stream=True)

            if r.status_code == 200:
                r.raw.decode_content = True

                with open(filename, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                # print('image successfully downloaded: ', filename)
                img_list.append(Image.open(filename))
            else:
                print(f"image couldn't be retrieved ({e + 1})")
                e += 1

        img_list[0].save(pdf, "PDF", resolution=100.0, save_all=True, append_images=img_list[1:])
        tmp_dir.cleanup()
