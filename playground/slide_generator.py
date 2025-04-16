import datetime

from weasyprint import HTML
import base64

with open("../style.css", "r") as fl:
    fl = fl.read().replace("hidden;", "visible;")
    styles = fl

def functional_design(name, hotel, pax, flight, time, date):
    # Load images as base64 to embed directly in HTML
    def image_to_base64(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"Warning: Image file {image_path} not found.")
            return ""

    # Try to load images, use placeholders if not found
    try:
        logo_base64 = image_to_base64("../images/LOGO.png")
        logo_img = f'<img class="logo-img" src="data:image/png;base64,{logo_base64}"/>'

        departure_base64 = image_to_base64("../images/SALIDA.png")
        departure_img = f'<img class="clock-icon" src="data:image/png;base64,{departure_base64}"/>'

        st_base64 = image_to_base64("../images/ST_LOGO.png")
        st_img = f'<img class="logo-st" src="data:image/png;base64,{st_base64}">'

        id_base64 = image_to_base64("../images/ID.png")
        id_img = f'<img class="id-st" src="data:image/png;base64,{id_base64}">'

        template_base64 = image_to_base64("../images/BG.png")
        bg_img = f'<img class="wave-bg" src="data:image/png;base64,{template_base64}"/>'

        service_base64 = image_to_base64("../images/LLEGADA.png")
        service_img = f'<img class="clock-icon" src="data:image/png;base64,{service_base64}"/>'

        top_base64 = image_to_base64("../images/TOP_RIGHT.png")
        top_img = f'<img class="logo-img" src="data:image/png;base64,{top_base64}"/>'

        bottom_base64 = image_to_base64("../images/BOTTOM_LEFT.png")
        bottom_img = f'<img class="logo-img" src="data:image/png;base64,{bottom_base64}"/>'
    except FileNotFoundError:
        return "Could not get some files to complete the operation"

    design = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Sacbé Transfers - Franco Barrios</title>
            <style>
            {styles}
            </style>
        </head>
        <body>
            <div class="voucher-container">
        
                <div class="corner-top-right" >
                    {top_img}
                </div>
        
                <div class="corner-bottom-left" >
                    {bottom_img}
                </div>
        
                <div>
                    {bg_img}
                </div>
        
                <div class="logo-container">
                    <div class="logo">
                        {st_img}
                    </div>
                </div>
        
                <div class="name-container">
                    <h1 class="first-name">{name[0]}</h1>
                    <h1 class="last-name">{name[1]}</h1>
                </div>
        
                <div class="divider"></div>
        
                <div class="info-container">
                    <div class="left-info">
                       {id_img}
                    </div>
        
                    <div class="right-info">
                        <div class="info-details">
                            <div class="info-row">
                                <div class="info-label">HOTEL:</div>
                                <div class="info-value">{hotel}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">PAX:</div>
                                <div class="info-value">{pax}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">HOUR:</div>
                                <div class="info-value">{time}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">FLIGHT:</div>
                                <div class="info-value">{flight}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">DATE:</div>
                                <div class="info-value">{date}</div>
                            </div>
                        </div>
                        <div class="arrival-container">
                            {service_img}
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    return design

def create_slides():
    slides = """
    Mustafa Khan,11:42 pm,DM 5805,8,Playa Coral B11
    GUILLERMO Rosco,02:00 pm,UA 2122,03,Ocean Blue & Sand
    Luigi Mendez,12:36 pm,B6 1077,02,Secrets Royal Beach PUJ
    """

    slides = slides.strip().split("\n")

    for slide in slides:
        slide = slide.split(",")

        name = slide[0].upper()
        time = slide[1].upper()
        flight = slide[2].upper()
        pax = slide[3].upper()
        hotel = slide[4].upper()
        date = str(datetime.datetime.today()).split()[0]

        HTML(string=functional_design(name.strip().split(" "), hotel, pax, flight, time, date), base_url=".").write_pdf(f"{name.strip()}.pdf")


create_slides()