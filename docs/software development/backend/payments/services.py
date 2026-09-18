"""
Payment gateway integration point.

No real payment provider was specified for this project, so this module
gives you a single place to plug one in (e.g. PayFast, Yoco, Paystack, or
Stripe are all common choices in South Africa) without touching views or
models. MockGateway lets the rest of the app be built and tested end-to-end
before a real merchant account exists - swap PAYMENT_GATEWAY below once you
have one.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass

from django.conf import settings


class PaymentGatewayUnavailable(Exception):
    pass

@dataclass
class ChargeResult:
    success: bool
    provider_reference: str
    message: str = ""


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, *, amount, method, order_id: int) -> ChargeResult:
        ...


class MockGateway(PaymentGateway):
    """Development-only stand-in. Never use in production - it always succeeds."""

    def charge(self, *, amount, method, order_id: int) -> ChargeResult:
        return ChargeResult(success=True, provider_reference=f"MOCK-{order_id}", message="Simulated success.")


class CashOnPickupGateway(PaymentGateway):
    """No money moves electronically; the payment record just tracks that cash is owed on pickup."""

    def charge(self, *, amount, method, order_id: int) -> ChargeResult:
        return ChargeResult(success=True, provider_reference="", message="Pay in person on pickup/delivery.")


def get_gateway(method: str) -> PaymentGateway:
    if method == "cash_on_pickup":
        return CashOnPickupGateway()
    if settings.DEBUG:
        return MockGateway()
    raise PaymentGatewayUnavailable(
        "Electronic payments are disabled until a production payment gateway is configured."
    )
