from datetime import datetime
from logging import getLogger
import math
from os import path
import os
import shutil

import click

import settings
from cards_pdf import (CardsPDF, create_qrcode, generate_qrcode,
                       get_file_as_base64, get_qr_image_as_base64)
import utils

logger = getLogger('QR')


def generate_pdf(codes, split_by, batch, base_url, url, out, preview, card_template):
    # Value in px calculated with DPI 96, use to_dpi filter in template to convert to DPI 300.
    card_design = {
        "preview": preview,
        "logo": {
            "image": get_file_as_base64(path.join(settings.TEMPLATES_DIR, "assets/wfp-logo.png"))
        },
        "url": base_url
    }
    total_cards = len(codes)
    card_per_sheet = 8

    batch_no = f"{batch:08d}"
    pdf_metadata = {
        "Title": f"WFP Self Registration QR Codes",
        "Author": "WFP",
        "Creator": "Script",
        "CreationDate": datetime.utcnow().strftime("D:%Y%m%d%H%M%SZ"),
    }

    pdf_out_dir = f"{out}/{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    os.mkdir(pdf_out_dir)

    total_files = 1
    if split_by != 0:
        total_files = math.ceil(total_cards / split_by)

    logger.debug("Creating PDF cards...")
    for i in range(0, total_files):
        if total_files > 1:
            file_begin = i * split_by
            file_end = file_begin + split_by
            current_code_partition = codes[file_begin:file_end]
        else:
            current_code_partition = codes
        sheets = []
        cards = []
        sheet_cnt = 0
        card_cnt = 0
        pdf_filename = f"qrcards_batch_{batch_no}_{i+1}.pdf"
        pdf_file = path.join(pdf_out_dir, pdf_filename)
        for c in current_code_partition:
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
            # work_dir=settings.QR_FILE_DIR,
            card_template=card_template
        )
        logger.debug("Writing data to PDF.")
        pdf.create(pdf_file, pdf_metadata)
        logger.debug(f"Save PDF: {pdf_file}")


def generate_code(total_card, url, out):
    last_seq = utils.get_last_seq(dir=out)
    generated_codes = []
    for (i, uid) in utils.unique_id_generator(last_seq=last_seq, upper_bound_id=total_card):
        qr_url = f'{url}{uid}'
        create_qrcode(generate_qrcode(qr_url, size=15), uid)
        generated_codes.append(uid)

    utils.save_last_seq(i, dir=out)

    logger.info(f'Total QR code generated: {len(generated_codes)}')
    logger.info(f'Stored last sequence: {last_seq}')
    logger.info(f'Number of cards to generate: {total_card}')
    logger.info(f'Last sequence: {i}')
    logger.info(f'Generated unique codes:')
    logger.info('-' * 80)
    for code in generated_codes:
        logger.info(f'{code}')
    logger.info('-' * 80)

    return generated_codes

@click.command()
@click.option("--base-url", type=str, default=settings.SELF_REGISTRATION_BASE_URL, help="Self registration base url e.g https://example.com/reg")
@click.option("--url", type=str, default=settings.SELF_REGISTRATION_URL, help="Self registration url e.g https://example.com/reg/?code=")
@click.option("--cards", type=int, required=True, help="Number of cards to generate")
@click.option("--split-by", type=int, default=0, help="Number of PDF files to generate")
@click.option("--batch", type=int, required=True, help="Batch number")
@click.option("--out", type=str, help="Output directory", default=settings.OUTPUT_DIR)
@click.option("--preview", is_flag=True, show_default=True, help="PDF render with PREVIEW background", default=settings.PREVIEW)
@click.option("--card-template", type=str, required=False, default="card.svg")
def generate_qr_cards(base_url, url, cards, split_by, batch, out, preview, card_template):
    logger.info('QR Cards generator.')
    logger.info('=' * 80)
    logger.info(f"Base URL: {base_url}")
    logger.info(f"URL: {url}")
    logger.info(f"Total cards: {cards}")
    logger.info(f"Total cards per file: {split_by}")
    logger.info(f"Batch no: {batch}")
    logger.info(f"Output path: {out}")
    logger.info(f"Preview: {'Yes' if preview else 'No'}")
    logger.info(f"Card template: {card_template}")
    logger.info('-' * 80)

    if split_by > cards:
        logger.error("Total files to split is larger than total number of cards to be generated. Terminating...")
        return

    if not path.exists(out):
        os.mkdir(out)

    generated_codes = generate_code(cards, url=url, out=out)

    generate_pdf(codes=generated_codes, split_by=split_by, batch=batch, base_url=base_url, url=url, out=out, preview=preview, card_template=card_template)

    # Cleanup
    shutil.rmtree(settings.QR_FILE_DIR)


if __name__ == "__main__":
    generate_qr_cards()
