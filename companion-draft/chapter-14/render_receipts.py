"""Render original fictional teaching receipts. No captured document or model output.
Run: uv run --offline --with pillow python companion-draft/chapter-14/render_receipts.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
out = Path(__file__).parent
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Courier New.ttf', 32)
small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Courier New.ttf', 24)
for obscured in (False, True):
    im = Image.new('RGB', (1100, 640), 'white')
    d = ImageDraw.Draw(im)
    d.rectangle((24, 24, 1075, 615), outline='black', width=3)
    for y,text in [(55,'FICTIONAL PRACTICE RECEIPT'),(120,'Supply kits'),(175,'Quantity: 2'),(230,'Unit price: USD 12.00'),(300,'Delivery: USD 3.00'),(375,'Total: USD 27.00')]:
        d.text((65,y), text, font=font, fill='black')
    if obscured:
        # Cover the complete delivery value; no hidden text layer is emitted.
        d.rectangle((255,295,440,340),fill='black')
    d.text((65,455),'No additional tax or charges.',font=small,fill='black')
    d.text((65,505),'Designed example; not a purchase record.',font=small,fill='black')
    d.text((65,550),'One field deliberately covered.' if obscured else 'All fields deliberately legible.',font=small,fill='black')
    im.save(out/('receipt-obscured.png' if obscured else 'receipt-clear.png'))
