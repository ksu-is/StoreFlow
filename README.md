# StoreFlow
a Python-powered “coach” designed to help retail teams such as Walmart online order associates, Instacart shoppers, or campus market staff complete pick lists faster and with fewer errors.
Joined ksu-is and started working on code and structure today.

Made projectroadmap file
# StoreFlow – Interactive Retail Pick Coach

StoreFlow is a simple Python-based tool designed to help workers in **retail stores**, **gig shopping services** (like Instacart or Shipt), and **campus markets** complete customer pick lists faster and with fewer mistakes.

## Features

- Asks for **customer name** and **order ID**
- Guides the worker through a pick list one item at a time
- Displays:
  - Item name
  - SKU
  - Zone
  - Aisle
  - Location
  - Quantity needed
- Lets the worker:
  - Pick the item
  - Skip the item
  - Quit the session early
- Prevents common errors by warning about overpicking
- Tracks:
  - Total items
  - Units needed vs. units picked
  - Short/skipped items
- Shows a summary with:
  - Accuracy percentage by units
  - Simple coaching tips
- Can run multiple customers one after another

## How It Works

1. The worker runs the program:

   ```bash
   python storeflow.py
