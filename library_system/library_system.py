from pcconfig import config
import pynecone as pc
import csv

class Book(pc.Model, table=True):
    book_id:str
    title:str
    author:str
    kdc:str
    publisher:str
    location:str # ex "A 04 3 45" "서가고유번호 세부서가번호 칸수(상->하) 순서(좌->우)" 


class State(pc.State):
    search_query: str = ""
    input_state_info: str = ""
    query_type: str = "title"
    search_results: list[Book] = []
    is_searching: bool = False
    show_devtools: bool = False
    pin: str = ""
    default_pin: str = "123456"
    dev_logined: bool = False
    login_failed: bool = False
    
    def init_db(filename: str):
        with open(filename) as f:
            with pc.session as session:
                for row in csv.DictReader(f):
                    book = Book(
                        bookid=row["bookid"],
                        title=row["title"],
                        author=row["author"],
                        kdc=row["kdc"],
                        publisher=row["publisher"],
                    )
                    session.add(book)
                session.commit()
    
    def search_book(self):
        with pc.session as session:
            match self.query_type:
                case "title":
                    self.search_results = session.query(Book).filter(Book.title.contains(self.search_query))
                case "author":
                    self.search_results = session.query(Book).filter(Book.author.contains(self.search_query))
                case "kdc":
                    self.search_results = session.query(Book).filter(Book.kdc == self.search_query)
                case "publisher":
                    self.search_results = session.query(Book).filter(Book.publisher.contains(self.search_query))
                case "book_id":
                    self.search_results = session.query(Book).filter(Book.book_id == self.search_query)
                    
    def devtools(self):
        self.show_devtools = not self.show_devtools
                
    def find_book(self):
        if self.search_query != "":
            self.input_state_info = ""
            self.search_book()
        else:
            self.input_state_info = "input required"
    
    def dev_login(self):
        if self.default_pin == self.pin:
            self.dev_logined = True
        else:
            self.login_failed = True
        
    def login_failed_change(self):
        self.login_failed = not self.login_failed
    
    def logout(self):
        self.dev_logined = False


def index():
    return (
        pc.vstack(
            navbar(),
            searcharea(),
            devtools(),
        )
    )

def navbar():
    return (
        pc.vstack(
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
                    pc.icon(tag="EditIcon"),
                    on_click=State.devtools,
                ),
                pc.button(
                    pc.icon(tag="MoonIcon"),
                    on_click=pc.toggle_color_mode,
                ),
                
                
                padding="1em", width="100%", padding_bottom="0.5em",
            ),
            pc.divider(),
            width="100%",
        )
    )

def searcharea():
    return (
        pc.vstack(
            pc.vstack(
                pc.heading("Search"),
                pc.hstack(
                    pc.badge(State.query_type, color_scheme="blue"),
                    pc.spacer(),
                    pc.input(placeholder="Search something!", on_change=State.set_search_query),
                    pc.button(pc.icon(tag="SearchIcon"), on_click=State.find_book, variant="solid", color_scheme="blue", size="md"),
                width="100%",
                padding="1em",
                ),
                pc.radio_group(
                    pc.vstack(
                        pc.box(
                            pc.text("Search with...", align="left"),
                            width="100%",
                        ),
                        pc.hstack(
                            pc.radio("title", is_checked=True),
                            pc.spacer(),
                            pc.radio("author"),
                            pc.spacer(),
                            pc.radio("book_id"),
                            pc.spacer(),
                            pc.radio("kdc"),
                            pc.spacer(),
                            pc.radio("publisher"),
                            width="100%",
                        ),
                    ),
                    on_change=State.set_query_type,
                    padding="1em",
                    border_radius="0.5em",
                    border="1px solid grey",
                    width="100%",
                ),
                pc.cond(
                    State.input_state_info != "",
                    pc.alert(
                        pc.alert_icon(),
                        pc.alert_title(State.input_state_info),
                        status="error",
                        variant="left-accent",
                        width="100%",
                        padding_top="1em",
                    ),
                    pc.text(""),
                ),
                width="40%",
                padding="5em",
            ),
        pc.divider(),
        width="100%",
        )
    )

def devtools():
    return (
        pc.drawer(
            pc.drawer_overlay(
                pc.drawer_content(
                    pc.drawer_header(
                        pc.heading("Dev"),
                        padding="1em",
                    ),
                    pc.drawer_body(
                        pc.cond(
                            State.dev_logined,
                            pc.hstack(
                                pc.text("logged in"),
                                pc.vstack(
                                    pc.input(_type="file"),
                                    pc.button() # todo
                                ),
                            ),
                            pc.vstack(
                                pc.text("please input pin"),
                                pc.hstack(
                                    pc.pin_input(length=6, on_change=State.set_pin, mask=True),
                                    pc.button(pc.icon(tag="UnlockIcon"), on_click=State.dev_login),
                                ),
                                pc.alert_dialog(
                                    pc.alert_dialog_overlay(
                                        pc.alert_dialog_content(
                                            pc.alert_dialog_header("Wrong PIN!"),
                                            pc.alert_dialog_body("Please input correct PIN!"),
                                            pc.alert_dialog_footer(
                                                pc.button("Close", on_click=State.login_failed_change,
                                                ),
                                            ),
                                        )
                                    ),
                                    is_open=State.login_failed
                                ),
                            ),
                        ),
                    ),
                    pc.drawer_footer(
                        pc.hstack(
                            pc.cond(
                                State.dev_logined,
                                pc.button("log out", on_click=State.logout),
                                pc.spacer(),
                            ),
                            pc.button("Close", on_click=State.devtools),
                        ),
                    ),
                ),
            ),
            is_open=State.show_devtools,
            size="md",
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