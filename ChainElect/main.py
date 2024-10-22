import os
import json
import qrcode
import dotenv
import flet as ft
from click import FileError
from collections import defaultdict
from flet_core import MainAxisAlignment, TextAlign, Alignment

from blockchain import Blockchain, cipher

dotenv.load_dotenv()

# Create a new blockchain instance
voting_chain = Blockchain()
voters = set()


def main(page: ft.Page):
    page.title = "Blockchain Voting System"
    page.window.width = 500
    page.window.height = 800
    page.window.center()
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    voter_id_input = ft.TextField(label="Voter ID", width=300, icon=ft.icons.HOW_TO_VOTE)
    candidate_input = ft.TextField(label="Candidate", width=300, icon=ft.icons.PERSON)
    blockchain_display = ft.ListView(expand=True, spacing=10, padding=10)
    vote_count_display = ft.ListView(expand=True, spacing=10, padding=10, visible=False)

    def reset_blockchain(e):
        # Create a reference to the password input field
        password_input = ft.TextField("", password=True, can_reveal_password=True, label="Admin Password")

        def check_reset(e):
            # Access the password value from the TextField reference
            if password_input.value != os.getenv('ADMIN_PASSWORD'):
                dialog_ = ft.AlertDialog(title=ft.Text("Reset Status"),
                                         content=ft.Text("Invalid Password.\nPlease try again."), open=True)
                page.overlay.append(dialog_)
                page.update()
                return

            # DANGER ZONE: Reset the blockchain
            global voting_chain, voters
            vote_count_display.controls.clear()
            voting_chain = Blockchain()
            voters = set()
            blockchain_update_display()
            dialog_ = ft.AlertDialog(title=ft.Text("Reset Status"), content=ft.Text("Blockchain reset successfully."),
                                     open=True)
            page.overlay.append(dialog_)
            page.update()

        # Create the reset dialog
        dialog = ft.AlertDialog(
            title=ft.Text("Reset Status", text_align=ft.TextAlign.CENTER),
            content=password_input,  # Use the TextField reference here
            actions=[
                ft.Container(
                    ft.ElevatedButton("Reset ElectChain", on_click=check_reset, color=ft.colors.RED),
                    expand=True,
                    alignment=ft.Alignment(0, 0)
                )
            ],
            icon=ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS),
            icon_color=ft.colors.RED,
            open=True,
        )
        page.overlay.append(dialog)
        page.update()

    def generate_qr_code(e):
        data = [block.__dict__ for block in voting_chain.chain]
        qr = qrcode.make(str(data))
        qr.save("blockchain_qr.png")
        dialog = ft.AlertDialog(
            title=ft.Text("Ledger QR", text_align=TextAlign.CENTER),
            content=ft.Image(src="blockchain_qr.png", width=200, height=200),
            icon=ft.Icon(ft.icons.QR_CODE),
            open=True
        )
        page.overlay.append(dialog)
        page.update()

    def export_blockchain(e):
        def dialog_fn(msg):
            dialog = ft.AlertDialog(
                title=ft.Text("Export ledger"),
                content=ft.Text(f"{msg}"),
                actions=[ft.ElevatedButton("OK", on_click=lambda _: page.close(dialog))],
                open=True,
                modal=True,
            )
            return dialog

        try:
            with open("blockchain.json", "w") as f:
                # noinspection PyTypeChecker
                json.dump([block.__dict__ for block in voting_chain.chain], f)
            dialog = dialog_fn("Successfully exported.")
            page.overlay.append(dialog)
        except FileError:
            dialog = dialog_fn("Export failed.")
            page.overlay.append(dialog)
        page.update()

    def view_block_details(e, block):
        block_index = ft.TextField(f"{block.index}", read_only=True, label="Index")
        data_view = ft.TextField(f"{block.data}", read_only=True, multiline=True, label="Data",
                                 on_focus=page.set_clipboard(block.data))
        hash_view = ft.TextField(f"{block.hash}", read_only=True, multiline=True, label="Hash",
                                 on_focus=page.set_clipboard(block.hash))
        dialog = ft.AlertDialog(
            title=ft.Text(f"Block Details", text_align=ft.TextAlign.CENTER),
            content=ft.Column([block_index, data_view, hash_view], width=350, height=350, spacing=30),
            open=True,
            modal=True,
            actions=[
                ft.Container(ft.ElevatedButton("OK", on_click=lambda _: page.close(dialog)),
                             alignment=ft.Alignment(0, 0))]
        )
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def blockchain_update_display():
        blockchain_display.controls.clear()
        for idx, block in enumerate(voting_chain.chain):
            chain_block = "Genesis Block" if block.index == 0 else f"Block {block.index}"
            block_button = ft.TextButton(
                f"{chain_block}",
                on_click=lambda e, blk=block: view_block_details(e, blk),
            )
            blockchain_display.controls.append(block_button)
            if idx < len(voting_chain.chain) - 1:
                arrow_icon = ft.Icon(name=ft.icons.ARROW_DOWNWARD, size=24, color=ft.colors.GREY)
                blockchain_display.controls.append(arrow_icon)
        page.update()

    def submit_vote(e):
        if voter_id_input.value in voters:
            dialog = ft.AlertDialog(
                title=ft.Text("Warning", text_align=ft.TextAlign.CENTER),
                content=ft.Text("Duplicate vote found\nVote will not be recorded", text_align=ft.TextAlign.CENTER),
                actions=[
                    ft.Container(ft.ElevatedButton("OK", on_click=lambda _: page.close(dialog), color=ft.colors.RED),
                                 alignment=ft.Alignment(0, 0))],
                alignment=Alignment(0, 0),
                open=True,
                icon=ft.Icon(ft.icons.WARNING)
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return
        elif voter_id_input.value == '' or candidate_input.value == '':
            dialog = ft.AlertDialog(
                title=ft.Text("Warning", text_align=ft.TextAlign.CENTER),
                content=ft.Text("No VoterID/Candidate found.", text_align=ft.TextAlign.CENTER),
                actions=[
                    ft.Container(ft.ElevatedButton("OK", on_click=lambda _: page.close(dialog), color=ft.colors.RED),
                                 alignment=ft.Alignment(0, 0))],
                alignment=Alignment(0, 0),
                open=True,
                icon=ft.Icon(ft.icons.WARNING)
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()
            return
        else:
            voters.add(voter_id_input.value)
            data = {"voter_id": voter_id_input.value, "candidate": candidate_input.value}
            voting_chain.add_block(data)
            blockchain_update_display()
            dialog = ft.AlertDialog(
                title=ft.Text("Voted!", text_align=ft.TextAlign.CENTER, color=ft.colors.GREEN),
                content=ft.Text("Congratulations!\nYour vote has been preserved.\nThank you for voting.",
                                text_align=ft.TextAlign.CENTER),
                actions=[ft.Container(
                    ft.IconButton(ft.icons.DONE, icon_color=ft.colors.GREEN, alignment=ft.Alignment(0, 0),
                                  on_click=lambda _: page.close(dialog)), alignment=ft.Alignment(0, 0))],
                icon=ft.Icon(ft.icons.HOW_TO_VOTE),
                open=True
            )
            update_vote_count_display()
            page.overlay.append(dialog)
        voter_id_input.value = ""
        candidate_input.value = ""
        page.update()

    def validate_chain(e):
        is_valid = voting_chain.is_chain_valid()
        msg = "Blockchain is valid!" if is_valid else "Blockchain is corrupted!"
        dialog = ft.AlertDialog(
            title=ft.Text("Validate Chain"),
            content=ft.Text(msg),
            actions=[
                ft.ElevatedButton("OK", on_click=lambda _: page.close(dialog))
            ],
            open=True,
            modal=True
        )
        page.overlay.append(dialog)
        page.update()

    # Button
    submit_button = ft.ElevatedButton("Submit Vote", on_click=submit_vote, icon=ft.icons.CHEVRON_RIGHT)
    validate_button = ft.ElevatedButton("Validate Blockchain", on_click=validate_chain, icon=ft.icons.CHECK)
    export_button = ft.ElevatedButton("Export Ledger", on_click=export_blockchain, icon=ft.icons.IMPORT_EXPORT)
    ledger_button = ft.ElevatedButton("View Ledger", on_click=lambda _: page.go("/ledger"), icon=ft.icons.NOTES)
    quit_button = ft.ElevatedButton("Exit", on_click=lambda _: page.window.close(), icon=ft.icons.EXIT_TO_APP)
    dark_mode_button = ft.IconButton(icon=ft.icons.LIGHT_MODE, on_click=lambda e: toggle_dark_mode(e),
                                     icon_color=ft.colors.YELLOW)
    qr_button = ft.IconButton(icon=ft.icons.QR_CODE, on_click=generate_qr_code, tooltip=ft.Tooltip("View ledger as QR"))
    reset_button = ft.IconButton(icon=ft.icons.LOCK_RESET, on_click=reset_blockchain, icon_color=ft.colors.RED,
                                 tooltip=ft.Tooltip("Reset ledger"))
    vote_count_display_button = ft.IconButton(icon=ft.icons.HOW_TO_VOTE_OUTLINED, on_click=lambda _: page.go("/votes"),
                                              icon_color=ft.colors.RED, tooltip=ft.Tooltip("View vote count"))

    # text containers
    title_container = ft.Container(
        ft.Text("ChainElect", style=ft.TextThemeStyle.HEADLINE_LARGE, color=ft.colors.ORANGE,
                weight=ft.FontWeight.BOLD),
        alignment=ft.Alignment(0, 0),
    )

    sub_title_container = ft.Container(
        ft.Text("Block chain based voting system.", style=ft.TextThemeStyle.TITLE_SMALL, weight=ft.FontWeight.W_100),
        alignment=ft.Alignment(0, 0),
    )

    ballot_label_container = ft.Container(
        ft.Text("Voting Ballot", text_align=ft.TextAlign.CENTER, style=ft.TextThemeStyle.BODY_SMALL,
                weight=ft.FontWeight.BOLD),
        alignment=ft.Alignment(0, 0),
    )

    bottom_bar = ft.Container(
        ft.Row([
            ft.Text("Made with"),
            ft.Icon(name=ft.icons.FAVORITE, color=ft.colors.RED, size=13),
            ft.Text("in Flet by Abu Bakr.")
        ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

    def toggle_dark_mode(e):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.bg_color = ft.colors.BLACK
            e.control.icon = ft.icons.BRIGHTNESS_5
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bg_color = ft.colors.LIGHT_BLUE
            e.control.icon = ft.icons.BRIGHTNESS_3
        page.update()

    def get_vote_count():
        vote_count = defaultdict(int)
        for block in voting_chain.chain[1:]:  # Skip genesis block
            # block.data is a hash, decrypt fernet cypher to ascii string then convert this string to dict
            data = eval(cipher.decrypt(block.data).decode('ascii'))
            # considers first name entered which matches only for count, may not be accurate
            # TODO some ID system and drop down for candidates
            vote_count[data["candidate"].strip().lower()] += 1
        return vote_count

    def update_vote_count_display():
        vote_count_display.controls.clear()
        counts = get_vote_count()
        for candidate, count in counts.items():
            vote_count_display.controls.append(
                ft.Text(f"{candidate}: {count} votes")
            )
        page.update()

    def route_change(route):
        page.views.clear()

        def verify_admin_password():
            password_input = ft.TextField(
                "", password=True, can_reveal_password=True, label="Admin Password"
            )

            def check_password(e):
                if password_input.value != os.getenv('ADMIN_PASSWORD'):
                    dialog_ = ft.AlertDialog(
                        title=ft.Text("Access Denied"),
                        content=ft.Text("Invalid Password.\nPlease try again."),
                    )
                    page.overlay.append(dialog_)
                    dialog_.open = True
                else:
                    vote_count_display.visible = True
                    dialog.open = False
                page.update()

            dialog = ft.AlertDialog(
                title=ft.Text("Admin Panel", text_align=ft.TextAlign.CENTER, color=ft.colors.RED),
                content=password_input,
                actions=[ft.ElevatedButton("Verify", on_click=check_password)],
                icon=ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS),
                icon_color=ft.colors.RED
            )
            page.overlay.append(dialog)
            dialog.open = True
            page.update()

        if page.route == "/ledger":
            page.views.append(
                ft.View(
                    "/ledger",
                    [
                        ft.AppBar(
                            title=ft.Text("ChainElect Ledger", weight=ft.FontWeight.BOLD,
                                          text_align=ft.TextAlign.CENTER, color=ft.colors.ORANGE),
                            leading=ft.IconButton(ft.icons.CHEVRON_LEFT, on_click=lambda _: page.go("/")),
                        ),
                        blockchain_display,
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            )
        elif page.route == "/votes":
            verify_admin_password()
            page.views.append(
                ft.View(
                    "/votes",
                    [
                        ft.AppBar(
                            title=ft.Text("ChainElect Vote Count", weight=ft.FontWeight.BOLD,
                                          text_align=ft.TextAlign.CENTER, color=ft.colors.ORANGE),
                            leading=ft.IconButton(ft.icons.CHEVRON_LEFT, on_click=lambda _: page.go("/")),
                        ),
                        vote_count_display,
                    ],
                    scroll=ft.ScrollMode.ADAPTIVE,
                )
            )
        else:
            vote_count_display.visible = False
            page.views.append(
                ft.View(
                    "/",
                    [
                        title_container,
                        sub_title_container,
                        ft.Text("----------", text_align=ft.TextAlign.CENTER),
                        ballot_label_container,
                        voter_id_input,
                        candidate_input,
                        submit_button,
                        ft.Text("----------", text_align=ft.TextAlign.CENTER),
                        validate_button,
                        export_button,
                        ledger_button,
                        quit_button,
                        ft.Text("----------", text_align=ft.TextAlign.CENTER),
                        bottom_bar,
                        ft.Row([vote_count_display_button, qr_button, dark_mode_button, reset_button],
                               alignment=MainAxisAlignment.CENTER)
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go(page.route)
    blockchain_update_display()


if __name__ == "__main__":
    ft.app(target=main)
