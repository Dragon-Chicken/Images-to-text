from PIL import Image, ImageDraw, ImageFont
import threading

# gradients
# copy and paste into 'chars'
# keep the first character a space
# ░▒▓█
# ▁▂▃▄▅▆▇█
# ▏▎▍▌▋▊▉█
# ▁▏▂▎▍▄▌▅▋▆▊▇▉█
# ▏▁▎▂▍▌▃▋▄▅▆▊▉▇█
# ▁ ▂ ▃ ▄▌▅▋▆▊▇▉█

# settings
# paste gradients in the '
chars = ' ▏▎▍▌▋▊▉█'
# print the output to the terminal or open it as an image
terminal = False
# quality of the image (higer is better)
quality = 2
# path to the image file
filepath = 'wallpaper.jpg'
# path to font file
font = ImageFont.truetype('/usr/share/fonts/TTF1/JetBrainsMonoNerdFont-Regular.ttf')


# other varibles (don't touch)
nchars = len(chars)
bands = 256/nchars

if terminal:
    samplex = 6 / quality
    sampley = 18 / quality
else:
    samplex = 6 / quality
    sampley = 15 / quality
# for terminal x=3, y=8
# for saved image x=3, y=7

output = ''

im = Image.open(filepath)
width, height = im.size
hs = int(height/sampley)
ws = int(width/samplex)

imagex = ws * 6
imagey = hs * 15

results = [None] * hs
threads = [None] * hs

# get char colour
def getchar(colour):
    for i in reversed(range(nchars)):
        value = bands*i
        if colour == (0, 0, 0):
            return chars[0]
        if colour >= (value, value, value):
            return chars[i]

# multi-threading
def xrow(y, ws):
    output = ''
    ty = y*sampley
    for x in range(ws):
        tx = x*samplex
        output += getchar(im.getpixel((tx, ty)))
    results[y] = output + '\n'

# main
for y in range(len(threads)):
    threads[y] = threading.Thread(target=xrow, args=(y, ws))
    threads[y].start()
    threads[y].join()

# output
output = ''.join(results)

if terminal:
    print(output)

else:
    outputfile = open('output.txt', 'w')
    outputfile.write(output)
    outputfile.close()
    print('Saved to text file!')

    img = Image.new('RGB', (imagex, imagey))
    d = ImageDraw.Draw(img)
    #d.rectangle([0, 0, imagex, imagey], (29, 32, 33))
    if font:
        d.multiline_text((0,0), output, (251,241,199), font)
    else:
        d.multiline_text((0,0), output, (251,241,199))
    img.show()
    print('Image created!')
