import datetime
from datetime import timedelta
import os
from weasyprint import HTML
import base64

from src.utils import colored_print

path = os.path.expanduser("~/Desktop")
file = "TODAY.csv"

# Load images as base64 to embed directly in HTML
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Warning: Image file {image_path} not found.")
        return ""

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
    arrival_img = f'<img class="clock-icon" src="data:image/png;base64,{service_base64}"/>'

    top_base64 = image_to_base64("../images/TOP_RIGHT.png")
    top_img = f'<img class="logo-img" src="data:image/png;base64,{top_base64}"/>'

    bottom_base64 = image_to_base64("../images/BOTTOM_LEFT.png")
    bottom_img = f'<img class="logo-img" src="data:image/png;base64,{bottom_base64}"/>'
except FileNotFoundError:
    print("Could not get some files to complete the operation")

def functional_design(name, hotel, pax, time, date, company="at", service="a", flight=None):
    # Change logo depending on type.
    # Simply toggle visibility for the id variation.
    with open("../style.css", "r") as fl:
        fl = fl.read()
        if service == "d":  # Used the comment to identify the exact line I want to replace.
            fl = fl.replace("flex;  /*collapse*/", "none;")
        if company == "st":
            fl = fl.replace("hidden", "visible")  # Only case where this happens, should use the same comment strategy

    styles = fl
    surname = ' '.join([part for part in name[1:]]) if len(name) > 1 else name[1]

    logo = logo_img if company == "at" else st_img
    service_image = arrival_img if service == "a" else departure_img

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
                        {logo}
                    </div>
                </div>
        
                <div class="name-container">
                    <h1 class="first-name">{name[0]}</h1>
                    <h1 class="last-name">{surname}</h1>
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
                            <div class="info-row-flight">
                                <div class="info-label">FLIGHT:</div>
                                <div class="info-value">{flight}</div>
                            </div>
                            <div class="info-row">
                                <div class="info-label">DATE:</div>
                                <div class="info-value">{date}</div>
                            </div>
                        </div>
                        <div class="arrival-container">
                            {service_image}
                        </div>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
    return design

def create_slides(data, company, service):
    slides = data.strip().split("\n")

    for slide in slides:

        slide = slide.split(",")

        name = slide[0].upper()
        time = slide[1].upper()
        # For we will keep checking the flights manually and introducing them here as hard coded values
        flight = ""
        if service[3:] == "arrivals":
            flight = slide[2]
            pax = slide[3]
            hotel = slide[4].upper()
        else:
            pax = "0"+slide[2] if int(slide[2]) < 10 else slide[2]
            hotel = slide[3].upper()

        date = (str(datetime.datetime.today() + timedelta(days=1))).split()[0]
        # date = str(datetime.datetime.today())

        # might also add logic to delete the current files in the directory
        output_dir = f"{path}/OPERATIONS/{(company+service[0]).upper()}/{name.strip()} - {company.upper()}.pdf"
        HTML(
            string=functional_design(
                name.strip().split(" "), hotel, pax, time, date, flight=flight, company=company.lower(), service=service.lower()), base_url="."
        ).write_pdf(output_dir)

        colored_print(f"Slide for {name} done", "green")

    colored_print("Done!", "green")

