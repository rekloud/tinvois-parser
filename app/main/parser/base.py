from abc import ABCMeta, abstractmethod
from pandas import DataFrame
from .ocr import ocr_image
from .utils import read_config
from ..utils import get_logger

logger = get_logger(__file__)


class BaseReceipt(metaclass=ABCMeta):
    def __init__(self, image_content, cutoff=.8):
        self.cutoff = cutoff
        self.config = read_config()
        self.image_content = image_content
        self.df_ocr_raw = ocr_image(image_content)
        self.number_of_netto_values = 4
        self.netto_amount = 0

    @abstractmethod
    def preprocess(self):
        self.df_ocr: DataFrame = DataFrame()
        self.rotation: int = 0
        self.df_values: DataFrame = DataFrame()
        self.df_values['text2']: DataFrame = DataFrame()
        self.line_height: int = 0
        raise NotImplementedError()

    @abstractmethod
    def fit(self):
        raise NotImplementedError()

    @abstractmethod
    def parse_all(self) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def get_date(self):
        raise NotImplementedError()

    @abstractmethod
    def get_merchant(self):
        raise NotImplementedError()

    @abstractmethod
    def get_sum(self):
        raise NotImplementedError()

    @abstractmethod
    def get_netto(self):
        raise NotImplementedError()

    @abstractmethod
    def get_brutto(self):
        raise NotImplementedError()

    @abstractmethod
    def get_image_hash(self):
        raise NotImplementedError()
