import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Product:
    price: int
    description: str
    _id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class SaleLineItem:
    product: Product
    quantity: int

    @property
    def total_price(self) -> int:
        return self.quantity * self.product.price


@dataclass
class Sale:
    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())

    @property
    def total_price(self) -> int:
        return sum(line.total_price for line in self.items)

    def add_line_item(self, product: Product, quantity: int) -> None:
        self.items.append(SaleLineItem(product, quantity))


def main() -> None:
    milk = Product(price=5_00, description="Milk")
    coffee = Product(price=10_00, description="Coffee")

    row1 = SaleLineItem(milk, quantity=2)
    print(f"Price of line 1: ${row1.total_price / 100:.2f}")

    row2 = SaleLineItem(coffee, quantity=3)
    print(f"Price of line 2: ${row2.total_price / 100:.2f}")

    sale = Sale()
    sale.add_line_item(product=milk, quantity=2)
    sale.add_line_item(product=coffee, quantity=3)

    print(f"Total price of sale: ${sale.total_price / 100:.2f}")


if __name__ == "__main__":
    main()
