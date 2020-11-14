import app.main.parser_servie.parse_image as pi
from app.main.parser_servie.utils import read_config
import io

# imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\3.jpeg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\alaki.jpg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\fileName.jpg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\fritten.jpg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\2.jpeg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\invoice1.jpeg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\3.jpeg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\rossmann.jpg'
imgae_path = r'C:\Users\shossein\Documents\personal\taxapp\sample_invoices\tank-oil.jpg'
imgae_path = r'C:\Users\shossein\OneDrive\house\hoerde Stiftkamp 18\Rechnung\hornbach-26.03.2019.jpg'
with io.open(imgae_path, 'rb') as f:
    image_content = f.read()

config = read_config()
print(imgae_path)
receipt = pi.Receipt(image_content=image_content)
sum = receipt.get_sum()
print('sum:', sum)
netto = receipt.get_netto()
print('netto:', netto)
brutto = receipt.get_brutto()
print('brutto:', brutto)
date = receipt.get_date()
print('date:', date)
merchant = receipt.get_merchant()
print('merchant:', merchant)
# df = pi.pre_process_ocr_results(df)