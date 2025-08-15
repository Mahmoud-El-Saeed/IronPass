from rich.table import Table
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Static, Button, Input , OptionList
from textual.containers import Horizontal  , CenterMiddle
import pyperclip 
import re
from crypto_utils import Generate_Password


PASSWORD_PATTERN = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{9,}$'



class FirstTimeScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True,time_format="%H:%M:%S")
        yield Footer()
        with open("welcome.txt", "r") as file:
            ascii_art = file.read()
        yield Static(ascii_art, classes="ascii-logo")
        with Horizontal():
            yield Input(placeholder="Enter your Master password", id="master_password_input", password=True)
            yield Button("Show", id="toggle_master")
        with Horizontal():
            yield Input(placeholder="Confirm your Master password", id="confirm_password_input", password=True)
            yield Button("Show", id="toggle_confirm")

        yield Button("Submit", variant="success", id="Submit_button")
        yield Static("", id="message_area", classes="message")

    def on_button_pressed(self, event: Button.Pressed):
        message_widget = self.query_one("#message_area", Static)

        if event.button.id == "toggle_master":
            pw_input = self.query_one("#master_password_input", Input)
            pw_input.password = not pw_input.password
            event.button.label = "Hide" if not pw_input.password else "Show"
        elif event.button.id == "toggle_confirm":
            pw_input = self.query_one("#confirm_password_input", Input)
            pw_input.password = not pw_input.password
            event.button.label = "Hide" if not pw_input.password else "Show"

        elif event.button.id == "Submit_button":
            master_password_widget = self.query_one("#master_password_input", Input)
            master_password = master_password_widget.value
            confirm_password_widget = self.query_one("#confirm_password_input", Input)
            confirm_password = confirm_password_widget.value

            if master_password != confirm_password:
                message_widget.update("[red]Master passwords do not match![/red]")
                return

            if not re.match(PASSWORD_PATTERN, master_password):
                message_widget.update("[red]Password must be at least 9 chars, include upper, lower, digit, and special char![/red]")
                return

            message_widget.update("[green]Password accepted! Returning...[/green]")

class ReturningUserScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, time_format="%I:%M:%S")
        yield Footer()
        with open("welcome.txt", "r") as file:
            ascii_art = file.read()
        yield Static(ascii_art, classes="ascii-logo")
        with Horizontal():
            yield Input(placeholder="Enter your Master password", id="master_password_input", password=True)
            yield Button("Show", id="toggle_master")

        yield Button("Submit", variant="success", id="Submit_button")
        yield Static("", id="message_area", classes="message")

    def on_button_pressed(self, event: Button.Pressed):
        message_widget = self.query_one("#message_area", Static)

        if event.button.id == "toggle_master":
            pw_input = self.query_one("#master_password_input", Input)
            pw_input.password = not pw_input.password
            event.button.label = "Hide" if not pw_input.password else "Show"
        elif event.button.id == "Submit_button":
            master_password_widget = self.query_one("#master_password_input", Input)
            master_password = master_password_widget.value

            if not re.match(PASSWORD_PATTERN, master_password):
                message_widget.update("[red]Invalid password format![/red]")
                return

            message_widget.update("[green]Password accepted! Returning...[/green]")

class OptionsMenu(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True,time_format="%I:%M:%S")
        yield Footer()
        with open("welcome.txt", "r") as file:
            ascii_art = file.read()
        yield Static(ascii_art, classes="ascii-logo")
        with CenterMiddle(classes="options-container"):
            yield Button("Add Password", id="add_password",variant="success")
            yield Button("Show Password", id="show_password",variant="primary")
            yield Button("Delete Password", id="delete_password",variant="error")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "add_password":
            self.app.push_screen(AddPasswordScreen())
        elif event.button.id == "show_password":
            self.app.push_screen(ShowPasswordScreen())
        elif event.button.id == "delete_password":
            self.app.push_screen(DeletePasswordScreen())

class AddPasswordScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(show_clock=True,time_format="%I:%M:%S")
        yield Footer()
        with open("welcome.txt", "r") as file:
            ascii_art = file.read()
        yield Static(ascii_art, classes="ascii-logo")
        with CenterMiddle(classes="SiteName_UserName"):
            yield Input(placeholder="Enter Your Site Name")
            yield Input(placeholder="Enter Your Username")
            with Horizontal():
                yield Input(placeholder="Enter Your Password", password=True, id="master_password_input")
                yield Button("Generate", id="generate_password", variant="primary")
                yield Button("Show", id="toggle_password", variant="warning")

        yield Button("Submit", variant="success", id="Submit_button")
        yield Button("Exit", id="Exit_id")
    
    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "Exit_id":
            self.app.pop_screen()
        elif event.button.id == "toggle_password":
            pw_input = self.query_one("#master_password_input", Input)
            pw_input.password = not pw_input.password
            event.button.label = "Hide" if not pw_input.password else "Show"
        elif event.button.id == "generate_password":
            pw_input = self.query_one("#master_password_input", Input)
            pw_input.value = Generate_Password()

class ShowPasswordScreen(Screen):
    Fake_data = [
        ("google", "mahmoud", "7hn5|TJlr5ilwReT4;:H$@ErW0ZIiwU0~'l5@k"),
        ("github", "ali", "-^immzZ*2N^dtdt9F>6+K!n0RlsLq%'(o"),
        ("google", "ali", "|iq<gvszR,1cCSz\\tC$R}F7wq.c\\G02z>45XC]I"),
        ("facebook", "ali", "Fb@c00k1e!"),
        ("twitter", "ali", "Tw!tt3rP@ssw0rd"),
        ("linkedin", "ali", "LiNk3dInP@ssw0rd"),
        ("snapchat", "ali", "Sn@pCh@tP@ssw0rd")
    ]

    def __init__(self):
        super().__init__()
        self._selected_index = None
        self._show_password = False
        self._filtered_data = list(self.Fake_data) 

    @staticmethod
    def password_entry(service: str, username: str, password: str, hide=True) -> Table:
        table = Table(title=f"{service} ({username})", expand=True)
        table.add_column("Service")
        table.add_column("Username")
        table.add_column("Password")
        if hide:
            table.add_row(service, username, "*" * len(password))
        else:
            table.add_row(service, username, password)
        return table

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("🔐 Show Passwords", classes="title")
        yield Input(id="search_input", placeholder="Search...")
        self.option_list = OptionList(
            *[self.password_entry(*row) for row in self._filtered_data], id="option-list"
        )
        yield self.option_list
        with Horizontal(id="actions_bar"):
            self.btn_show = Button("Show", id="btn_show", variant="primary", disabled=True)
            self.btn_copy = Button("Copy", id="btn_copy", variant="success", disabled=True)
            yield self.btn_show
            yield self.btn_copy
            yield Button("Exit", id="Exit_id", variant="default")
        yield Footer()

    def refresh_option_list(self):
        self.option_list.clear_options()
        for i, row in enumerate(self._filtered_data):
            hide = not (self._show_password and i == self._selected_index)
            self.option_list.add_option(self.password_entry(*row, hide=hide))

    def on_input_changed(self, event: Input.Changed):
        query = event.value.strip().lower()
        if query:
            self._filtered_data = [
                row for row in self.Fake_data
                if row[0].lower().startswith(query) or row[1].lower().startswith(query)
            ]
        else:
            self._filtered_data = list(self.Fake_data)
        self._selected_index = None
        self.btn_show.disabled = True
        self.btn_copy.disabled = True
        self.refresh_option_list()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self._selected_index = event.option_index
        self.btn_show.disabled = False
        self.btn_copy.disabled = False
        if self._show_password:
            self._show_password = False
            self.btn_show.label = "Show"
            self.refresh_option_list()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "Exit_id":
            self.app.pop_screen()
        elif event.button.id == "btn_show" and self._selected_index is not None:
            self._show_password = not self._show_password
            self.btn_show.label = "Hide" if self._show_password else "Show"
            self.refresh_option_list()
        elif event.button.id == "btn_copy" and self._selected_index is not None:
            _, _, password = self._filtered_data[self._selected_index]
            pyperclip.copy(password)

