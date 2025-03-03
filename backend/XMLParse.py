import xml.etree.ElementTree as ET
import csv
import os
from math import gcd

# Function to simplify fractions
def simplify_fraction(numerator, denominator):
    common_divisor = gcd(numerator, denominator)
    simplified_numerator = numerator // common_divisor
    simplified_denominator = denominator // common_divisor
    return f"{simplified_numerator}/{simplified_denominator}" if simplified_denominator != 1 else f"{simplified_numerator}"

# Function to convert mm to inches and round to nearest 1/16
def mm_to_inches_and_format(mm):
    if not mm:
        return "0"
    inches = float(mm) / 25.4
    inches_rounded = round(inches * 16 + 0.5)
    whole_inch = inches_rounded // 16
    fraction = inches_rounded % 16
    if fraction == 0:
        return f"{int(whole_inch)}"
    else:
        simplified_fraction = simplify_fraction(fraction, 16)
        return f"{int(whole_inch)} {simplified_fraction}" if whole_inch != 0 else f"{simplified_fraction}"

# Function to extract product details
def extract_product_details(product):
    return {
        "UniqueID": product.get("UniqueID"),
        "CabNo": product.get("CabNo"),
        "ProdName": product.get("ProdName"),
        "Width": product.get("Width"),
        "Height": product.get("Height"),
        "Depth": product.get("Depth"),
        "CabProdParts": [
            {
                "ReportName": part.get("ReportName"),
                "W": part.get("W"),
                "L": part.get("L"),
                "Comment": part.get("Comment"),
            }
            for part in product.findall(".//CabProdPart")
        ],
    }

# Function to parse XML and save it as CSV
def parse_xml_to_csv(xml_filepath, output_folder):
    with open(xml_filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find where XML starts
    xml_content = None
    for i, line in enumerate(lines):
        if line.strip().startswith("<?xml"):
            xml_content = "".join(lines[i:])
            break

    if not xml_content:
        raise ValueError("No valid XML found in the file.")

    # Parse XML
    root = ET.fromstring(xml_content)
    room_unique_id = root.get("UniqueID")

    if not room_unique_id:
        raise ValueError("Room UniqueID not found in XML.")

    products_data = [extract_product_details(product) for product in root.findall(".//Product")]

    # Generate CSV filename
    csv_filename = f"Room_{room_unique_id}_parts.csv"
    csv_filepath = os.path.join(output_folder, csv_filename)

    with open(csv_filepath, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Part Name", "Width (inches)", "Length (inches)", "Cabinet Number"])

        for product in products_data:
            for part in product["CabProdParts"]:
                width_formatted = mm_to_inches_and_format(part["W"])
                length_formatted = mm_to_inches_and_format(part["L"])
                writer.writerow([part["ReportName"], width_formatted, length_formatted, product["CabNo"]])

    return csv_filepath  # Return path of the processed CSV
