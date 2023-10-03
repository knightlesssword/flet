import flet as ft
import random as r
from flet import TextField
from flet_core.control_event import ControlEvent


def main(page: ft.Page):
    page.title = "Simple Counter"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER   
    page.theme_mode = 'dark'
    
    def close_dlg(e: ControlEvent):
        alert_msg.open = False
        page.update()
    
    alert_msg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Sorry, unable to count!"), 
        content=ft.Text("Only digits (0-9) are allowed for counting."),
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
        actions=[
            ft.TextButton("OK", on_click=close_dlg)
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,)
    
    field_number = TextField(value='0', text_align=ft.TextAlign.CENTER, width=150)
    
    def random_number(e: ControlEvent):
        if e.name == 'click':
            field_number.value = r.randint(-10000, 10000)
            page.update()
    
    def decrement(e: ControlEvent):
       
        if e.name == 'click':
            if field_number.value == '':
                field_number.value = 0
                
            if type(field_number.value) == int or field_number.value.isdigit() or (field_number.value[0] == '-' and field_number.value[1:].isdigit()):
                field_number.value = str(int(field_number.value) - 1)
                page.update()
        
            else:
                page.show_dialog(alert_msg)
                field_number.value = 0
                page.update()
            
    def increment(e: ControlEvent):
        
        if e.name == 'click': 
            if field_number.value == '':
                field_number.value = 0
                
            if type(field_number.value) == int or field_number.value.isdigit() or (field_number.value[0] == '-' and field_number.value[1:].isdigit()):                
                field_number.value = str(int(field_number.value) + 1)
                page.update()
        
            else:
                page.show_dialog(alert_msg)
                field_number.value = 0     
                page.update()       
            
    def clear_field(e: ControlEvent):
        
        if e.name == 'click':
            field_number.value = ''
            page.update()
            field_number.value = 0
            
    page.add(
        ft.Row(
            [
                ft.Text("Simple Counter", color=ft.colors.LIGHT_GREEN_200, size=25),
            ],
            alignment= ft.MainAxisAlignment.SPACE_EVENLY
        ),
        
        ft.Row(
        ),
        
        ft.Row(
        ),
        
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=decrement, icon_color=ft.colors.AMBER, icon_size=20),
                field_number,
                ft.IconButton(ft.icons.ADD, on_click=increment, icon_color=ft.colors.AMBER, icon_size=20),
            ],
            alignment= ft.MainAxisAlignment.CENTER
        ),
        
        ft.Row(
            [
                ft.IconButton(ft.icons.CLEAR, on_click=clear_field, icon_color=ft.colors.RED, icon_size=20),
                ft.IconButton(ft.icons.NUMBERS, on_click=random_number, icon_color=ft.colors.YELLOW, icon_size=20, tooltip="A random number is generated for you between -10000 and 10000!")
            ],
            alignment= ft.MainAxisAlignment.CENTER,
        ),
        
        ft.Row(
        ),
        
        ft.Row(
        ),
        
        ft.Row(
        ),
        
        ft.Row(
        ),
        
        ft.Row(
            [   
                ft.Text("Made with"),
                ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.RED, size=13),
                ft.Text("in Flet by Abu Bakr.")
            ],
            alignment= ft.MainAxisAlignment.CENTER,
        ),
    )
    
    
if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER)