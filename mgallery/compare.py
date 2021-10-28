import gi

from humanize import naturalsize

from mgallery.database import get_duplicates
from mgallery.settings import GALLERY_PATH

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk, GdkPixbuf  # noqa


class DuplicatesWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Duplicated Images")
        self.set_border_width(20)


class DuplicatesBox(Gtk.Box):
    check_boxes = []

    def __init__(self, images):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.set_homogeneous(True)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(0)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        for index, image in enumerate(images):
            if ".gif" in image['name']:
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

            attrs_label = Gtk.Label(label=f"{image['path'] or 'root'} / {image['name']}"[:20])
            attrs_label.set_alignment(0.05, 0)
            grid.attach(attrs_label, index, image_box_height + 1, 1, 1)

            size = naturalsize(image["size"], gnu=True)
            attrs_label = Gtk.Label(label=f"{image['width']}x{image['height']} {size}")
            attrs_label.set_alignment(0.05, 0)
            grid.attach(attrs_label, index, image_box_height + 2, 1, 1)

            check_box = Gtk.CheckButton(label=f"delete")
            grid.attach(check_box, index, image_box_height + 3, 1, 1)
            self.check_boxes.append(check_box)

        self.add(grid)


def delete_images(button):
    print("Clicked")


async def build_image_compare_window(window: Gtk.Window):
    grouped_images = {}
    for image in await get_duplicates():
        grouped_images.setdefault(image["phash"], []).append(image)

    action_box = Gtk.VBox()
    scrolled_window = Gtk.ScrolledWindow()
    action_box.add(scrolled_window)

    buttons_grid = Gtk.Grid()
    buttons_grid.set_column_spacing(10)
    buttons_grid.set_row_spacing(10)

    delete_button = Gtk.Button(label="Delete")
    delete_button.connect("clicked", delete_images)
    buttons_grid.attach(delete_button, 0, 0, 10, 1)

    action_box.pack_start(buttons_grid, False, False, 10)

    window.add(action_box)

    images_grid = Gtk.Grid()
    images_grid.set_column_spacing(20)
    images_grid.set_row_spacing(10)
    images_grid.set_hexpand(True)

    left = top = 0
    for phash, images in grouped_images.items():
        duplicates_box = DuplicatesBox(images)
        images_grid.attach(duplicates_box, left, top, 1, 1)
        left += 1
        if (left + 1) % 4 == 0:
            left = 0
            top += 1
        if top == 10:
            break

    scrolled_window.add(images_grid)


async def run_compare(width: int = 1280, height: int = 720):
    window = DuplicatesWindow()
    window.set_default_size(width, height)
    await build_image_compare_window(window)

    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
