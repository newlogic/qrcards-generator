# QR code card pdf generator

## Requirements
- Python 3
- rsvg-convert
- mutool

## Debian / Ubuntu env install
```shell
sudo apt-get install librsvg2-bin mupdf-tools
```

## Pypi dependencies
```shell
pip install -r requirements.txt
```

## Run
```shell
# Generate 10 qr codes with batch 1: 1 pdf with 2 sheets
python generate_qr_cards --cards 10 --batch 1 --base-url https://ukr.reg.scope.wfp.org/ --url 'https://ukr.reg.scope.wfp.org/ukr/code/?code='

# Generate 2 qr codes with batch 2: 1 pdf with 1 sheet
python generate_qr_cards --cards 2 --batch 2 --base-url https://ukr.reg.scope.wfp.org/ --url 'https://ukr.reg.scope.wfp.org/ukr/code/?code='
```

## Docker
```shell
# Build and tag image
docker build -t newlogic/qrcards_generator .

# Run
# PDF and .last_seq files will save to output directory
docker run -it --rm -v $PWD/output:/output newlogic/qrcards_generator --cards 10 --batch 1 --base-url https://ukr.reg.scope.wfp.org/ --url 'https://ukr.reg.scope.wfp.org/ukr/code/?code=' --out /output

# PDF with PREVIEW
docker run -it --rm -v $PWD/output:/output newlogic/qrcards_generator --cards 10 --batch 1 --base-url https://ukr.reg.scope.wfp.org/ --url 'https://ukr.reg.scope.wfp.org/ukr/code/?code=' --out /output --preview
```


## Sample output
```log
QR Cards generator.
================================================================================
Total QR code generated: 10
Stored last sequence: 0
Number of cards to generate: 10
Last sequence: 10
Generated unique codes:
--------------------------------------------------------------------------------
jN9rZyRmngxD
Wlwy1vymd4g0
ykz51Ezq2jgR
PNVXZRVZrenL
jlr917G1O3X0
wbP2ZPYm3Q50
LYEJ19M1orAe
5JX618Yqrd4L
r6BX1w5ZG0Jx
2Y0712KqMe63
--------------------------------------------------------------------------------
Creating sheets..
Creating PDF cards...
Writing data to PDF.
Generating SVGs.
Preparing PDF sheet number 1.
[card 1].
[card 1] Rendering card data...
[card 1] Card rendering complete.
[card 2].
[card 2] Rendering card data...
[card 2] Card rendering complete.
[card 3].
[card 3] Rendering card data...
[card 3] Card rendering complete.
[card 4].
[card 4] Rendering card data...
[card 4] Card rendering complete.
[card 5].
[card 5] Rendering card data...
[card 5] Card rendering complete.
[card 6].
[card 6] Rendering card data...
[card 6] Card rendering complete.
[card 7].
[card 7] Rendering card data...
[card 7] Card rendering complete.
[card 8].
[card 8] Rendering card data...
[card 8] Card rendering complete.
Rendering sheet number 1.
Sheet number 1 rendering complete.
Preparing PDF sheet number 2.
[card 9].
[card 9] Rendering card data...
[card 9] Card rendering complete.
[card 10].
[card 10] Rendering card data...
[card 10] Card rendering complete.
Rendering sheet number 2.
Sheet number 2 rendering complete.
0
convert_svgs_to_pdf: 0.0679s
optimize_pdf: 0.0034s
update_pdf_metadata: 0.0056s
Save PDF: /output/qrcards_batch_01.pdf
```
