"""Template for HTML document generator."""

from typing import Final

from p5core.html import Tag

html = Tag("html", lang="fr")
head = html.head
body = html.body

meta: Final[str] = "meta"
Tag(meta, parent=head, charset="utf-8")
tmp = Tag(meta, parent=head, content="IE=edge,chrome=1")
tmp.attribs["http-equiv"] = "X-UA-Compatible"
Tag(meta, parent=head, name="viewport", content="width=device-width,minimum-scale=1")
Tag(meta, parent=head, name="generator", content="p5core")
Tag(meta, parent=head, name="robots", content="index, follow")

body.header.p.append("P⁵ : Programmer en Python comme un Pro Par la Pratique")
content = Tag("article", parent=body, class_="content")
body.footer.p.append(
    "© 2020 Vincent Poulailleau"
)  # TODO mettre la bonne année automatiquement
