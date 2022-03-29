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
