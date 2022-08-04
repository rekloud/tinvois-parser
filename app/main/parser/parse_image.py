import base64
import io

import numpy as np
import pandas as pd
from PIL import Image
from flask_restx import abort
from imagehash import average_hash

from .base import BaseReceipt
from .date_parser import regex_date_parser_direct_dateutils, regex_date_parser_from_full_text
from .merchant_parser import regex_merchant_parser
from .ml_approach import (
    extract_features_token,
    classify,
    parse_vat,
    parse_netto_from_table,
    parse_netto_in_front,
    parse_netto_from_vat,
    parse_brutto_from_table,
    parse_brutto_in_front,
    parse_brutto_with_vat,
)
from .preprocessing import pre_process_ocr_results
from ..utils import get_logger

logger = get_logger(__file__)


class Receipt(BaseReceipt):
    def preprocess(self):
        self.df_ocr, self.rotation = pre_process_ocr_results(self)
        self.df_values = self.df_ocr.loc[self.df_ocr["is_numeric"], :].copy()
        if len(self.df_values) == 0:
            msg = "Image contains no amount"
            logger.warning(msg)
            abort(400, msg)
        self.df_values["text2"] = self.df_values["text2"].astype(float)

    def _get_height_of_line_in_receipt(self):
        self.line_height = np.median(self.df_ocr["3y"] - self.df_ocr["2y"])

    def fit(self) -> BaseReceipt:
        self._get_height_of_line_in_receipt()
        extract_features_token(self)
        classify(self)
        parse_vat(self)
        return self

    def parse_all(self) -> dict:
        self.preprocess()
        self.fit()
        output = dict(
            rotation=self.rotation,
            amount=self.get_sum(),
            amountexvat=self.get_netto(),
            merchant_name=self.get_merchant(),
            date=self.get_date(),
            hash=get_image_hash(self.image_content),
            raw_text=base64.b64encode(self.df_ocr_raw.to_json(orient="index").encode()).decode(),
        )
        if output["amount"] is None:
            output["amount"] = self.get_brutto()
        return output

    def get_date(self):
        date_parsers = [regex_date_parser_direct_dateutils, regex_date_parser_from_full_text]
        for date_parser in date_parsers:
            detected_date = date_parser(self)
            if detected_date is not None:
                return detected_date.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        logger.warning("could not parse date")

    def get_merchant(self):
        merchant_parsers = [regex_merchant_parser]
        for merchant_parser in merchant_parsers:
            merchant = merchant_parser(self)
            if merchant is not None:
                return merchant
        logger.warning("could not parse merchant")

    def get_sum(self):
        sum_value = self.df_values.loc[self.df_values["CLASS"] == "SUM", "text2"].max()
        if not pd.isnull(sum_value):
            self.sum = sum_value
            return int(sum_value)
        logger.warning("could not parse sum")

    def get_netto(self):
        netto_parsers = [parse_netto_from_table, parse_netto_in_front, parse_netto_from_vat]
        for netto_parser in netto_parsers:
            netto_value = netto_parser(self)
            if netto_value:
                self.netto_amount = netto_value
                return netto_value
        logger.warning("could not find netto")

    def get_brutto(self):
        brutto_parsers = [parse_brutto_from_table, parse_brutto_in_front, parse_brutto_with_vat]
        for brutto_parser in brutto_parsers:
            brutto_value = brutto_parser(self)
            if brutto_value:
                return brutto_value
        logger.warning("could not find brutto at all")


def get_image_hash(image_content):
    image_hash = average_hash(Image.open(io.BytesIO(image_content)), hash_size=16)
    return str(image_hash)
