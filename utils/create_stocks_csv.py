import csv

data = [
    # Category 1: Gaming and Entertainment
    ["Electronic Arts Inc.", "EA"],
    ["Take-Two Interactive Software, Inc.", "TTWO"],
    ["Inspired Entertainment Inc.", "INSE"],
    ["Nintendo Co., Ltd.", "NTDOY"],
    ["Sony Group Corporation", "SONY"],
    ["Ubisoft Entertainment SA", "UBSFY"],
    ["Nexon Co., Ltd.", "NEXOF"],
    ["NetEase, Inc.", "NTES"],
    ["Sea Limited", "SE"],
    ["Square Enix Holdings Co., Ltd.", "SQNXF"],

    # Category 2: Technology and Software
    ["Adobe Inc.", "ADBE"],
    ["Salesforce.com Inc.", "CRM"],
    ["Oracle Corporation", "ORCL"],
    ["SAP SE", "SAP"],
    ["Intuit Inc.", "INTU"],
    ["ServiceNow, Inc.", "NOW"],
    ["Workday, Inc.", "WDAY"],
    ["Autodesk, Inc.", "ADSK"],
    ["DocuSign, Inc.", "DOCU"],
    ["Atlassian Corporation Plc", "TEAM"],

    # Category 3: E-commerce and Retail
    ["Amazon.com Inc.", "AMZN"],
    ["Alibaba Group Holding Limited", "BABA"],
    ["eBay Inc.", "EBAY"],
    ["Shopify Inc.", "SHOP"],
    ["Walmart Inc.", "WMT"],
    ["Target Corporation", "TGT"],
    ["JD.com, Inc.", "JD"],
    ["MercadoLibre, Inc.", "MELI"],
    ["Etsy, Inc.", "ETSY"],
    ["Wayfair Inc.", "W"],

    # Category 4: Communication and Social Media
    ["Facebook, Inc.", "META"],
    ["Pinterest, Inc.", "PINS"],
    ["Snap Inc.", "SNAP"],
    ["Tencent Holdings Limited", "TCEHY"],
    ["Weibo Corporation", "WB"],
    ["Alphabet Inc. Class A", "GOOGL"],
    ["Baidu, Inc.", "BIDU"],
    ["Match Group, Inc", "MTCH"],
    ["Alibaba Group Holding Limited", "BABA"],

    # Category 5: Hardware and Technology Services
    ["Apple Inc.", "AAPL"],
    ["Intel Corporation", "INTC"],
    ["NVIDIA Corporation", "NVDA"],
    ["Advanced Micro Devices, Inc.", "AMD"],
    ["Cisco Systems, Inc.", "CSCO"],
    ["Hewlett Packard Enterprise Company", "HPE"],
    ["Dell Technologies Inc.", "DELL"],
    ["Lenovo Group Limited", "LNVGY"],
    ["Seagate Technology Holdings plc", "STX"],
    ["Western Digital Corporation", "WDC"],
]

categories = {
    "Gaming and Entertainment": data[:10],
    "Technology and Software": data[10:20],
    "E-commerce and Retail": data[20:30],
    "Communication and Social Media": data[30:40],
    "Hardware and Technology Services": data[40:],
}

# Write data to CSV file
with open("stocks_list.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Category", "Company", "Ticker"])
    for category, companies in categories.items():
        for company in companies:
            writer.writerow([category] + company)
