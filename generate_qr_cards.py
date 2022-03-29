from datetime import datetime
from logging import getLogger
from os import path

import click

import settings
from cards_pdf import (CardsPDF, create_qrcode, generate_qrcode,
                       get_file_as_base64, get_qr_image_as_base64)
import utils

logger = getLogger('QR')


def generate_pdf(codes, batch, base_url, url, out):
    logger.debug("Creating sheets..")
    batch_no = f'{batch:02d}'
    pdf_filename = f"qrcards_batch_{batch_no}.pdf"
    pdf_file = path.join(out, pdf_filename)
    pdf_metadata = {
        "Title": f"WFP Self Registration QR Codes",
        "Author": "WFP",
        "Creator": "Script",
        "CreationDate": datetime.utcnow().strftime("D:%Y%m%d%H%M%SZ"),
    }
    logger.debug("Creating PDF cards...")

    # Value in mm, use to_dpi to convert.
    card_design = {
        "preview": False,
        "logo": {
            "image": get_file_as_base64(path.join(settings.TEMPLATES_DIR, "assets/wfp-logo.png")),
            "x": 189,
            "y": 75,
            "w": 174,
            "h": 75,
        },
        "card": {
            "qr": {
                "x": 53,
                "y": 60,
                "w": 80,
                "h": 80,
            },
            "url": {
                "x": 35,
                "y": 195,
            },
            "code": {
                "x": 35,
                "y": 235,
            },
            "batch": {
                "x": 363,
                "y": 248,
            },
            "font_family": "DejaVu Sans Condensed",
            "font_size": 16,
            "font_size_small": 11,
        },
        "url": base_url
    }
    sheets = []
    cards = []
    card_per_sheet = 8
    sheet_cnt = 0
    card_cnt = 0
    for c in codes:
        cards.append({
            "card_number": card_cnt + 1,
            "code": c,
            "qr_image": get_qr_image_as_base64(c),
            "batch": batch_no
        })
        if card_cnt % card_per_sheet == 0:
            sheet_cnt += 1
            sheets.append({
                "sheet_number": sheet_cnt,
            })
        card_cnt += 1

    pdf = CardsPDF(
        sheets,
        cards,
        card_design,
        # work_dir=settings.QR_FILE_DIR
    )
    logger.debug("Writing data to PDF.")
    pdf.create(pdf_file, pdf_metadata)
    logger.debug(f"Save PDF: {pdf_file}")


@click.command()
@click.option("--base-url", type=str, default=settings.SELF_REGISTRATION_BASE_URL, help="Self registration base url e.g https://example.com/reg")
@click.option("--url", type=str, default=settings.SELF_REGISTRATION_URL, help="Self registration url e.g https://example.com/reg/?code=")
@click.option("--cards", type=int, required=True, help="Number of cards to generate")
@click.option("--batch", type=int, required=True, help="Batch number")
@click.option("--out", type=str, help="Output directory", default=settings.BASE_DIR)
def generate_qr_cards(base_url, url, cards, batch, out):
    logger.info('QR Cards generator.')
    logger.info('=' * 80)
    
    last_seq = utils.get_last_seq(dir=out)
    generated_codes = []
    for (i, uid) in utils.unique_id_generator(last_seq=last_seq, upper_bound_id=cards):
        qr_url = f'{url}{uid}'
        create_qrcode(generate_qrcode(qr_url, size=15), uid)
        generated_codes.append(uid)

    utils.save_last_seq(i, dir=out)

    logger.info(f'Total QR code generated: {len(generated_codes)}')
    logger.info(f'Stored last sequence: {last_seq}')
    logger.info(f'Number of cards to generate: {cards}')
    logger.info(f'Last sequence: {i}')
    logger.info(f'Generated unique codes:')
    logger.info('-' * 80)
    for code in generated_codes:
        logger.info(f'{code}')
    logger.info('-' * 80)

    generate_pdf(generated_codes, batch, base_url, url, out)


if __name__ == "__main__":
    generate_qr_cards()
