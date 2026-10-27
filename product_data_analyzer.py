
#Note: I am using standard commas. If the Excel is set to German this file 
#might look a bit cooked because German Excel expects semicolons
#(found out the hard way:D)



import csv
print("INDUSTRIAL PRODUCT DATA ANALYSER AHHHHHHHHHHHHH")



with open("industrial_products.csv", "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file, delimiter=";")
    products = list(reader)


print(f"\nloaded {len(products)} products!")
print("Product Catalogue:")


for product in products:
    print(
        f'{product["Product ID"]} | '
        f'{product["Product Name"]} | '
        f'{product["Category"]}'
    )

print("\nDataset loaded bebe")

#QUALITY AHHHHHHHHHHHH

print("\nDATA QUALITY CHECK: ")

products_with_missing_data = []

for product in products:
    missing_fields = []

    
    for column in product:
        if product[column].strip() == "":
            missing_fields.append(column)

    if missing_fields:
        products_with_missing_data.append(product["Product ID"])
        print(
            f'CHECK: {product["Product ID"]} '
            f'has missingg info in: {", ".join(missing_fields)}'
        )

if not products_with_missing_data:
    print("\nyey!! No missingg info")

print(
    f"\nProducts need checking: "
    f"{len(products_with_missing_data)}"
)


#DOUBLE IDENTITY AHHHHHHHHH

print("DUPLICATE PRODUCT ID CHECK: ")

seen_ids = set()
duplicate_ids = set()

for product in products:
    product_id = product["Product ID"].strip()
    if product_id in seen_ids:
        duplicate_ids.add(product_id)
    else:
        seen_ids.add(product_id)

if duplicate_ids:
    print("DOUBLE IDENTITY SITUTION!")
    for product_id in sorted(duplicate_ids):
        print(f"THE SUSPECT: {product_id}")
else:
    print("no dups yay!")

print(f"Num of dup IDs: {len(duplicate_ids)}")

#INVALIDATION SITUATION 

print("INVALIDATION CHECKER")
products_with_invalid_values = []

for product in products:
    issues = []
    try:
        price = float(product["Price"])
        stock = int(product["Stock"])
#cuz stock cant be a float dahhhh
        if price <= 0:
            issues.append("price has to be larger then zeroo")
        if stock < 0:
            issues.append("stalk cannot be negative")
    except ValueError:
        issues.append("this has to be a number")

    if issues:
        products_with_invalid_values.append(product["Product ID"])
        print(
            f'CHECK: {product["Product ID"]} - '
            f'{"; ".join(issues)}'
        )

if not products_with_invalid_values:
    print("no inval yay!")

print(
    f"Products with invalid values: "
    f"{len(products_with_invalid_values)}"
)

#SAMMY TAMMAMI OFCC
print("SAMMI TAMMAMI AKA OVERALL DATA QUALITY SUMMARY")
total_products = len(products)

# Countt
duplicate_product_count = sum(
    1 for product in products
    if product["Product ID"].strip() in duplicate_ids
)

products_needing_review = (
    set(products_with_missing_data)
    | set(duplicate_ids)
    | set(products_with_invalid_values)
)

review_count = len(products_needing_review)
complete_count = total_products - review_count

if total_products > 0:
    quality_percentage = (complete_count / total_products) * 100
else:
    quality_percentage = 0

print(f"Tot product records: {total_products}")
print(f"Needing checking: {review_count}")
print(f"no issues: {complete_count}")
print(f"percentage of ones that passt: {quality_percentage:.1f}%")

if review_count == 0:
    print("\nSTATUS: ALL PASSED THROW A PARTY NOW!")
else:
    print("\nSTATUS: Hmmmmm maybe chcek them again")
    
    
#NOW EXPORTING REPORTS
#GENRAL STUFF::::
report_data = [
    ["Metric", "Value"],
    ["Total product records", total_products],
    ["Records needing review", review_count],
    ["Records without issues", complete_count],
    ["Records passing checks (%)", round(quality_percentage, 1)],
    ["Records with missing info", len(products_with_missing_data)],
    ["Duplicate product IDs", len(duplicate_ids)],
    ["Products with invalid values", len(products_with_invalid_values)]
]

with open(
    "data_quality_report.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as report_file:
    writer = csv.writer(report_file)
    writer.writerows(report_data)

print("\nData quality report exported yayy!")
print("File made: data_quality_report.csv")

    
    
#BAD STUFFF:::::
print("PRODUCT ISSUE REPORT")

issue_report = []

for product in products:
    product_id = product["Product ID"].strip()
    product_name = product["Product Name"].strip()
    issues = []

#check for missing info
    for column, value in product.items():
        if value is None or value.strip() == "":
            issues.append(f"Missing value: {column}")

#check for dup IDs
    if product_id in duplicate_ids:
        issues.append("Duplicate product ID")

#validate for price
    price_text = product["Price"].strip()

    if price_text:
        try:
            price = float(price_text)

            if price <= 0:
                issues.append("Price must be greater than zeroo")

        except ValueError:
            issues.append("Price must be a number")

#validate for stock
    stock_text = product["Stock"].strip()

    if stock_text:
        try:
            stock = int(stock_text)

            if stock < 0:
                issues.append("Stock cannot be negative")

        except ValueError:
            issues.append("Stock must be a whole number")

#add products with issues to report
    if issues:
        issue_report.append([
            product_id,
            product_name,
            "; ".join(issues)
        ])

        print(f"REVIEW: {product_id} - {'; '.join(issues)}")

#EXPORTINGGGGGG
with open(
    "product_issue_report.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as issue_file:
    writer = csv.writer(issue_file)

    writer.writerow([
        "Product ID",
        "Product Name",
        "Issues Found"
    ])

    writer.writerows(issue_report)

print("\nproduct issue report exported yayyy!")
print(f"Products listed for checking: {len(issue_report)}")
print("File created: product_issue_report.csv")












