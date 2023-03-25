# mypy: ignore-errors
import sqlite3
import tkinter as tk
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from tkinter import simpledialog
from typing import Protocol

TITLE = "Products list"
DELETE_BTN_TXT = "Delete product"
ADD_BTN_TEXT = "Add product"


@dataclass(kw_only=True)
class Product:
    """Product information."""

    name: str
    price: float
    _id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __str__(self) -> str:
        return f"{self.name} (${self.price:.2f})"


class Model:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("products.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS products (name TEXT, price REAL);")

    def add_product(self, product: Product) -> None:
        self.cursor.execute("INSERT INTO products VALUES (?, ?)", (product.name, product.price))
        self.connection.commit()

    def delete_product(self, product_name: str) -> None:
        self.cursor.execute("DELETE FROM products WHERE name = ?", (product_name,))
        self.connection.commit()

    def get_products(self) -> list[tuple[str, float]]:
        products: list[tuple[str, float]] = [
            (row[0], row[1]) for row in self.cursor.execute("SELECT name, price FROM products")
        ]
        return products


class AppInterface(Protocol):
    def bind_add_product(self, callback: Callable[[tk.Event], None]) -> None:
        ...

    def bind_del_product(self, callback: Callable[[tk.Event], None]) -> None:
        ...

    def update_products_list(self) -> None:
        ...

    def mainloop(self) -> None:
        ...


class App(tk.Tk, AppInterface):
    def __init__(self, model: Model) -> None:
        super().__init__()
        self.model = model
        self.title(TITLE)
        self.geometry("500x300")
        self.create_ui()
        self.update_products_list()

    def create_ui(self) -> None:
        self.frame = tk.Frame(self, padx=10, pady=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.product_list = tk.Listbox(
            self.frame,
            height=10,
            activestyle="none",
        )
        self.product_list.pack(fill=tk.X)
        self.product_list.bind("<FocusOut>", self.on_focus_out)
        self.product_list.bind("<<ListboxSelect>>", self.on_select_product)

        self.add_product_button = tk.Button(
            self.frame,
            text=ADD_BTN_TEXT,
            width=15,
            pady=5,
            state=tk.NORMAL,
        )
        self.add_product_button.pack(side=tk.TOP, anchor=tk.NW)

        self.del_product_button = tk.Button(
            self.frame,
            text=DELETE_BTN_TXT,
            width=15,
            pady=5,
            state=tk.DISABLED,
        )
        self.del_product_button.pack(side=tk.TOP, anchor=tk.NW)

    @property
    def selected_product(self) -> str:
        return self.product_list.get(self.product_list.curselection()).split()[0]

    def on_select_product(self, event=None) -> None:
        self.del_product_button.config(state=tk.NORMAL)

    def on_focus_out(self, event=None) -> None:
        self.product_list.selection_clear(0, tk.END)
        self.del_product_button.config(state=tk.DISABLED)

    def update_products_list(self) -> None:
        self.product_list.delete(0, tk.END)
        for item in self.model.get_products():
            name, price = item[0], item[1]
            product = Product(name=name, price=price)
            self.product_list.insert(tk.END, product)
        self.del_product_button.config(state=tk.DISABLED)

    def bind_add_product(self, callback: Callable[[tk.Event], None]) -> None:
        self.add_product_button.configure(command=callback)

    def bind_del_product(self, callback: Callable[[tk.Event], None]) -> None:
        self.del_product_button.configure(command=callback)


class Controller:
    def __init__(self, model: Model, view: AppInterface) -> None:
        self.model = model
        self.view = view

        self.view.bind_add_product(self.add_product)
        self.view.bind_del_product(self.delete_product)

    def add_product(self, event=None):
        name = simpledialog.askstring(title="Add", prompt="Product name:")
        price = float(simpledialog.askstring(title="Add", prompt="Product price $:"))

        self.model.add_product(Product(name=name, price=price))
        self.view.update_products_list()

    def delete_product(self, event=None):
        self.model.delete_product(self.view.selected_product)
        self.view.update_products_list()

    def run(self) -> None:
        self.view.mainloop()


def main() -> None:
    model = Model()
    view = App(model)
    controller = Controller(model, view)
    controller.run()


if __name__ == "__main__":
    main()
