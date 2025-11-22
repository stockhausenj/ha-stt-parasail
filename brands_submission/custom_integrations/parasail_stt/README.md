# Parasail Speech-to-Text - Brands Repository Submission

This folder contains the icon and logo files needed for submitting to the Home Assistant brands repository.

## Required Files

Place the following PNG files in this directory:

### Required:
- `icon.png` - 256x256px (square, 1:1 aspect ratio)
- `icon@2x.png` - 512x512px (square, 1:1 aspect ratio)
- `logo.png` - landscape format, shortest side 128-256px
- `logo@2x.png` - landscape format, shortest side 256-512px

### Optional (for dark theme support):
- `dark_icon.png` - 256x256px
- `dark_icon@2x.png` - 512x512px
- `dark_logo.png` - landscape format, shortest side 128-256px
- `dark_logo@2x.png` - landscape format, shortest side 256-512px

## Specifications

All files must be:
- PNG format
- Properly compressed and optimized (lossless preferred)
- Transparent background (preferred)
- Cannot use Home Assistant branded images

## How to Create These Files

### Using the Included Script

From the `brands_submission` directory, run:
```bash
./prepare_icons.sh
```

This will automatically convert the `parasail_stt_logo.svg` file to all required PNG formats.

### Manual Conversion

Using ImageMagick:
```bash
# Create icon files (square)
convert parasail_stt_logo.svg -resize 256x256 -gravity center -extent 256x256 icon.png
convert parasail_stt_logo.svg -resize 512x512 -gravity center -extent 512x512 icon@2x.png

# Create logo files (preserve aspect ratio)
convert parasail_stt_logo.svg -resize x256 logo.png
convert parasail_stt_logo.svg -resize x512 logo@2x.png
```

Using Inkscape:
```bash
# Export specific size
inkscape parasail_stt_logo.svg --export-type=png --export-filename=icon.png --export-width=256 --export-height=256
inkscape parasail_stt_logo.svg --export-type=png --export-filename=icon@2x.png --export-width=512 --export-height=512
```

## Next Steps

Once you have all the required PNG files:
1. Fork the Home Assistant brands repository: https://github.com/home-assistant/brands
2. Copy this entire `parasail_stt` folder to `custom_integrations/` in your fork
3. Submit a pull request
4. Reference this integration: https://github.com/stockhausenj/ha-stt-parasail

## Validation

Before submitting, verify:
- [ ] All images are PNG format
- [ ] Icons are exactly 256x256 and 512x512 pixels
- [ ] Logos maintain proper aspect ratio
- [ ] Files are optimized/compressed
- [ ] No Home Assistant branding is used
- [ ] Background is transparent (if applicable)
