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
    }
}


# ============================================================
# TechNova policies
# ============================================================

POLICIES = {
    "returns": (
        "Returns are accepted within 30 days "
        "in the original packaging."
    ),

    "warranty": (
        "Electronics come with a "
        "1-year manufacturer warranty."
    ),

    "shipping": (
        "Free shipping is available for orders "
        "above Rs.999. Standard delivery takes 3-5 days."
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
        return (
            f"Order {order_id} was not found."
        )

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
    Get a TechNova policy for returns,
    warranty, or shipping.
    """

    topic = topic.lower().strip()

    if topic not in POLICIES:
        return (
            "Policy not found. Available policies are: "
            "returns, warranty, shipping."
        )

    return POLICIES[topic]