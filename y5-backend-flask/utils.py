import csv
import os
import uuid

import PIL
from PIL import Image
from flask import current_app

from config import TIMELINE_PRI
from models import User, PrivateMessage, Post


def rename_image(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


def resize_image(image, filename, base_width):
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    if img.size[0] <= base_width:
        return filename + ext
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)

    filename += current_app.config['PHOTO_SUFFIX'][base_width] + ext
    img.save(os.path.join(current_app.config['UPLOAD_PATH'], filename), optimize=True, quality=85)
    return filename


def import_csv(file):
    f = csv.reader(open(file, 'r', encoding='UTF-8'))
    for key, line in enumerate(f):
        if key == 0:
            pass
        username = line[1]
        room_id = line[2]
        seat_no = line[3]
        topic_no = line[4]
        message_id = line[5]

        participant = User.query.filter_by(username=username).first()
        private_message = PrivateMessage.query.filter_by(message_id=message_id).first()
        private_post = post = Post(
            timeline_type=TIMELINE_PRI,
            post_title=private_message.message_title,
            post_content=private_message.message_content,
            post_type=1,    # fixme
            user_id=participant.id,
            room_id=room_id,
            topic=topic_no,
            photo_uri=private_message.photo_uri
        )
        db.session.add(post)
        db.session.commit()
