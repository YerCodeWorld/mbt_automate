import os
from pypdf import PdfReader, PdfWriter

path = os.path.expanduser('~/Desktop')
# We will automate this as well
names = ['Ana maiara soares Vieira', 'Antonio Pérez Valdés']

reader = PdfReader(f"{path}/DEPARTURES_AT_TO_SPLIT.pdf")

for i in range(len(reader.pages)):
    writer = PdfWriter()
    writer.add_page(reader.pages[i])
    with open(f"{path}/{names[i]} - ST.pdf", "wb") as output_file:
        writer.write(output_file)
    print("Operation completed")
