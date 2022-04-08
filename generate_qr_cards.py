"""
   Copyright 2020 Newlogic

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
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
            "image": get_file_as_base64(path.join(settings.TEMPLATES_DIR, "assets/newlogic-logo-black.png"))
        },
        "url": base_url
    }
    total_cards = len(codes)
    card_per_sheet = 8

    pdf_metadata = {
        "Title": "QRCards",
        "Author": "QRCards Generator",
        "Creator": "Script",
        "CreationDate": datetime.utcnow().strftime("D:%Y%m%d%H%M%SZ"),
    }

    base_out_dir = f"{out}/{batch:04d}"
    os.mkdir(base_out_dir)
    pdf_out_dir = f"{base_out_dir}/PDFs"
    os.mkdir(pdf_out_dir)
    codes_out_dir = f"{base_out_dir}/Codes"
    os.mkdir(codes_out_dir)

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

        pdf_filename = f"qrcards_batch_{batch:04d}_{i + 1:02d}.pdf"
        pdf_file = path.join(pdf_out_dir, pdf_filename)
        code_file = pdf_file.replace(".pdf", ".txt").replace(pdf_out_dir, codes_out_dir)
        write_codes_to_file(current_code_partition, code_file)

        for c in current_code_partition:
            if card_cnt % card_per_sheet == 0:
                sheet_cnt += 1
                sheets.append({
                    "sheet_number": sheet_cnt,
                })
                batch_prefix = f"{batch:04d}.{i + 1:03d}"
            batch_no = f"{batch_prefix}.{card_cnt + 1:03d}"
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
    return pdf_out_dir


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

def write_codes_to_file(codes, filename):
    with open(filename, 'w') as f:
        for code in codes:
            f.write(f'{code}\n')


@click.command()
@click.option("--base-url", type=str, help="Base url e.g https://example.com/reg")
@click.option("--url", type=str, help="Url e.g https://example.com/reg/?code=")
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

    pdf_out_dir = generate_pdf(codes=generated_codes, split_by=split_by, batch=batch, base_url=base_url, url=url, out=out, preview=preview, card_template=card_template)

    write_codes_to_file(generated_codes, path.join(pdf_out_dir, f"codes_{batch}.txt"))

    # Cleanup
    shutil.rmtree(settings.QR_FILE_DIR)


if __name__ == "__main__":
    generate_qr_cards()
