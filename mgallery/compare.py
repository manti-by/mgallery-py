import gi
import os
import logging

from gi.repository.GLib import GError
from humanize import naturalsize

from mgallery.database import Database
from mgallery.image import create_thumbnail
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

    def __init__(self, images: list):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.set_homogeneous(True)

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(0)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        for index, image in enumerate(images):
            if ".gif" in image["name"]:
                continue

            try:
                thumbnail = create_thumbnail(image["path"], image["name"])
                pix_buf = GdkPixbuf.Pixbuf.new_from_file_at_scale(
                    thumbnail,
                    width=128,
                    height=128,
                    preserve_aspect_ratio=True,
                )
            except GError:
                logger.warning(f"Can't open an image {image['path']}/{image['name']}")
                continue
            except Exception as e:
                logger.error(e)
                continue

            image_box_height = 7

            image_box = Gtk.Image.new_from_pixbuf(pix_buf)
            image_box.set_alignment(0, 0.95)
            grid.attach(image_box, index, 0, 1, image_box_height)

            label = Gtk.Label()
            image_size = naturalsize(image["size"], gnu=True)
            label_text = f"<b>{image_size}</b> {image['width']}x{image['height']} "
            label.set_markup(f"<span size='medium'>{label_text}</span>")
            label.set_alignment(0, 0.05)
            grid.attach(label, index, image_box_height + 1, 1, 1)

            label = Gtk.Label()
            label_text = image["path"] or "root"
            label.set_markup(f"<span size='medium'><b>{label_text}</b></span>")
            label.set_alignment(0, 0.05)
            grid.attach(label, index, image_box_height + 2, 1, 1)

            label = Gtk.Label()
            label_text = image["name"][:50]
            label.set_markup(f"<span size='small'>{label_text}</span>")
            label.set_alignment(0, 0.05)
            grid.attach(label, index, image_box_height + 3, 1, 1)

            check_box = Gtk.CheckButton(label="delete")
            check_box.connect(
                "toggled", self.on_check_toggled, image["path"], image["name"]
            )
            grid.attach(check_box, index, image_box_height + 4, 1, 1)

        self.add(grid)

    def on_check_toggled(self, check_box, path, name):
        if check_box.get_active():
            self.files_to_delete.append((path, name))


class DuplicatesGrid(Gtk.Grid):
    duplicates_boxes = []

    def __init__(self, duplicates: dict):
        super().__init__()

        self.set_column_spacing(5)
        self.set_row_spacing(5)
        self.set_hexpand(True)

        left = top = 0
        for phash, images in duplicates.items():
            duplicates_box = DuplicatesBox(images)
            self.attach(duplicates_box, left, top, 1, 1)
            left += 1
            if (left + 1) % 3 == 0:
                left = 0
                top += 1
            self.duplicates_boxes.append(duplicates_box)


class DuplicatesApp(Gtk.VBox):
    def __init__(self, duplicates: dict):
        logger.info(f"Compare {len(duplicates)} images")

        super().__init__()

        scrolled_window = Gtk.ScrolledWindow()
        self.add(scrolled_window)

        self.duplicates_grid = DuplicatesGrid(duplicates)
        scrolled_window.add(self.duplicates_grid)

        buttons_grid = Gtk.Grid()
        buttons_grid.set_column_spacing(10)
        buttons_grid.set_row_spacing(10)

        delete_button = Gtk.Button(label="Delete")
        delete_button.connect("clicked", self.delete_images)
        buttons_grid.attach(delete_button, 0, 0, 10, 1)

        self.pack_start(buttons_grid, False, False, 10)

        self.database = Database()

    def delete_images(self, button: Gtk.Button):
        for path, name in self.duplicates_grid.duplicates_boxes[0].files_to_delete:
            self.database.delete(path, name)
            file_name = f"{GALLERY_PATH}/{path}/{name}"
            if os.path.exists(file_name):
                os.remove(file_name)
                logger.info(f"{file_name} is deleted")
                continue
            logger.error(f"Can't find a file {file_name}")


def build_image_compare_window(window: Gtk.Window):
    duplicates = Database().duplicates()
    duplicates_app = DuplicatesApp(duplicates)
    window.add(duplicates_app)


def run_compare(width: int = 1600, height: int = 800):
    window = DuplicatesWindow()
    window.set_default_size(width, height)
    build_image_compare_window(window)

    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
