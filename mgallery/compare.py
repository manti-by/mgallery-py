import gi
import os
import logging

from humanize import naturalsize

from mgallery.database import get_duplicates, delete_image
from mgallery.settings import GALLERY_PATH

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GdkPixbuf  # noqa

logger = logging.getLogger(__name__)


class DuplicatesWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Duplicated Images")
        self.set_border_width(20)


class DuplicatesBox(Gtk.Box):
    files_to_delete = []

    def __init__(self, images):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.set_homogeneous(True)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(0)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        for index, image in enumerate(images):
            # TODO: temporary disable gif support
            if ".gif" in image["name"]:
                continue

            pix_buf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                f"{GALLERY_PATH}/{image['path']}/{image['name']}",
                width=150,
                height=150,
                preserve_aspect_ratio=True,
            )
            image_box = Gtk.Image.new_from_pixbuf(pix_buf)
            image_box_height = 7
            grid.attach(image_box, index, 0, 1, image_box_height)

            attrs_label = Gtk.Label(
                label=f"{image['path'] or 'root'} / {image['name']}"[:20]
            )
            attrs_label.set_alignment(0.05, 0)
            grid.attach(attrs_label, index, image_box_height + 1, 1, 1)

            size = naturalsize(image["size"], gnu=True)
            attrs_label = Gtk.Label(label=f"{image['width']}x{image['height']} {size}")
            attrs_label.set_alignment(0.05, 0)
            grid.attach(attrs_label, index, image_box_height + 2, 1, 1)

            check_box = Gtk.CheckButton(label="delete")
            check_box.connect(
                "toggled", self.on_check_toggled, image["path"], image["name"]
            )
            grid.attach(check_box, index, image_box_height + 3, 1, 1)

        self.add(grid)

    def on_check_toggled(self, check_box, path, name):
        if check_box.get_active():
            self.files_to_delete.append((path, name))


class DuplicatesGrid(Gtk.Grid):
    duplicates_boxes = []

    def __init__(self, grouped_images):
        super().__init__()

        self.set_column_spacing(20)
        self.set_row_spacing(10)
        self.set_hexpand(True)

        left = top = 0
        for phash, images in grouped_images.items():
            duplicates_box = DuplicatesBox(images)
            self.attach(duplicates_box, left, top, 1, 1)
            left += 1
            if (left + 1) % 4 == 0:
                left = 0
                top += 1
            self.duplicates_boxes.append(duplicates_box)


class DuplicatesApp(Gtk.VBox):
    def __init__(self, grouped_images):
        super().__init__()

        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.duplicates_grid = DuplicatesGrid(grouped_images)
        scrolled_window.add(self.duplicates_grid)

        buttons_grid = Gtk.Grid()
        buttons_grid.set_column_spacing(10)
        buttons_grid.set_row_spacing(10)

        delete_button = Gtk.Button(label="Delete")
        delete_button.connect("clicked", self.delete_images)
        buttons_grid.attach(delete_button, 0, 0, 10, 1)

        self.pack_start(buttons_grid, False, False, 10)

    def delete_images(self, button):
        # TODO: very strange behaviour
        for path, name in self.duplicates_grid.duplicates_boxes[0].files_to_delete:
            delete_image(path, name)
            os.remove(f"{GALLERY_PATH}/{path}/{name}")
            logger.info(f"{GALLERY_PATH}/{path}/{name} is deleted")


def build_image_compare_window(window: Gtk.Window):
    grouped_images = {}
    for image in get_duplicates():
        grouped_images.setdefault(image["phash"], []).append(image)

    duplicates_app = DuplicatesApp(grouped_images)
    window.add(duplicates_app)


async def run_compare(width: int = 1280, height: int = 720):
    window = DuplicatesWindow()
    window.set_default_size(width, height)
    build_image_compare_window(window)

    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
