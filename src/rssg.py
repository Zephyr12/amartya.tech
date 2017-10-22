import yaml
import jinja2
import markdown

from os import makedirs, listdir, walk
from os.path import join, isfile, basename
import shutil


FILE_ROOT = "./files"
OUTPUT_ROOT = "../www"
SITE_NAME = "Amartya's Site"


categories = next(walk(FILE_ROOT))[1]

site_pages = {category: [filename
                         for filename in listdir(join(FILE_ROOT, category)) 
                         if isfile(join(FILE_ROOT, category, filename))]
                for category in categories}

for content in listdir(OUTPUT_ROOT):
    shutil.rmtree(join(OUTPUT_ROOT, content))

env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(join(FILE_ROOT, "templates")),
        autoescape=jinja2.select_autoescape([]))

for category, files in site_pages.items():
    if category == "static":
        shutil.copytree(join(FILE_ROOT, "static"), join(OUTPUT_ROOT, "static"))
    elif category not in ["templates", "ignore"]:
        makedirs(join(OUTPUT_ROOT, category))
        template = env.get_template(category + ".html")
        for file in files:
            if not file.startswith("."):
                print(file)
                documents = [doc for doc in open(join(FILE_ROOT, category, file)).read().split("---\n")]
                metadata = yaml.load(documents[0])
                variables = {"site_pages": site_pages, "site_name": SITE_NAME, **metadata}
                documents = [jinja2.Template(markdown.markdown(document)).render(variables) for document in documents[1:]]
                variables["documents"] = documents
                with open(join(OUTPUT_ROOT, category, file.split(".")[0] + ".html"), "w+") as outfile:
                    outfile.write(template.render(**variables))
    else:
        pass
