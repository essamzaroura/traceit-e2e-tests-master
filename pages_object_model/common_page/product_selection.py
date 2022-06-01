class ProductSelection:
    """
    Represents a selected product
    """
    def __init__(self, product_id, product_name, product_category):
        self.product_category = product_category
        self.product_name = product_name
        self.product_id = product_id
