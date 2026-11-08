
from langchain_core.tools import tool


# ============================================================
# Mock order data
# ============================================================

ORDERS = {
    "TN1001": {
        "item": "Laptop Pro 14",
        "status": "Shipped",
        "eta": "2 days"
    },
    "TN1002": {
        "item": "Noise-cancel Earbuds",
        "status": "Processing",
        "eta": "5 days"
    },
    "TN1003": {
        "item": "Phone X",
        "status": "Delivered",
        "eta": "-"
    },
    "TN1004": {
        "item": "Smart Watch Series 5",
        "status": "Delivered",
        "eta": "-"
    },
    "TN1005": {
        "item": "Gaming Laptop G15",
        "status": "Shipped",
        "eta": "3 days"
    },
    "TN1006": {
        "item": "Wireless Keyboard",
        "status": "Processing",
        "eta": "4 days"
    },
    "TN1007": {
        "item": "Bluetooth Speaker",
        "status": "Out for Delivery",
        "eta": "Today"
    },
    "TN1008": {
        "item": "4K Smart Monitor",
        "status": "Cancelled",
        "eta": "-"
    },
    "TN1009": {
        "item": "Mechanical Gaming Mouse",
        "status": "Shipped",
        "eta": "2 days"
    },
    "TN1010": {
        "item": "Tablet Pro 11",
        "status": "Processing",
        "eta": "6 days"
    },
    "TN1011": {
        "item": "USB-C Fast Charger",
        "status": "Delivered",
        "eta": "-"
    },
    "TN1012": {
        "item": "External SSD 1TB",
        "status": "Shipped",
        "eta": "1 day"
    },
    "TN1013": {
        "item": "Wireless Headphones",
        "status": "Out for Delivery",
        "eta": "Today"
    },
    "TN1014": {
        "item": "Smart TV 55-inch",
        "status": "Processing",
        "eta": "7 days"
    },
    "TN1015": {
        "item": "Laptop Pro 16",
        "status": "Delivered",
        "eta": "-"
    },
    "TN1016": {
        "item": "Power Bank 20000mAh",
        "status": "Shipped",
        "eta": "3 days"
    },
    "TN1017": {
        "item": "Wireless Gaming Controller",
        "status": "Cancelled",
        "eta": "-"
    },
    "TN1018": {
        "item": "Digital Camera",
        "status": "Processing",
        "eta": "5 days"
    },
    "TN1019": {
        "item": "Smart Home Security Camera",
        "status": "Delivered",
        "eta": "-"
    },
    "TN1020": {
        "item": "Portable Bluetooth Speaker",
        "status": "Shipped",
        "eta": "4 days"
    }
}


# ============================================================
# TechNova policies
# ============================================================

POLICIES = {
    "returns": (
        "Returns are accepted within 30 days "
        "in the original packaging. Products must be unused "
        "and include all original accessories and invoices."
    ),

    "warranty": (
        "Electronics come with a 1-year manufacturer warranty. "
        "The warranty covers manufacturing defects but does not "
        "cover physical damage, water damage, or unauthorized repairs."
    ),

    "shipping": (
        "Free shipping is available for orders above Rs.999. "
        "Standard delivery takes 3-5 days. Express delivery "
        "is available in selected locations."
    ),

    "refunds": (
        "Refunds are initiated after the returned product passes "
        "quality inspection. Refunds are generally processed within "
        "5-7 business days to the original payment method."
    ),

    "cancellation": (
        "Orders can be cancelled before they are shipped. "
        "Once an order has been shipped, cancellation is not available. "
        "Customers can request a return after delivery."
    ),

    "payment": (
        "TechNova accepts UPI, debit cards, credit cards, "
        "net banking, and eligible cash-on-delivery orders. "
        "All online payments are processed through secure payment gateways."
    ),

    "exchange": (
        "Customers can request an exchange within 30 days of delivery. "
        "The product must be unused, in its original packaging, "
        "and accompanied by the purchase invoice. "
        "Exchange requests are subject to product availability."
    ),

    "damaged_products": (
        "Customers who receive damaged or defective products should "
        "report the issue within 48 hours of delivery. "
        "Photographs or videos of the damaged product may be requested "
        "for verification. Eligible products can be replaced or refunded."
    ),

    "late_delivery": (
        "If an order is delayed beyond the estimated delivery date, "
        "customers can contact TechNova support with their order ID. "
        "The support team will check the shipment status and provide "
        "an updated delivery estimate."
    ),

    "replacement": (
        "Replacement requests are accepted for eligible defective "
        "or damaged products. The product must pass verification. "
        "Approved replacements are dispatched subject to availability."
    )
}


# ============================================================
# Get order status
# ============================================================

@tool
def get_order_status(order_id: str) -> str:
    """
    Get the status, item name, and estimated delivery
    time for a TechNova order.
    """

    order_id = order_id.upper().strip()

    order = ORDERS.get(order_id)

    if not order:
        return f"Order {order_id} was not found."

    return (
        f"Order {order_id}: "
        f"Item: {order['item']}, "
        f"Status: {order['status']}, "
        f"ETA: {order['eta']}"
    )


# ============================================================
# Get TechNova policy
# ============================================================

@tool
def get_policy(topic: str) -> str:
    """
    Get a TechNova policy for returns, warranty, shipping,
    refunds, cancellation, payment, exchange, damaged products,
    late delivery, or replacement.
    """

    topic = topic.lower().strip()

    # Alternative names for policy topics
    topic_aliases = {
        "return": "returns",
        "return policy": "returns",
        "refund": "refunds",
        "refund policy": "refunds",
        "warranty policy": "warranty",
        "shipping policy": "shipping",
        "payment policy": "payment",
        "exchange policy": "exchange",
        "cancellation policy": "cancellation",
        "replacement policy": "replacement",
        "damaged product": "damaged_products",
        "damaged products": "damaged_products",
        "damaged product policy": "damaged_products",
        "late delivery policy": "late_delivery"
    }

    topic = topic_aliases.get(topic, topic)

    if topic not in POLICIES:
        return (
            "Policy not found. Available policies are: "
            + ", ".join(POLICIES.keys())
        )

    return POLICIES[topic]
