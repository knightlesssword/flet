import os
import shutil
import logging

import flet
from flet import (
    Page, TextField, FilePicker, FilePickerResultEvent, SnackBar, ElevatedButton,
    Text, ProgressBar, Column, FontWeight, colors, MainAxisAlignment, Row,
    Container, ListView
)
from flet_core import CrossAxisAlignment, TextAlign, ScrollMode, Icon, icons

# Define the mapping of file extensions to folder names
FILE_TYPE_MAPPING = {
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.xlsx', '.pptx'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'Videos': ['.mp4', '.mkv', '.avi', '.mov', '.flv'],
    'Music': ['.mp3', '.wav', '.aac', '.flac'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Scripts': ['.py', '.js', '.sh', '.bat', '.pl'],
    'Executables': ['.exe', '.msi', '.apk'],
    'Others': []  # Files that don't match any category will go here
}

# Configure logging
logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_category(file_extension):
    for category, extensions in FILE_TYPE_MAPPING.items():
        if file_extension.lower() in extensions:
            return category
    return 'Others'

def resolve_conflict(destination_folder, filename):
    name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(destination_folder, new_filename)):
        new_filename = f"{name} ({counter}){extension}"
        counter += 1
    return new_filename

def organize_files(target_directory, progress_callback=None):
    total_files = sum([len(files) for _, _, files in os.walk(target_directory)])
    if total_files == 0:
        total_files = 1  # Prevent division by zero
    processed_files = 0

    for item in os.listdir(target_directory):
        item_path = os.path.join(target_directory, item)

        if os.path.isdir(item_path):
            continue

        _, extension = os.path.splitext(item)
        category = get_category(extension)

        destination_folder = os.path.join(target_directory, category)
        os.makedirs(destination_folder, exist_ok=True)

        new_filename = resolve_conflict(destination_folder, item)
        destination_path = os.path.join(destination_folder, new_filename)

        try:
            shutil.move(item_path, destination_path)
            logging.info(f"Moved: {item_path} -> {destination_path}")
        except Exception as e:
            logging.error(f"Error moving {item_path} to {destination_path}: {e}")

        processed_files += 1
        if progress_callback:
            progress_callback(processed_files / total_files * 100)

def build_tree_view(folder_path, level=0):
    """Recursively builds a tree view of files and folders."""
    tree_view = []

    try:
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isdir(item_path):
                # Add folder name with indentation
                tree_view.append(
                    Row(
                        [
                            Text("  " * level + "📁 " + item, weight=FontWeight.BOLD),
                        ],
                        alignment=MainAxisAlignment.START
                    )
                )
                # Recursion for subfolders
                tree_view.extend(build_tree_view(item_path, level + 1))
            else:
                # Add file name with indentation
                tree_view.append(
                    Row(
                        [
                            Text("  " * level + "📄 " + item),
                        ],
                        alignment=MainAxisAlignment.START
                    )
                )

    except PermissionError:
        logging.warning(f"Permission denied: {folder_path}")

    return tree_view

def main(page: Page):
    page.title = "File Organizer"
    page.window.height = 600  # Increased height to accommodate tree view
    page.window.width = 800    # Increased width for better layout
    page.padding = 20

    selected_folder = TextField(label="Selected Folder", width=600, read_only=True)
    file_picker = FilePicker(on_result=lambda e: on_file_selected(e, selected_folder))
    page.overlay.append(file_picker)

    progress_bar = ProgressBar(width=700, visible=False)
    status_text = Text("", size=15)
    tree_view_container = Container(
        content=ListView(height=300, expand=1),
        width=780,   # Adjust based on your window width
        height=300,  # Fixed height for the tree view
        border_radius=5,
        padding=10,
        bgcolor=colors.BLACK
    )

    def on_file_selected(e: FilePickerResultEvent, selected_folder: TextField):
        if e.path:
            folder_path = e.path
            selected_folder.value = folder_path
            page.update()

    def select_folder(e):
        file_picker.get_directory_path()

    def start_organizing(e):
        folder = selected_folder.value.strip()
        if not folder:
            page.snack_bar = SnackBar(content=Text("Please choose a folder to organize."))
            page.snack_bar.open = True
            page.update()
            return

        if not os.path.exists(folder):
            page.snack_bar = SnackBar(content=Text("Folder does not exist."))
            page.snack_bar.open = True
            page.update()
            return

        organize_button.disabled = True
        select_button.disabled = True
        progress_bar.visible = True
        status_text.value = "Organizing..."
        progress_bar.value = 0
        page.update()

        def update_progress(progress):
            progress_bar.value = progress / 100
            status_text.value = f"Organizing... {progress:.2f}%"
            page.update()

        organize_files(folder, progress_callback=update_progress)

        # Display the tree view after organizing
        tree_view_container.content.controls.clear()
        tree_view_container.content.controls.extend(build_tree_view(folder))

        organize_button.disabled = False
        select_button.disabled = False
        progress_bar.visible = False
        status_text.value = "Organization complete!"
        page.update()


    # Create buttons
    select_button = ElevatedButton(text="Select Folder", on_click=select_folder)
    organize_button = ElevatedButton(text="Organize Files", on_click=start_organizing)

    # Arrange components in the page
    page.add(
        Column(
            [
                Text(
                    "File Organizer",
                    size=30,
                    weight=FontWeight.BOLD,
                    color=colors.ORANGE,
                    text_align=TextAlign.CENTER
                ),
                Row(
                    [
                        selected_folder,
                        select_button
                    ],
                    alignment=MainAxisAlignment.CENTER
                ),
                Row(
                    [
                        organize_button,
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=10
                ),
                progress_bar,
                status_text,
                Column(height= 300, scroll=ScrollMode.AUTO, controls=[tree_view_container])
            ],
            alignment=MainAxisAlignment.START,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10,
        ),
        Container(
            Row(
                [
                    Text("Made with", size=12),
                    Icon(icons.FAVORITE, size=12, color=colors.RED),
                    Text("in Flet by Abu Bakr.", size=12)
                ],
                alignment=MainAxisAlignment.CENTER
            )
        ),
    )

if __name__ == '__main__':
    flet.app(target=main)
