# Comparison Cart

### Video Demo: [Link](<URL HERE>)

## Summary

This web application, developed as the final project for CS50x, simplifies shopping by allowing users to search and compare products from two major UK retail stores: Morrisons and Waitrose. It's built using Python and Flask as the web framework, with HTML, Jinja, CSS, and Bootstrap for the frontend. User authentication and authorization are implemented for security, and user/session data are stored in a SQL database. Product details are obtained through web scraping from Morrisons and Waitrose's websites, ensuring up-to-date information.

## Running the Application Locally

To run the web application locally, follow these steps:

1. Open your terminal window and navigate to the project directory using the 'cd' command.
2. Type 'flask run' and press Enter to start the Flask application.
3. After starting the server, a link will be displayed in the terminal. Click on the provided link to access the web application in your web browser.

## User Registration

To access the web application's full functionality, you must first complete a simple registration process. Here's how it works:

- **Registration:** Start by choosing a unique username and a secure password. Confirm your password to ensure accuracy. If any required information is missing or there's a mismatch in password confirmation, the system will prompt you with an error message, ensuring that your registration details are correct.

- **Authentication:** After successful registration, you'll gain access to the application's features. However, if you attempt to use the application without being authenticated, you will be automatically redirected to the '/login' route, where you can log in with your registered credentials.

## Searching and Comparing Products

Once you've successfully logged into the site, you can start searching for products by following these steps:

- **Navigation:** Click the 'Search' button on the navigation bar to initiate the product search.

- **Product Search:** On the '/search' page, enter the name of the product you want to find. The web application will simultaneously perform web scraping on both Morrisons and Waitrose websites to gather relevant product information.

- **Search Results:** The top ten relevant products from both retailers will be displayed on the same page in a clear table format. Each product entry includes detailed information and hoverable images, making it easy for you to evaluate your options.

- **Adding to Your Cart:** You can add any of these products to your own shopping cart. When you successfully add a product, you'll receive a confirmation message highlighted in lime color and bold text directly above the tables.

- **Error Handling:** In case of invalid inputs or issues with adding products to your cart, the system will trigger error messages.


## Managing Your Carts

Once you've added the products you wish to compare, simply click the "Your Carts" button to access the "/carts" page. Here, you can perform the following actions:

- **View Cart Contents:** On the "/carts" page, you'll find a list of the items you've previously added to your carts. While the details are presented with a concise summary, you'll also see each cart's total value for your convenience.

- **Remove Items:** If you decide to remove specific items from your carts, you have the flexibility to do so. Simply click on the items you wish to remove, and they'll be taken out of your cart one by one.

- **Empty Your Cart:** Alternatively, you can choose to empty your entire cart in one go. This is a quick way to start fresh or make changes to your selections.

- **Error Handling:** Please note that the system is designed to handle potential errors. If you attempt to input non-integer values or quantities exceeding the available stock, the system will promptly alert you with error messages.

## Technologies Used

This Flask-based Grocery Shopping App utilizes the following technologies and libraries:

- **Flask Framework:** The core web framework used for building the application, handling routing, and rendering templates.

- **Flask-Session:** A Flask extension for managing session data, which is configured to use the filesystem for storing session information.

- **SQLite Database:** The application uses SQLite for database management, allowing for data storage and retrieval. This is facilitated through the CS50 Library.

- **Werkzeug Security:** The Werkzeug library is used for security-related tasks, including password hashing (via generate_password_hash) and password verification (via check_password_hash).

- **Jinja2 Templating:** HTML templates are used for rendering web pages and presenting data to users. Jinja2, a template engine, is used to integrate dynamic content into the HTML templates.

- **Bootstrap Framework:** Bootstrap is used to enhance the application's user interface with pre-designed and responsive components.

- **HTML and CSS:** These front-end technologies are employed for styling the web pages and enhancing user interactions.

- **Python Modules:**

    * functools: Used for functional programming tools, particularly the wraps decorator for preserving function metadata.
    * bs4 (Beautiful Soup): A Python library for web scraping and parsing HTML and XML documents.
    * requests: Used for making HTTP requests to external websites and fetching data for grocery item searches.

These technologies work together to provide the features and functionality of the Grocery Shopping App, including user authentication, shopping cart management, and grocery item searching.

## Image Credit

The image used in the error prompt is sourced from [memegen.link](https://memegen.link/). It features Dwight Schrute (Rainn Wilson) from The Office (US). While it's already immensely popular, I still want to acknowledge the source and express my appreciation.