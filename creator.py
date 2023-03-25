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


@dataclass
class Sale:
    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())

    def add_line_item(self, product: Product, quantity: int) -> None:
        self.items.append(SaleLineItem(product, quantity))


def main() -> None:
    milk = Product(price=5_00, description="Milk")
    coffee = Product(price=10_00, description="Coffee")

    sale = Sale()
    sale.add_line_item(product=milk, quantity=2)
    sale.add_line_item(product=coffee, quantity=3)

    print(sale)


if __name__ == "__main__":
    main()
