# DunkDistrict

Full-Stack Basketball Sportswear E-commerce Website

DunkDistrict is a modern, feature-rich full-stack web application built with Django, designed specifically to serve basketball enthusiasts with premium sportswear and accessories. This platform offers an intuitive and dynamic shopping experience, combining sleek UI design with robust backend functionality.

Key Features:

	•	User Authentication & Profiles:
        DunkDistrict uses a custom user model (email-based authentication) with secure password handling. Registered users have personalized profiles storing details such as name, date of birth, contact info, shipping address, and accumulated total spending for loyalty tracking.

	•	Shopping Cart & Checkout Flow:
        Each user profile is linked to a dedicated shopping cart that allows adding multiple products with size and quantity selections. Users can easily update quantities, remove items, and review cart contents before checkout. The checkout process securely creates orders, calculates subtotals, taxes, shipping fees, and final totals, ensuring transparent and smooth order placement.

	•	Product Catalog & Details:
        Products feature rich metadata including multiple sizes, images, descriptions, and pricing. The front-end elegantly displays product listings and individual product pages with dynamic controls for size and quantity selection, enhancing user interaction.

	•	Order Management:
        Upon checkout, orders are stored with detailed order items capturing the product’s price at purchase to avoid discrepancies from future price changes. Orders track their status through various stages: pending, processing, delivered, or cancelled, enabling efficient order tracking for both users and admins.

	•	Role-Based Access & Admin Customization:
        Staff and admin users can manage products, orders, and users with tailored access controls. Admin panels are customized to streamline data management workflows and enhance productivity.

	•	Responsive & User-Friendly Interface:
        The UI is designed to be clean and responsive, optimized for both desktop and mobile use. Users enjoy seamless navigation across product categories, cart, profile, and checkout pages.

	•	Security & Data Integrity:
        Employing Django’s built-in security features alongside custom validations ensures data integrity and protects user information. The checkout process uses CSRF protection and secure payment placeholders to promote safe transactions.

	•	Scalable Architecture:
        With a modular Django app structure separating accounts, products, cart, and orders, DunkDistrict is designed for maintainability and future expansion, including integrations with payment gateways, inventory management, and analytics.