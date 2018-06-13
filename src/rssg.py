import yaml
import pdb
import jinja2
import markdown

from os import makedirs, listdir, walk
from os.path import join, isfile, basename
import shutil


FILE_ROOT = "./files"
OUTPUT_ROOT = "../www"
SITE_NAME = "Amartya's Site"


categories = next(walk(FILE_ROOT))[1]

site_pages = {category: {filename: yaml.load(open(join(FILE_ROOT, category, filename)).read().split("---\n")[0]) if category != "static" else {}
                         for filename in listdir(join(FILE_ROOT, category))
                         if isfile(join(FILE_ROOT, category, filename))}
                for category in categories if category not in ["templates", "ignore"]}
print(site_pages)
base_variables =  {"site_pages": site_pages, "site_name": SITE_NAME}

for content in listdir(OUTPUT_ROOT):
    shutil.rmtree(join(OUTPUT_ROOT, content))

env = jinja2.Environment(
        loader=jinja2.loaders.FileSystemLoader(join(FILE_ROOT, "templates")),
        autoescape=jinja2.select_autoescape([]))

for category, document_set in site_pages.items():
    if category == "static":
        shutil.copytree(join(FILE_ROOT, "static"), join(OUTPUT_ROOT, "static"))
    elif category not in ["templates", "ignore"]:
        makedirs(join(OUTPUT_ROOT, category))
        template = env.get_template(category + ".html")
        for document_name, metadata in document_set.items():
            if not document_name.startswith("."):
                print(document_name)
                documents = [doc for doc in open(join(FILE_ROOT, category, document_name)).read().split("---\n")]
                variables = {**base_variables, **metadata}
                documents = [markdown.markdown(jinja2.Template(document).render(variables)) for document in documents[1:]]
                variables["documents"] = documents
                with open(join(OUTPUT_ROOT, category, document_name.split(".")[0] + ".html"), "w+") as outfile:
                    outfile.write(template.render(**variables))
    else:
        pass
