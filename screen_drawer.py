from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import io
import pymunk
import os

def image_to_byte_array(image: Image) -> bytes:
  # BytesIO is a file-like buffer stored in memory
  imgByteArr = io.BytesIO()
  # image.save expects a file-like as a argument
  image.save(imgByteArr, format="PNG")
  # Turn the BytesIO object back into a bytes object
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

FRAME_SIZE = (900, 720)

NON_UNIVERSAL_RADIUS = 30
MASK_IMG = Image.new("L", FRAME_SIZE)
MASK_ELLIPSE_IMG = Image.new("L", (2 * NON_UNIVERSAL_RADIUS, 2 * NON_UNIVERSAL_RADIUS))
draw_MASK_ELLIPSE_IMG = ImageDraw.Draw(MASK_ELLIPSE_IMG)
draw_MASK_ELLIPSE_IMG.ellipse((0, 0, 2 * NON_UNIVERSAL_RADIUS, 2 * NON_UNIVERSAL_RADIUS), fill=255)

def standard_icon(radius=30):
    img = Image.new("RGBA", (2 * radius, 2 * radius))
    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, 2 * radius, 2 * radius), fill="#5760fa")
    return img

class Player:
    name: str
    circle: pymunk.Circle
    icon: Image.Image
    def __init__(self, name, circle, icon_path):
        self.name = name
        self.circle = circle
        if os.path.exists(icon_path):
            self.icon = Image.open(icon_path).resize((2 * int(self.circle.radius), 2 * int(self.circle.radius)))
        else:
            self.icon = standard_icon(radius=int(self.circle.radius))

font = ImageFont.truetype("LTSuperior-Regular.otf", 20)

writer = None

def draw(circles: list[pymunk.Circle], segments: list[pymunk.Segment], players: list[Player], frames_drawn):
    img = Image.new("RGBA", FRAME_SIZE)
    draw = ImageDraw.Draw(img)
    draw.rectangle((0, 0, 1000, 1000), fill="#313332")

    offset_y = 0
    for player in players:
        if player.circle.body.position.y <= 11000:
            offset_y = min(offset_y, -player.circle.body.position.y + 500)

    for circle in circles:
        x1 = circle.body.position.x - circle.radius
        x2 = circle.body.position.x + circle.radius
        y1 = circle.body.position.y - circle.radius + offset_y
        y2 = circle.body.position.y + circle.radius + offset_y
        draw.ellipse((x1, y1, x2, y2), fill="white")

    for segment in segments:
        a = segment.a.rotated(segment.body.angle)
        b = segment.b.rotated(segment.body.angle)
        x1 = a.x + segment.body.position.x
        x2 = b.x + segment.body.position.x
        y1 = a.y + segment.body.position.y + offset_y
        y2 = b.y + segment.body.position.y + offset_y
        draw.line((x1, y1, x2, y2), fill="white", width=20)

    for player in players:
        x1 = player.circle.body.position.x - player.circle.radius
        x2 = player.circle.body.position.x + player.circle.radius
        y1 = player.circle.body.position.y - player.circle.radius + offset_y
        y2 = player.circle.body.position.y + player.circle.radius + offset_y
        
        img.paste(player.icon.rotate(-player.circle.body.angle * 180 / 3.14), 
                  (int(x1), int(y1)), 
                  mask=MASK_ELLIPSE_IMG)

        draw.text((x1, y1 - 30), player.name, font=font, align="left", fill="#5760fa")

    writer.send(img.convert("RGB").tobytes())

    # img.save(f"images/img_{frames_drawn}.png")
