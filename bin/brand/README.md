# Brand assets

Source for the WordPress.org icon and banner in `.wordpress-org/`. Both are
drawn in SVG, so they can be changed and re-exported at exact sizes.

- `icon.html`: the "vote nook" icon (Midnight & coral). `window.render('A', t)`
  draws the animation at time `t` (0 to 1.35 seconds). The first frame is the
  still design.
- `banner.html`: the 1544×500 banner (render at device scale 0.5 for 772×250).

## Re-export

Needs Node with `playwright-core` and Chrome, Python with Pillow, and gifsicle.

```bash
# Icon frames (34 frames over 1.35s), then the GIF with a 2s pause on the still.
for s in 256 128; do
  node bin/brand/frames.mjs A $s /tmp/frames-$s 34 1.35 "$PWD/bin/brand/icon.html"
  python3 bin/brand/makegif.py /tmp/frames-$s /tmp/icon.gif /tmp/sheet-$s.png
  gifsicle -O3 /tmp/icon.gif -o .wordpress-org/icon-${s}x${s}.gif
done
```

For the banner, screenshot the `#b` element of `banner.html` at 1544×500
(device scale 1 and 0.5). Banners must be PNG or JPG.

Palette: background #2B1E6B → #140F3D, nook #FFF8F1 / #FFE8DC / #FFD4C2,
like pill #FF6B6B → #FF3D7F, hearts #FF3D7F / #FF8FB1, sparkles #FFD166,
dislike icon #7C6FD6.
