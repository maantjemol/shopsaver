# Software Requirement Specification

## What is the problem?

The problem is the inconvenience faced by customers when trying to find the best prices for their groceries. Traditional methods of manually comparing prices across multiple stores are time-consuming and inefficient. ShopSaver aims to automate this process by providing a centralised platform where users can input their grocery list, and the system will determine the cheapest shop based on web scraping of grocery prices from various stores.

## Why is it important to solve the problem?

It is important to solve this problem because it saves users time and money. By finding the cheapest shop for their groceries, users can make informed purchasing decisions, save on their grocery bills, and optimize their expenses. Additionally, it enhances user experience by simplifying the shopping process, making it more convenient and efficient.

## What exactly are the data input to the system and what exactly are the data output by the system?

**Data Inputs:**

- List of grocery items entered by the user through the web interface.

**Data Outputs:**

- Total price of the user's shopping list.
- Information on the cheapest grocery store where the items can be purchased.

## What are the possible approaches/procedures to solve the problem?

1. **Web Scraping:** Utilize web scraping techniques to extract real-time price data from various grocery store websites.
2. **Database:** Implement a database to store the web scraped data
3. **Algorithmic Comparison:** Implement algorithms to compare prices and determine the cheapest store for the given grocery list. Also implement an algorithm that finds out what the user means, meaning sugar = 1kg sugar and not sugar cubes.
4. **User Interface:** Develop an intuitive user interface for users to input their grocery items and view the results.

## What are the complexities that might arise while solving the problem?

1. **Website Structure Changes:** The structure of grocery store websites may change, requiring constant monitoring and adaptation of the web scraping code.
2. **Data Accuracy:** Ensuring scraped data is accurate and up-to-date is crucial for providing reliable results to users.
3. **Categorisation**: We want to categorise different kinds of butter from different stores as butter
4. **User Experience:** Designing a user-friendly interface that is easy to navigate and understand.
5. **Legal and Ethical Considerations:** Adhering to legal and ethical guidelines related to web scraping and data usage.

## If the developed software has to interface with external software or hardware, then what should be the data interchange formats with the external systems?

If the software needs to interface with external systems, standard data interchange formats such as JSON can be used. These formats provide a structured way to exchange data between different software systems and ensure compatibility and ease of integration. The choice of format would depend on the specific requirements and compatibility with the external systems involved in the integration process.

---

### **1. System Architecture Design:**

- **Components:**
    - Web Scraper Module: Responsible for extracting data from grocery store websites.
    - Price Comparison Module: Compares prices of items from different stores.
    - User Interface Module: Handles user input and displays results.
    - Database Module: Manages data storage and retrieval using PostgreSQL.
- **Interactions:**
    - User Interface interacts with the Web Scraper and Price Comparison modules.
    - Web Scraper module interacts with grocery store websites and sends data to the Price Comparison module.
    - Price Comparison module interacts with the Database module to store and retrieve price data.
    - Database module stores price data

### **2. Detailed Design:**

- **Web Scraper Module:**
    - Utilize libraries like **`requests`** and **`BeautifulSoup`** for web scraping.
    - Implement error handling for website structure changes.
- **Price Comparison Module:**
    - Implement algorithms to compare and store prices efficiently.
    - Use Python's built-in sorting functions for sorting price data.
- **User Interface Module:**
    - Use a web framework like Flask or Django for building the user interface.
    - Implement responsive design for various devices.
    - Use AJAX for dynamic updates without page reloads.

### **3. User Interface Design:**

- **Layout and Navigation:**
    - Design a clean and intuitive layout for easy navigation.
    - Implement a simple menu structure for adding items and viewing results.
- **Visual Elements:**
    - Choose a pleasant color scheme and readable fonts.
    - Use charts or graphs for visualizing price comparisons if necessary.

### **4. Database Design:**

- **Database Schema:**
    - Define tables for items, stores, prices, and user information.
    - Establish relationships between tables (e.g., items and prices, stores and prices).
- **Access Methods:**
    - Use Python's **`psycopg2`** library to connect to PostgreSQL.
    - Implement SQL queries for efficient data retrieval based on user input.

### **5. Algorithm Design:**

- **Price Comparison Algorithm:**
    - Implement algorithms for comparing prices of similar items from different stores.
    - Use appropriate sorting algorithms for displaying results by price.

### **6. Code Architecture Design:**

- **Module Organization:**
    - Organize code into separate Python modules for each component (e.g., scraper.py, comparator.py, ui.py, database.py).
    - Follow the MVC (Model-View-Controller) pattern for separation of concerns.
- **Design Patterns:**
    - Apply design patterns like Singleton for database connections.
    - Use Factory pattern if there are multiple types of scrapers or comparators.

By following these design principles and utilizing Python for coding and PostgreSQL for database management, the ShopSaver software can be developed with a robust, efficient, and user-friendly architecture.

---

### **Database Model:**

### 1. **Stores Table:**

- **Columns:**
    - **`store_id`** (Primary Key, Integer): Unique identifier for each store.
    - **`store_name`** (String): Name of the grocery store.

### 2. **Items Table:**

- **Columns:**
    - **`item_id`** (Primary Key, Integer): Unique identifier for each item.
    - **`item_name`** (String): Name of the grocery item.
    - **`category`** (String): Category of the item (e.g., dairy, produce, etc.).

### 3. **Prices Table:**

- **Columns:**
    - **`price_id`** (Primary Key, Integer): Unique identifier for each price entry.
    - **`store_id`** (Foreign Key, Integer): References **`store_id`** in the Stores table.
    - **`item_id`** (Foreign Key, Integer): References **`item_id`** in the Items table.
    - **`price`** (Decimal): Price of the item at the specific store.
    - **`unit`** (String): Unit of measurement (e.g., kg, lb, etc.).
    - **`timestamp`** (Timestamp): Date and time when the price was recorded.
