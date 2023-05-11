import json

import qrcode.constants
from qrcode import QRCode
from pathlib import Path

from config import config
import logging


class ProductQr:
    SCHEME = "https"
    NETLOC = "promo"
    DATA_SAVED = Path.cwd() / "qrs"
    tracking = ""

    def __init__(self, product, country):
        self.product = product
        self.country = country

    def __str__(self):
        return self.product

    def _get_product(self):
        return f"{self.SCHEME}://{self.NETLOC}.{self.product}.com"


    def get_products(self, filename):
        list_urls = []
        with open(filename, "r") as f:
            urls = json.load(f)
        for url in urls:
            list_urls.append(f"{self.SCHEME}://{self.NETLOC}.{url}.com")
        return list_urls


    def generate_qr_image(self):
        product_to_handle = self._get_product()
        qr = QRCode(
            version=config.VERSION,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=config.BOX_SIZE,
            border=config.BORDER
        )
        qr.add_data(product_to_handle)
        qr.make(fit=True)
        img = qr.make_image(fill_color=config.DEFAULT_FILL_COLOR, back_color=config.DEFAULT_BG_COLOR)
        return img
    

    def save_image_to(self):
        img = self.generate_qr_image()
        folder = self.DATA_SAVED / self.country
        folder.mkdir(parents=True, exist_ok=True)
        img.save(f"{folder}/{self.product}.png")


if __name__ == "__main__":
    c = ProductQr("playweez-gn", "GN")
    c.generate_qr_image()
    c.save_image_to()

