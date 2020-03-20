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

## Usage
```shell
Usage: generate_qr_cards.py [OPTIONS]

Options:
  --base-url TEXT     Base url e.g https://example.com/reg
  --url TEXT          Url e.g https://example.com/reg/?code=
  --cards INTEGER     Number of cards to generate  [required]
  --split-by INTEGER  Number of PDF files to generate
  --batch INTEGER     Batch number  [required]
  --out TEXT          Output directory
  --preview           PDF render with PREVIEW background  [default: False]
  --help              Show this message and exit.
```

## Run
```shell
# Generate 10 qr codes with batch 1: 1 pdf with 2 sheets
python generate_qr_cards.py --cards 10 --batch 1 --base-url https://example.org/ --url 'https://example.org/code/?code='

# Generate 2 qr codes with batch 2: 1 pdf with 1 sheet
python generate_qr_cards.py --cards 2 --batch 2 --base-url https://example.org/ --url 'https://example.org/code/?code='
```

## Docker
```shell
# Build and tag image
docker build -t newlogic/qrcards_generator .

# Run
# PDF and .last_seq files will save to output directory
docker run -it --rm -v $PWD/output:/app/output newlogic/qrcards_generator --cards 10 --batch 1 --split-by 5 --base-url https://example.org/ --url 'https://example.org/code/?code=' 
# PDF with PREVIEW
docker run -it --rm -v $PWD/output:/app/output newlogic/qrcards_generator --cards 15 --batch 10000000 --split-by 8 --preview
```

## Sample output
```log
QR Cards generator.
================================================================================
Base URL: https://example.org/
URL: https://example.org/code/?code=
Total cards: 15
Total cards per file: 8
Batch no: 10000000
Output path: /app/output
Preview: Yes
--------------------------------------------------------------------------------
Total QR code generated: 15
Stored last sequence: 0
Number of cards to generate: 15
Last sequence: 15
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
0AjD1Y0mPvpw
MQK5ZVMqRGEO
23Aymr0qY0Kx
5nDAqo0ZxKQj
deNMmxLmg2YQ
--------------------------------------------------------------------------------
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
0
convert_svgs_to_pdf: 0.1024s
optimize_pdf: 0.0055s
update_pdf_metadata: 0.0077s
Save PDF: /app/output/20200309094903/qrcards_batch_10000000_1.pdf
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
Rendering sheet number 1.
Sheet number 1 rendering complete.
0
convert_svgs_to_pdf: 0.0621s
optimize_pdf: 0.0050s
update_pdf_metadata: 0.0063s
Save PDF: /app/output/20200309094903/qrcards_batch_10000000_2.pdf
```
