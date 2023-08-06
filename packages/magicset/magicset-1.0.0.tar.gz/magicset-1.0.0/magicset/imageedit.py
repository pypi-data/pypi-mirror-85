
# _*_ coding=utf-8 _*_
__author__  = "8034.com"
__date__    = "2020-03-03"

import PIL
from PIL import Image, ImageFilter,ImageFont,ImageDraw
# pip install Pillow 是PIL的分支（原来PIL2009年已经停止更新）
# Pillow==6.2.2 

class ImageEditor(object):
    img = None
    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 24)
    # font = ImageFont.truetype('Deng.ttf',  30)
    font = None

    def open_file(self, imageFile):
        self.img = Image.open(imageFile)
        return self

    def show_image(self):
        return self.img.show()
    
    def save_file(self, newfile):
        """  newfile == 'image_sharpened.jpg' """
        self.check_image()
        self.img.save(newfile, 'JPEG' )
        return self

    def set_font(self, tff, size):
        if not tff:
            tff = 'Deng.ttf'
        self.font = ImageFont.truetype(tff,  size)
        return self

    def add_text_alpha(self, text, posi, debug=50):
        """  newfile == 'image_sharpened.jpg' """
        in_font = self.font
        in_spacing = debug
        self.check_image()
        rgba_image = self.img.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        text_size_x, text_size_y = image_draw.textsize(text, font=in_font)
        # 设置文本文字位置
        # 设置文本颜色和透明度
        # image_draw.text(posi, text, font=self.font, fill=(0, 0, 0, 255))
        image_draw.text(posi, text, font=in_font, fill='black', spacing=in_spacing )
        image_with_text = Image.alpha_composite(rgba_image, text_overlay)
        self.img = image_with_text.convert('RGB')
        return self

    def add_text2(self, text, posi, font=font):
        """  posi == (200,170)位置元组 """
        in_font = font
        self.check_image()
        # 在图片上添加文字 1
        draw = ImageDraw.Draw(self.img)
        draw.text(posi, text, (0,0,0), in_font)

        draw = ImageDraw.Draw(self.img)
        return self

    def check_image(self):
        if not self.img:
            raise Exception("请先加载原图")
        pass


    pass

if __name__=='__main__':
    imgEditor = ImageEditor()
    imgEditor.open_file("idcard.jpg")
    imgEditor.add_text_alpha("于利奎", (210,105))
    # imgEditor.show_image()
    imgEditor.save_file("idcard_1.jpg")
    pass 