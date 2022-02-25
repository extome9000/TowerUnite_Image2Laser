from PIL import Image
import colorsys

def createImage(filename: str) -> None:
	image = Image.open(filename)
	image = image.resize((20,20))
	image = image.transpose(Image.FLIP_LEFT_RIGHT)
	image = image.rotate(90)
	imageWidth, imageHeight = image.size

	hues = {}
	sats = {}
	vals = {}
	for i in range(360):
		hues.update({i:[]})
	for i in range(11):
		sats.update({i:[]})
		vals.update({i:[]})

	for x in range(imageWidth):
		for y in range(imageHeight):
			pixel = image.getpixel((x,y))
			h,s,v = colorsys.rgb_to_hsv(pixel[0],pixel[1],pixel[2])
			hues[int(h*360)].append(imageWidth*x+y)
			sats[int(s*10)].append(imageWidth*x+y)
			vals[int((v/255)*10)].append(imageWidth*x+y)

	popularHue = 0
	popularHueLen = 0
	for h in hues.items():
		hLen = len(h[1])
		if hLen > popularHueLen:
			popularHue = h[0]
			popularHueLen = hLen
	hues.pop(popularHue)

	popularSat = 0
	popularSatLen = 0
	for s in sats.items():
		sLen = len(s[1])
		if sLen > popularSatLen:
			popularSat = s[0]
			popularSatLen = sLen
	sats.pop(popularSat)

	popularVal = 0
	popularValLen = 0
	for v in vals.items():
		vLen = len(v[1])
		if vLen > popularValLen:
			popularVal = v[0]
			popularValLen = vLen
	vals.pop(popularVal)

	print("# Image/GIF Dot Matrix Display | Script by extome")
	print(f"# Revision 2 | \"{filename}\"\n")
	print("x'=x;")
	print("y'=y;")
	print(f"h={popularHue};")
	print(f"s={popularSat/10:.1f};")
	print(f"v={popularVal/10:.1f};")
	print("i=index;")

	ifStatements = 0
	print("\n# Hue\n")

	for key,value in hues.items():
		if value:
			longif = ""
			print("h=if(",end="")
			for p in value:
				longif += f"i=={p}|"
			print(f"{longif[:-1]},{key},h);")
			ifStatements += 1

	print("\n# Saturation\n")

	for key,value in sats.items():
		if value:
			longif = ""
			print("s=if(",end="")
			for p in value:
				longif += f"i=={p}|"
			print(f"{longif[:-1]},{key/10:.1f},s);")
			ifStatements += 1

	print("\n# Value\n")

	for key,value in vals.items():
		if value:
			longif = ""
			print("v=if(",end="")
			for p in value:
				longif += f"i=={p}|"
			print(f"{longif[:-1]},{key/10:.1f},v);")
			ifStatements += 1

	print(f"\n# ifStatements: {ifStatements}")

def createGIF(filename: str) -> None:
	image = Image.open(filename)
	print("# Image/GIF Dot Matrix Display | Script by extome")
	print(f"# Revision 2 | \"{filename}\"\n")
	print("x'=x;")
	print("y'=y;")
	print("i=index;") # Shorthand index for less characters
	print("r=10;") # Controls speed of GIF
	print("t=round(r*time);")
	frames = image.n_frames
	print(f"m={frames};")

	for f in range(0,frames):
		image.seek(f)
		frame = image.convert("RGB")
		frame = frame.resize((20,20))
		frame = frame.transpose(Image.FLIP_LEFT_RIGHT)
		frame = frame.rotate(90)
		imageWidth, imageHeight = frame.size
		frameNum = image.tell()

		hues = [[] for x in range(360)]
		sats = [[] for x in range(255)]
		vals = [[] for x in range(255)]

		for x in range(imageWidth):
			for y in range(imageHeight):
				r,g,b = frame.getpixel((x,y))
				convertedPixel = colorsys.rgb_to_hsv(r,g,b)
				hues[int(convertedPixel[0]*360)].append((imageWidth*x)+y)
				sats[int(convertedPixel[1]*10)].append((imageWidth*x)+y)
				vals[int((convertedPixel[2]/255)*10)].append((imageWidth*x)+y)

		print("\n# Hue\n")

		for i,hs in enumerate(hues):
			if hs:
				longif = ""
				print("h=if(",end="")
				for p in hs:
					longif += f"i=={p}|"
				print(f"{longif[:-1]}&(t%m)=={frameNum},{i},h);")

		print("\n# Saturation\n")

		for i,ss in enumerate(sats):
			if ss:
				longif = ""
				print("s=if(",end="")
				for p in ss:
					longif += f"i=={p}|"
				print(f"{longif[:-1]}&(t%m)=={frameNum},{i/10:.1f},s);")

		print("\n# Value\n")

		for i,vs in enumerate(vals):
			if vs:
				longif = ""
				print("v=if(",end="")
				for p in vs:
					longif += f"i=={p}|"
				print(f"{longif[:-1]}&(t%m)=={frameNum},{i/10:.1f},v);")

# createImage("example.png")
# createGIF("example.gif")
