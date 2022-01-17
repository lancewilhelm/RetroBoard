from bdflib import reader

with open('./fonts/tom-thumb.bdf', 'rb') as filehandle:
	font = reader.read_bdf(filehandle)

glyph = font[ord('1')]
print(glyph)

for row in glyph.iter_pixels():
	for pixel in row: 
		print(pixel)
	