class DeletePasswordScreen(Screen):
    Fake_data = [
        ("google", "mahmoud", "7hn5|TJlr5ilwReT4;:H$@ErW0ZIiwU0~'l5@k"),
        ("github", "ali", "-^immzZ*2N^dtdt9F>6+K!n0RlsLq%'(o"),
        ("google", "ali", "|iq<gvszR,1cCSz\\tC$R}F7wq.c\\G02z>45XC]I"),
        ("facebook", "ali", "Fb@c00k1e!"),
        ("twitter", "ali", "Tw!tt3rP@ssw0rd"),
        ("linkedin", "ali", "LiNk3dInP@ssw0rd"),
        ("snapchat", "ali", "Sn@pCh@tP@ssw0rd")
    ]

    def __init__(self):
        super().__init__()
        self._selected_index = None
        self._show_password = False
        self._filtered_data = list(self.Fake_data) 

    @staticmethod
    def password_entry(service: str, username: str, password: str, hide=True) -> Table:
        table = Table(title=f"{service} ({username})", expand=True)
        table.add_column("Service")
        table.add_column("Username")
        table.add_column("Password")
        if hide:
            table.add_row(service, username, "*" * len(password))
        else:
            table.add_row(service, username, password)
        return table

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("🔐 Delete Passwords", classes="title")
        yield Input(id="search_input", placeholder="Search...")
        self.option_list = OptionList(
            *[self.password_entry(*row) for row in self._filtered_data], id="option-list"
        )
        yield self.option_list
        with Horizontal(id="actions_bar"):
            self.btn_show = Button("Show", id="btn_show", variant="primary", disabled=True)
            self.delete_btn = Button("Delete", id="delete_btn", variant="error", disabled=True)
            yield self.btn_show
            yield self.delete_btn
            yield Button("Exit", id="Exit_id", variant="default")
        yield Footer()

    def refresh_option_list(self):
        self.option_list.clear_options()
        for i, row in enumerate(self._filtered_data):
            hide = not (self._show_password and i == self._selected_index)
            self.option_list.add_option(self.password_entry(*row, hide=hide))

    def on_input_changed(self, event: Input.Changed):
        query = event.value.strip().lower()
        if query:
            self._filtered_data = [
                row for row in self.Fake_data
                if row[0].lower().startswith(query) or row[1].lower().startswith(query)
            ]
        else:
            self._filtered_data = list(self.Fake_data)
        self._selected_index = None
        self.btn_show.disabled = True
        self.delete_btn.disabled = True
        self.refresh_option_list()

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        self._selected_index = event.option_index
        self.btn_show.disabled = False
        self.delete_btn.disabled = False
        if self._show_password:
            self._show_password = False
            self.btn_show.label = "Show"
            self.refresh_option_list()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "Exit_id":
            self.app.pop_screen()
        elif event.button.id == "btn_show" and self._selected_index is not None:
            self._show_password = not self._show_password
            self.btn_show.label = "Hide" if self._show_password else "Show"
            self.refresh_option_list()
        elif event.button.id == "delete_btn" and self._selected_index is not None:
            row = self._filtered_data.pop(self._selected_index)
            self.Fake_data.remove(row)
            self._selected_index = None
            self._show_password = False
            self.btn_show.label = "Show"
            self.btn_show.disabled = True
            self.delete_btn.disabled = True
            self.refresh_option_list()

class IronpassApp(App):
    CSS_PATH = "style.tcss"

    def on_mount(self) -> None:
        self.title = "Ironpass"
        self.push_screen(OptionsMenu())

if __name__ == "__main__":
    app = IronpassApp()
    app.run()
