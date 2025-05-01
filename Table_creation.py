import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 1. Create SQLite database and sales table
conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Drop table if it exists (for re-runs)
cursor.execute("DROP TABLE IF EXISTS sales")

# Create sales table
cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# 2. Insert sample data
sales_data = [
    ("2025-04-01", "Laptop", 3, 70000),
    ("2025-04-01", "Smartphone", 10, 25000),
    ("2025-04-02", "Headphones", 15, 2000),
    ("2025-04-02", "Smartwatch", 6, 8000),
    ("2025-04-03", "Laptop", 2, 72000),
    ("2025-04-03", "Smartphone", 5, 26000),
    ("2025-04-04", "Headphones", 8, 2200),
    ("2025-04-04", "Smartwatch", 4, 7800),
    ("2025-04-05", "Tablet", 7, 30000),
    ("2025-04-05", "Tablet", 3, 29000)
]

cursor.executemany("INSERT INTO sales (date, product, quantity, price) VALUES (?, ?, ?, ?)", sales_data)
conn.commit()

# 3. SQL Query: Summary by product
query = '''
SELECT product, 
       SUM(quantity) AS total_qty, 
       ROUND(SUM(quantity * price), 2) AS revenue 
FROM sales 
GROUP BY product
ORDER BY revenue DESC'''


df = pd.read_sql_query(query, conn)

# 4. Display result
print("Sales Summary by Product:")
print(df)

# 5. Plot bar chart
plt.figure(figsize=(8, 5))
df.plot(kind='bar', x='product', y='revenue', legend=False, color='skyblue')
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (INR)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("sales_chart.png")  # optional: save the chart
plt.show()

# 5.5 Display table-like structure using matplotlib
fig, ax = plt.subplots(figsize=(8, 2))  # Adjust height for compact view
ax.axis('off')  # Hide axes

# Create table
table = plt.table(cellText=df.values,
                  colLabels=df.columns,
                  loc='center',
                  cellLoc='center',
                  colLoc='center',
                  bbox=[0, 0, 1, 1])  # Full width

table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)  # scale width and height

plt.title("Sales Summary Table", pad=20)
plt.savefig("sales_summary_table.png")
plt.show()




#6. Top product
top_product = df.loc[df['revenue'].idxmax()]
print(f"\n Top Product: {top_product['product']} | Revenue: ₹{top_product['revenue']}")

#. Plot pie chart
df.set_index('product')['revenue'].plot.pie(autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
plt.title("Revenue Share by Product")
plt.ylabel('')
plt.tight_layout()
plt.savefig("revenue_pie_chart.png")
plt.show()



# 8. Close connection
conn.close()
