# project_9
E-commerce System

- Customer class
    - name
    - id

- Product class
    - product name
    - product id
    - price
    - inventory

- Shopping cart class
    - List of shopping cart items with quantities
    - Calculates total price

- Shopping cart items class
    - Product called from product class
    - Quantity

- Orders class
    - Order id
    - Customer called from customer class
    - Calls shopping cart from shopping cart class

- Payment class
    - Calls order
    - Processes payment

- main class
    - Add product
    - New Customer
    - View products
    - Place order
    - Checkout
    - View orders
    - Exit