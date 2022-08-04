import base64

from .bird_view_service import get_bird_view
from .edge_detector_service import get_edges
from ..parser import Receipt
from ..utils.log import get_logger

logger = get_logger(__file__)


def parse_image(image: str, output_edited_image: bool, try_auto_edit: bool) -> (dict, int):
    image_content = base64.b64decode(image)
    receipt_orig = Receipt(image_content=image_content)
    parsed_orig = receipt_orig.parse_all()
    if not validate_parsed_results(parsed_orig) and try_auto_edit:
        try:
            bird_view_image = auto_bird_view(image_content)
            receipt_bird_view = Receipt(image_content=bird_view_image)
            parsed_bird_view = receipt_bird_view.parse_all()
            data = merge_parse_results(
                parsed_orig, receipt_orig, parsed_bird_view, receipt_bird_view
            )
        except Exception as e:
            logger.info(f"failed for auto bird view image {e}")
            data = parsed_orig
    else:
        data = parsed_orig
    if output_edited_image:
        return dict(data=data, image=base64.b64encode(bird_view_image).decode()), 200
    return dict(data=data), 200


def auto_bird_view(image_content: bytes):
    try:
        edges = get_edges(image_content)
        bird_view_image = get_bird_view(image_content, edges)
        return bytes(bird_view_image)
    except Exception as e:
        logger.critical(f"auto bird view failed {e}")
        return bytes("failed".encode())


def validate_parsed_results(pared_result: dict) -> bool:
    # FIXME this version always returns False. Can consider more exact validation and do not
    # auto bird view in some cases
    if pared_result["amount"] is None:
        return False
    if pared_result["amountexvat"] is None:
        return False
    if pared_result["date"] is None:
        return False
    return False


def merge_parse_results(res1: dict, receipt1: Receipt, res2: dict, receipt2: Receipt) -> dict:
    update_dict = dict(
        amount=max_none(res1["amount"], res2["amount"]),
        amountexvat=max_none(res1["amountexvat"], res2["amountexvat"]),
        date=res1["date"] or res2["date"],
        merchant_name=merge_merchant(res1, receipt1, res2, receipt2),
    )
    res1.update(update_dict)
    return res1


def max_none(a, b):
    try:
        return max(a, b)
    except TypeError:
        return a or b


def merge_merchant(res1: dict, receipt1: Receipt, res2: dict, receipt2: Receipt):
    if receipt1.merchant_from_list:
        return res1["merchant_name"]
    if receipt2.merchant_from_list:
        return res2["merchant_name"]
    return res1["merchant_name"]
