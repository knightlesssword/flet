import flet as ft
from flet import (UserControl, Column, Row, Tab, Tabs, TextField, FloatingActionButton, icons, Checkbox, IconButton, colors)

class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        if self.edit_name.value != '':
            self.display_task.label = self.edit_name.value
            self.display_view.visible = True
            self.edit_view.visible = False
        self.update()

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)
        
class ToDoApp(UserControl):
    def build(self):
        self.new_task = TextField(hint_text="Learn Flet ♥...", expand=True)
        self.tasks = Column()

        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="ALL"), Tab(text="ACTIVE"), Tab(text="DONE")],
        )

        return Column(
            width=600,
            controls=[
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ],
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                    ],
                ),
            ],
        )

    def add_clicked(self, e):
        if self.new_task.value != '':
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
        self.update()

    def task_status_change(self, task):
        self.update()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()

    def update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        for task in self.tasks.controls:
            task.visible = (
                status == "ALL"
                or (status == "ACTIVE" and task.completed == False)
                or (status == "DONE" and task.completed)
            )
        super().update()

    def tabs_changed(self, e):
        self.update()

    
def main(page: ft.Page):
    
    page.title = "Simple To-Do App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.update()
    
        
    app = ToDoApp()    
    
    page.add(
        ft.Row(
            [
                ft.Text("Simple To-Do App", size= 25)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    page.add(app)
    
    page.add(
        ft.Container(
            ft.Row(
                [
                    ft.Text("Made with", size= 12),
                    ft.Icon(ft.icons.FAVORITE, size=12, color=ft.colors.RED),
                    ft.Text("in Flet by Abu Bakr.", size= 12)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ),
    )


if __name__ == "__main__":
    ft.app(target=main)