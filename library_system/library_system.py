from pcconfig import config
import pynecone as pc
from dataclasses import dataclass

@dataclass
def Book():
    id: str
    name: str
    author: str
    kdc: str
    


class State(pc.State):
    search_query: str = ""
    input_state_info: str = ""
    
    def find_book(self):
        if self.search_query == "":
            self.input_state_info = "input required"
        else:
            raise NotImplementedError


def index():
    return (
        pc.vstack(
            navbar(),
            searcharea(),
        )
    )

def navbar():
    return (
        pc.hstack(
            pc.link(
                pc.button("Home"),
                href="/",
                button=True,
            ),
            pc.link(
                pc.button("About"),
                href="/about",
                button=True,
            ),
            pc.link(
                pc.button("Contact"),
                href="/Contact",
                button=True,
            ),
            pc.spacer(),
            pc.button(
                pc.icon(tag="MoonIcon"),
                on_click=pc.toggle_color_mode,
            ),
            
            
            padding="1em", width="100%",
        )
    )

def searcharea():
    return (
        pc.vstack(
            pc.heading("Search"),
            pc.hstack(
                pc.input(placeholder="Search", on_change=State.set_search_query),
                pc.button("Search", on_click=State.find_book),
            ),
            pc.text(State.input_state_info),
        )
    )


def search():
    return pc.heading("Search")

"""def about():
    pass

def contact():
    pass

def bookinfo():
    pass"""

app = pc.App(state=State)
app.add_page(index)
app.add_page(search)
"""app.add_page(about)
app.add_page(contact)
app.add_page(bookinfo)"""
app.compile()