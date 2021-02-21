import tabula

# df = tabula.read_pdf("fs.pdf", pages='all')
tabula.convert_into("fs.pdf", "output.csv", output_format="csv", pages="all")
