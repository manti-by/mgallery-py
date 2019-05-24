from jinja2 import Markup
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.conf import settings
from model.base import BaseModel


image_to_image = Table(
    "image_to_image",
    BaseModel.metadata,
    Column("left_id", Integer, ForeignKey("image.id"), primary_key=True),
    Column("right_id", Integer, ForeignKey("image.id"), primary_key=True),
)


class ImageModel(BaseModel):

    __tablename__ = "image"

    path = Column(String)
    name = Column(String)
    phash = Column(String)

    width = Column(Integer)
    height = Column(Integer)

    gallery_id = Column(Integer, ForeignKey("gallery.id"))
    gallery = relationship("GalleryModel", back_populates="images")

    similar = relationship(
        "ImageModel",
        secondary=image_to_image,
        primaryjoin="ImageModel.id==image_to_image.c.left_id",
        secondaryjoin="ImageModel.id==image_to_image.c.right_id",
        backref="similar_to",
        lazy="dynamic",
    )

    @property
    def similar_images(self):
        return [x.id for x in self.similar]

    @property
    def url(self):
        return Markup('<a href="/image/{}/">{}</a>'.format(self.id, self.name))

    @property
    def link(self):
        return self.path.replace(settings["gallery"], "/media/")
