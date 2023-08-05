from mangakakalot import manga
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", help="pdf file name (optional)")
parser.add_argument("-l", "--link", help="link to manga - e.g. https://mangakakalot.com/read-gq3vy158504921722", required=True)
parser.add_argument("-c", "--chapter", help="number of chapter to download", required=True, type=int)

args = parser.parse_args()
ch = args.chapter

mg = manga.Manga(args.link)
chapters = mg.get_chapters()

chapter = chapters[-ch]
chapter.get_info()

print(chapter)

output = args.output
if output is None:
    output = chapter.title + ".pdf"

output = output.replace(":", "-")
output = output.replace("/", "-")
output = output.replace("\\", "-")
output = output.replace("|", "-")
output = output.replace("?", "-")
output = output.replace("*", "-")
output = output.replace("\"", "-")
output = output.replace("<", "-")
output = output.replace(">", "-")

chapter.download_as_pdf(output)
print(f"saved manga to: {output}")
