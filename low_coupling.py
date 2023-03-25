import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol


@dataclass(kw_only=True)
class Product:
    """Product information."""

    name: str
    price: int
    _id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class SaleLineItem:
    """One record in a sale."""

    product: Product
    quantity: int

    def total_line_price(self) -> int:
        """Returns the total of one line in the sale."""
        return self.quantity * self.product.price


class PaymentMethod(Protocol):
    """Payment method interface."""

    def net_price(self, total_price: int) -> int:
        ...


@dataclass
class Cash(PaymentMethod):
    """Payment method using cash."""

    discount_perc: float = 0.1

    def net_price(self, total_price: int) -> int:
        """Returns price with discount applied."""
        return int(total_price * (1 - self.discount_perc))


@dataclass
class CreditCard:
    """Payment method using credit card."""

    number: str
    fee_perc: float = 0.05

    def net_price(self, total_price: int) -> int:
        """Returns price with fee applied."""
        return int(total_price * (1 + self.fee_perc))


@dataclass
class Sale:
    """A sale to store all line records within it."""

    items: list[SaleLineItem] = field(default_factory=list)
    time: datetime = field(default=datetime.now())

    @property
    def total_price(self) -> int:
        """Returns the total price of the sale."""
        return sum(line.quantity * line.product.price for line in self.items)

    def add_line_item(self, product: Product, quantity: int) -> None:
        """Adds a product to the sale line."""
        self.items.append(SaleLineItem(product, quantity))

    def total_discounted_price(self, payment_method: PaymentMethod) -> int:
        """Calculates the net price of sale."""
        return payment_method.net_price(self.total_price)


def main() -> None:
    milk = Product(price=5_00, name="Milk")
    coffee = Product(price=4_50, name="Coffee")

    row1 = SaleLineItem(milk, quantity=2)
    print(f"Price of line 1: ${row1.total_line_price() / 100:.2f}")

    row2 = SaleLineItem(coffee, quantity=3)
    print(f"Price of line 2: ${row2.total_line_price() / 100:.2f}")

    sale = Sale()
    sale.add_line_item(product=milk, quantity=2)
    sale.add_line_item(product=coffee, quantity=3)

    print(f"Total price of sale: ${sale.total_price / 100:.2f}")

    cc = CreditCard("123456789")
    cash = Cash()
    print(f"Final value paid in cc: ${sale.total_discounted_price(cc) / 100:.2f}")
    print(f"Final value paid in cash: ${sale.total_discounted_price(cash) / 100:.2f}")


if __name__ == "__main__":
    main()
