import base64
from .edge_detector_service import get_edges
from .bird_view_service import get_bird_view
from ..parser import Receipt
from ..utils.log import get_logger

logger = get_logger(__file__)


def parse_image(image: str, output_edited_image: bool, try_auto_edit: bool) -> (dict, int):
    image_content = base64.b64decode(image)
    parsed_orig = Receipt(image_content=image_content).parse_all()
    bird_view_image = auto_bird_view(image_content)
    if not validate_parsed_results(parsed_orig) and try_auto_edit:
        try:
            parsed_bird_view = Receipt(image_content=bird_view_image).parse_all()
            data = merge_parse_results(parsed_orig, parsed_bird_view)
        except Exception as e:
            logger.info(f'failed for auto bird view image {e}')
            data = parsed_orig
    else:
        data = parsed_orig
    if output_edited_image:
        return dict(data=data, image=base64.b64encode(bird_view_image).decode()), 200
    return dict(data=data), 200


def auto_bird_view(image_content: bytes):
    edges = get_edges(image_content)
    bird_view_image = get_bird_view(image_content, edges)
    return bytes(bird_view_image)


def validate_parsed_results(pared_result: dict) -> bool:
    if pared_result['amount'] is None:
        return False
    if pared_result['amountexvat'] is None:
        return False
    if pared_result['date'] is None:
        return False


def merge_parse_results(res1: dict, res2: dict) -> dict:
    update_dict = dict(
        amount=res1['amount'] or res2['amount'],
        amountexvat=res1['amountexvat'] or res2['amountexvat'],
        date=res1['date'] or res2['date'],
        merchant_name=res1['merchant_name'] or res2['merchant_name'],
    )
    res1.update(update_dict)
    return res1