"""
Order Processor Application - Simulates real-time order processing flow.
Demonstrates function parameters, return values, decorators, and scope.
"""

from functools import wraps
import time
import sys
sys.stdout.reconfigure(encoding='utf-8')

# GLOBAL CONFIGURATION
TAX_RATE = 0.18  # Global scope


# STEP 1: CART OPERATIONS - finding subtotal, applying discounts, and calculating tax


def cart_subtotal(*prices):
    """Calculate subtotal from variable number of item prices."""
    subtotal = sum(prices)
    print(f"🛒 Cart Subtotal: ₹{subtotal}")
    return subtotal


def apply_discount(price, pct=0):
    """Apply discount to given price."""
    discounted = price * (1 - pct)
    print(f"💸 After {int(pct*100)}% Discount: ₹{discounted:.2f}")
    return discounted


# Lambda — discount calculator (single expression)
# apply_discount = lambda price, pct=0: price * (1 - pct)



def add_tax(amount):
    """Add tax to final amount."""
    tax = amount * TAX_RATE
    final = amount + tax
    print(f"🧾 Tax (@{int(TAX_RATE*100)}%): ₹{tax:.2f}")
    print(f"💰 Final Amount: ₹{final:.2f}")
    return final


# STEP 2: ORDER METADATA - using flexible keyword arguments to capture order details

def create_order(**details):
    """Create an order with flexible details."""
    print("\n📄 Order Details:")
    for key, val in details.items():
        print(f"   {key}: {val}")


# STEP 3: DECORATORS

def timer(func):
    """Measure execution time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = (time.time() - start) * 1000
        print(f"\n⏱ {func.__name__} completed in {duration:.2f} ms")
        return result
    return wrapper


def log_order(func):
    """Log order processing details."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\n📦 Processing Order ID: {kwargs.get('order_id', 'N/A')}")
        result = func(*args, **kwargs)
        print(f"✅ Done! Invoice: ₹{result:.2f}")
        return result
    return wrapper


# STEP 4: ORDER PROCESSING (MAIN BUSINESS LOGIC)

@timer
@log_order
def process_order(*prices, **meta):
    """
    Complete order processing pipeline:
    Subtotal → Discount → Tax
    """
    subtotal = cart_subtotal(*prices)
    discounted = apply_discount(subtotal, meta.get("discount", 0))
    final_amount = add_tax(discounted)

    create_order(**meta)
    return final_amount


# STEP 5: EXECUTION (REAL-TIME FLOW)
process_order(
    499, 199, 999,
    order_id="ORD-007",
    user="Sateesh",
    items=3,
    discount=0.10,
    express=True
)
