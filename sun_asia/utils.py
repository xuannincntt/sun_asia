def get_total_from_cart(cart):
    total_quantity = 0
    total_temp = 0
    for item in cart:
        print(item)
        item_quantity = int(item['quantity'])
        item_price = int(item['price'])
        total_quantity += item_quantity if item_quantity > 0 else 0
        total_temp += item_quantity * item_price

    return total_quantity, total_temp