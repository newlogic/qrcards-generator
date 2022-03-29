import base64
import datetime
import io
import os
import shutil
import subprocess
import tempfile
from logging import getLogger
from os import path
from timeit import default_timer as timer

import qrcode
from pdfrw import IndirectPdfDict, PdfReader, PdfWriter
from PIL import Image, ImageDraw
from qrcode.image.pil import PilImage

import settings
import template

logger = getLogger(__name__)


def mm2px(mm, dpi=300):
    return int((mm * dpi) / 25.4)


class PilImage(PilImage):
    def new_image(self, **kwargs):
        mode = '1'  # || '1'
        size = (self.pixel_size, self.pixel_size)
        img = Image.new(mode, size, 'white')
        self.fill_color = 'black'
        self._idr = ImageDraw.Draw(img)
        return img


def generate_qrcode(value, size=10, error_correction=qrcode.constants.ERROR_CORRECT_Q):
    """
    @param value: value of the qrcode
    @param size: size in mm
    @param error_correction: error correction level
    """
    # return qrcode.make(value)

    # code based on SCOPE's BasePDF
    qr = qrcode.QRCode(
        error_correction=error_correction,
        image_factory=PilImage,
        box_size=6,
        border=0,
    )
    qr.add_data(value)
    img = qr.make_image(fill_color='black', back_color='white')
    output = io.BytesIO()
    img.thumbnail((mm2px(size),) * 2, resample=Image.NEAREST)
    img.save(output, 'PNG', dpi=(300, 300))
    contents = output.getvalue()
    output.close()
    return contents


def create_qrcode(img, code):
    if not os.path.exists(settings.QR_FILE_DIR):
        os.mkdir(settings.QR_FILE_DIR)

    filename = f'{code}.png'
    with open(os.path.join(settings.QR_FILE_DIR, filename), 'wb') as f:
        f.write(img)
    return filename


def get_file_as_base64(file_path):
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()


def get_qr_image_as_base64(code):
    return get_file_as_base64(file_path=os.path.join(settings.QR_FILE_DIR, f'{code}.png'))


def get_fontconfig_env():
    font_conf_path = f"{settings.FONTS_DIR}/fonts.conf"
    fonts_path = path.dirname(font_conf_path)
    env = os.environ.copy()
    env.update(
        {
            #  - Track loading of font information at startup
            #  - Monitor which config files are loaded
            # See: https://www.freedesktop.org/software/fontconfig/fontconfig-user.html#DEBUG
            "FC_DEBUG": "1032",
            # Configure XDG_DATA_HOME sot the prefix `xdg` will point to our fonts path.
            "XDG_DATA_HOME": fonts_path,
            # Path of our `fonts/conf` file
            "FONTCONFIG_FILE": font_conf_path,
        }
    )
    return env


def convert_svgs_to_pdf(svg_files, output):
    if not svg_files:
        raise ValueError("No SVG to render.")

    # FIXME: Check version of rsvg-convert
    start = timer()
    with open(os.devnull, "wb") as devnull:
        return_value = subprocess.check_call(
            [
                "rsvg-convert",
                "-f",
                "pdf",
                # "--page-width=210mm",
                # "--page-height=297mm",
                "-d",
                "300",
                "-p",
                "300",
                "-o",
                output,
            ]
            + svg_files,
            stdout=devnull,
            env=get_fontconfig_env(),
        )
        logger.debug(return_value)
    logger.debug(f"convert_svgs_to_pdf: {timer() - start:.4f}s")


def optimize_pdf(input, output):
    start = timer()
    with open(os.devnull, "wb") as devnull:
        subprocess.call(
            [
                "mutool",
                "clean",
                "-gggg",
                input,
                output,
            ],
            stdout=devnull,
        )
    logger.debug(f"optimize_pdf: {timer() - start:.4f}s")


