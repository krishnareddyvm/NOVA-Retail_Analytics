import os

SCHEMA = (
    "customers(customer_id, customer_name, age, city, state, customer_segment, registration_date); "
    "products(product_id, product_name, category, price, cost); "
    "employees(employee_id, employee_name, region); "
    "orders(order_id, customer_id, product_id, employee_id, order_date, quantity, discount, sales_amount); "
    "payments(payment_id, order_id, payment_method, payment_status)"
)


def demo_sql(question):
    q = question.lower().strip()
    mappings = [
        (("total revenue", "total sales", "revenue generated"), "SELECT ROUND(SUM(sales_amount),2) AS total_revenue FROM orders"),
        (("average order value", "average order", "avg order"), "SELECT ROUND(AVG(sales_amount),2) AS average_order_value FROM orders"),
        (("how many customers", "number of customers", "customer count"), "SELECT COUNT(*) AS customer_count FROM customers"),
        (("total orders", "number of orders", "how many orders", "order count"), "SELECT COUNT(*) AS order_count FROM orders"),
        (("top 5 products", "top five products", "best products"), "SELECT p.product_name, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.product_id, p.product_name ORDER BY revenue DESC LIMIT 5"),
        (("highest revenue product", "product has the highest revenue", "highest revenue product"), "SELECT p.product_name, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.product_id, p.product_name ORDER BY revenue DESC LIMIT 1"),
        (("sales by category", "revenue by category", "category sales"), "SELECT p.category, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.category ORDER BY revenue DESC"),
        (("monthly revenue", "revenue by month", "monthly sales", "sales by month"), "SELECT substr(order_date,1,7) AS month, ROUND(SUM(sales_amount),2) AS revenue FROM orders GROUP BY month ORDER BY month"),
        (("sales by city", "revenue by city", "city sales", "top 5 cities"), "SELECT c.city, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN customers c ON c.customer_id=o.customer_id GROUP BY c.city ORDER BY revenue DESC LIMIT 5"),
        (("highest revenue city", "city with the highest revenue", "city has the highest revenue", "best city"), "SELECT c.city, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN customers c ON c.customer_id=o.customer_id GROUP BY c.city ORDER BY revenue DESC LIMIT 1"),
        (("sales by region", "revenue by region", "region sales"), "SELECT e.region, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN employees e ON e.employee_id=o.employee_id GROUP BY e.region ORDER BY revenue DESC"),
        (("payment method", "sales by payment method", "revenue by payment method", "popular payment"), "SELECT p.payment_method, ROUND(SUM(o.sales_amount),2) AS revenue FROM payments p JOIN orders o ON o.order_id=p.order_id WHERE p.payment_status='Paid' GROUP BY p.payment_method ORDER BY revenue DESC"),
        (("average discount", "avg discount", "average discount"), "SELECT ROUND(AVG(discount)*100,2) AS average_discount_percent FROM orders"),
        (("quantity by product", "order quantity by product", "units sold by product"), "SELECT p.product_name, SUM(o.quantity) AS units_sold FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.product_id, p.product_name ORDER BY units_sold DESC LIMIT 10"),
        (("customers from pune", "customers in pune"), "SELECT customer_id, customer_name, customer_segment FROM customers WHERE LOWER(city)='pune'"),
        (("top 5 employees", "top employees", "employees by revenue"), "SELECT e.employee_name, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN employees e ON e.employee_id=o.employee_id GROUP BY e.employee_id, e.employee_name ORDER BY revenue DESC LIMIT 5"),
        (("top 5 categories", "top categories", "categories by revenue"), "SELECT p.category, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.category ORDER BY revenue DESC LIMIT 5"),
        (("sales by state", "revenue by state", "state sales"), "SELECT c.state, ROUND(SUM(o.sales_amount),2) AS revenue FROM orders o JOIN customers c ON c.customer_id=o.customer_id GROUP BY c.state ORDER BY revenue DESC"),
        (("monthly orders", "orders by month", "order trend"), "SELECT substr(order_date,1,7) AS month, COUNT(*) AS orders FROM orders GROUP BY month ORDER BY month"),
        (("units sold by category", "quantity by category", "category quantity"), "SELECT p.category, SUM(o.quantity) AS units_sold FROM orders o JOIN products p ON p.product_id=o.product_id GROUP BY p.category ORDER BY units_sold DESC"),
        (("payment status", "orders by payment status", "payment status"), "SELECT payment_status, COUNT(*) AS orders FROM payments GROUP BY payment_status ORDER BY orders DESC"),
    ]
    for keys, sql in mappings:
        if any(k in q for k in keys):
            return sql
    raise ValueError(
        "This question is not supported in demo mode. Set GEMINI_API_KEY for general NL-to-SQL generation, or try one of the sample questions."
    )


def generate_sql(question):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        return demo_sql(question)
    from google import genai
    client = genai.Client(api_key=key)
    prompt = (
        "Generate exactly one SQLite SELECT query for the user's question. "
        "Use only this schema: " + SCHEMA + ". Never modify data, never use multiple "
        "statements, and return SQL only. Question: " + question
    )
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return response.text.strip().replace("```sql", "").replace("```", "").strip()
