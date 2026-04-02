import os
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.storage.jsonstore import JsonStore

from plyer import camera, filechooser
from plyer import toast


KV = '''
<MainLayout>:
    orientation: "vertical"
    padding: 20
    spacing: 20

    Label:
        text: "Selected Folder:"
        size_hint_y: None
        height: 40

    Label:
        text: root.folder_path
        text_size: self.width, None
        halign: "center"

    Button:
        text: "Select Folder"
        size_hint_y: None
        height: 60
        on_release: root.select_folder()

    Button:
        text: "Take Photo"
        size_hint_y: None
        height: 60
        on_release: root.take_photo()
'''


class MainLayout(BoxLayout):

    folder_path = StringProperty("No folder selected")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.store = JsonStore("settings.json")

        if self.store.exists("folder"):
            self.folder_path = self.store.get("folder")["path"]

    def select_folder(self):

        def selected(selection):
            if selection:
                self.folder_path = selection[0]
                self.store.put("folder", path=self.folder_path)
                toast("Folder selected")

        filechooser.choose_dir(on_selection=selected)

    def take_photo(self):

        if self.folder_path == "No folder selected":
            toast("Please select a folder first")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = os.path.join(self.folder_path, f"photo_{timestamp}.jpg")

        camera.take_picture(
            filename=filename,
            on_complete=lambda x: toast("Photo saved!")
        )


class CameraFolderApp(App):

    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    CameraFolderApp().run()