def update_pdf_metadata(pdf_file, metadata):
    start = timer()
    base_metadata = {
        "Creator": "WFP",
        "Producer": f"WFP Self Registration",
        "ModDate": datetime.datetime.utcnow().strftime("D:%Y%m%d%H%M%SZ"),
    }
    if metadata:
        base_metadata.update(metadata)

    trailer = PdfReader(pdf_file)
    trailer.Info = IndirectPdfDict(**base_metadata)
    writer = PdfWriter(version=trailer.version)
    writer.trailer = trailer
    writer.write(pdf_file)
    logger.debug(f"update_pdf_metadata: {timer() - start:.4f}s")


def prepare_image_for_pdf(input, output, size=None, color=(255, 255, 255)):
    img = Image.open(input)
    if size:
        img.thumbnail(size, Image.ANTIALIAS)
    if img.mode == "RGBA":
        # It's more space efficient to use a PNG
        # without an alpha channel. Otherwise cairo will create
        # a unique mask for this image.
        background = Image.new("RGB", img.size, color)
        background.paste(img, mask=img.split()[3])
        img = background
    img.save(output, "PNG")


class CardsPDF():

    page_template = template.get_template("page.svg")
    card_template = template.get_template("card.svg")
    work_dir = None

    def __init__(self, sheets, cards, card_design, debug=False, work_dir=None):
        self.sheets = sheets
        self.cards = list(cards)
        self.card_design = card_design
        self.debug = debug
        self.work_dir = work_dir

    def copy_image(self, image, filename, resize=False, verbatim=False):
        if resize and verbatim:
            raise ValueError("'resize' and 'verbatim' are incompatible options.")

        dst = path.join(self.work_dir, filename)
        if verbatim:
            shutil.copyfile(image, dst)
        else:
            prepare_image_for_pdf(image, dst, resize)

        return filename

    def create_qrcode(self, value, prefix):
        filename = f"{prefix}-qrcode.png"
        with open(path.join(self.work_dir, filename), "wb") as f:
            f.write(generate_qrcode(value))
        return filename

    def create(self, filename, metadata=None):
        can_clean = False
        if not self.work_dir:
            self.work_dir = tempfile.mkdtemp(suffix="wfp-self-reg")
            if self.debug:
                logger.debug(self.work_dir)
            else:
                can_clean = True

        try:
            self.svg_files = []
            self.generate_svgs()

            rsvg_pdf = path.join(self.work_dir, "rsvg.pdf")
            convert_svgs_to_pdf(self.svg_files, rsvg_pdf)

            final_pdf = path.join(self.work_dir, "result.pdf")
            optimize_pdf(rsvg_pdf, final_pdf)
            update_pdf_metadata(final_pdf, metadata)

            if isinstance(filename, str):
                shutil.copy(final_pdf, filename)
            else:
                with open(final_pdf) as f:
                    filename.write(f.read())
        finally:
            if can_clean:
                shutil.rmtree(self.work_dir)

    def render_card(self, card, index):
        print(f"[card {card['card_number']}].")
        context = {
            "index": index,
            "card": card,
            "card_design": self.card_design
        }

        print(f"[card {card['card_number']}] Rendering card data...")
        rendered_card = self.card_template.render(context)
        print(f"[card {card['card_number']}] Card rendering complete.")

        return rendered_card


    def render_page(self, sheet):
        context = {"sheet_page": sheet["sheet_number"]}

        print(f"Preparing PDF sheet number {sheet['sheet_number']}.")
        # get number of cards per page
        cards_on_page = self.cards[:8]

        for i, card in enumerate(cards_on_page, start=1):
            card_front = self.render_card(card, i)
            context[f"card_{i}"] = card_front
            self.cards.remove(card)

        print(f"Rendering sheet number {sheet['sheet_number']}.")
        rendered_page = self.page_template.render(context)
        print(f"Sheet number {sheet['sheet_number']} rendering complete.")

        return rendered_page

    def generate_svgs(self):
        print("Generating SVGs.")
        for i, sheet in enumerate(self.sheets, start=1):
            svg_file = path.join(self.work_dir, f"{sheet['sheet_number']:04}R.svg")
            with open(svg_file, "wb") as f:
                # render front page
                f.write(self.render_page(sheet).encode("utf-8"))
            self.svg_files.append(svg_file)
