from pcconfig import config
import pynecone as pc
import csv

class Book(pc.Model, table=True):
    bookid:str
    title:str
    author:str
    kdc:str
    publisher:str
    


class State(pc.State):
    search_query: str = ""
    input_state_info: str = ""
    query_type: str = "title"
    search_results: list[Book] = []
    
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
                case "bookid":
                    self.search_results = session.query(Book).filter(Book.bookid == self.search_query)
                
        
    
    def find_book(self):
        if self.search_query != "":
            self.search_book()
        else:
            self.input_state_info = "input required"
            


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