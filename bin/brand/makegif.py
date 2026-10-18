import sys, glob
from PIL import Image
src, out, sheet = sys.argv[1], sys.argv[2], sys.argv[3]
files = sorted(glob.glob(src + '/f*.png'))
frames = [Image.open(f).convert('RGB') for f in files]
# One palette for every frame, so colours don't shift between frames.
w, h = frames[0].size
strip = Image.new('RGB', (w, h * len(frames)))
for i, f in enumerate(frames):
    strip.paste(f, (0, i * h))
pal = strip.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
durations = [40] * len(q)
durations[-1] = 2000
q[0].save(out, save_all=True, append_images=q[1:], duration=durations, loop=0, optimize=False, disposal=1)
# Contact sheet: every 4th frame.
pick = frames[::4] + [frames[-1]]
cs = Image.new('RGB', (w * len(pick) + 8 * (len(pick) - 1), h), 'white')
for i, f in enumerate(pick):
    cs.paste(f, (i * (w + 8), 0))
cs.save(sheet)
