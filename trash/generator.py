from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

font_config = FontConfiguration()

HTML("index.html", base_url=".").write_pdf(
    "TEST.pdf",
    stylesheets=[CSS("style.css", font_config=font_config)],
    font_config=font_config
)