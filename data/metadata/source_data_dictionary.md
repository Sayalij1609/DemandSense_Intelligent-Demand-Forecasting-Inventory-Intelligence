# DemandSense Source Data Dictionary

This document details every column across all 10 raw CSV datasets evaluated during Phase 1. All raw files reside in `data/raw/kaggle/` and remain strictly immutable.

---

## 1. Primary Dataset: `retail_store_inventory.csv`

- **Filename**: `retail_store_inventory.csv`
- **Business Role**: Retail Sales Demand & Inventory Panel
- **Status**: **SELECTED AS PRIMARY REAL-DATA FOUNDATION**
- **Dimensions**: 73,100 rows x 15 columns
- **Granularity**: Daily Store-Product Level (`Date` + `Store ID` + `Product ID`)
- **Timeframe**: `2022-01-01` to `2024-01-01` (731 continuous days, 100 series)

| Column Name | Data Type | Missing Count (%) | Unique Values | Description / Business Meaning | Sample Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `Date` | `string (YYYY-MM-DD)` | 0 (0.0%) | 731 | Calendar date of observation. Covers exactly 2 full calendar years. | `'2022-01-01'`, `'2022-01-02'` |
| `Store ID` | `string` | 0 (0.0%) | 5 | Physical retail store identifier (`S001` to `S005`). | `'S001'`, `'S002'`, `'S003'` |
| `Product ID` | `string` | 0 (0.0%) | 20 | Retail product SKU identifier (`P0001` to `P0020`). | `'P0001'`, `'P0002'`, `'P0003'` |
| `Category` | `string` | 0 (0.0%) | 5 | Merchandise department/category classification. | `'Groceries'`, `'Toys'`, `'Electronics'`, `'Furniture'`, `'Clothing'` |
| `Region` | `string` | 0 (0.0%) | 4 | Geographic territory where the store operates. | `'North'`, `'South'`, `'West'`, `'East'` |
| `Inventory Level` | `integer` | 0 (0.0%) | 451 | Recorded stock-on-hand snapshot. | `231`, `204`, `102`, `469` |
| `Units Sold` | `integer` | 0 (0.0%) | 498 | Actual unit sales volume (primary demand target). | `127`, `150`, `65`, `14` |
| `Units Ordered` | `integer` | 0 (0.0%) | 181 | Replenishment order quantities placed. | `55`, `66`, `51`, `164` |
| `Demand Forecast` | `float` | 0 (0.0%) | 31,608 | Existing baseline statistical forecast in raw dataset. | `135.47`, `144.04`, `74.02` |
| `Price` | `float` | 0 (0.0%) | 8,999 | Retail selling price per unit ($). | `33.50`, `63.01`, `27.99` |
| `Discount` | `integer` | 0 (0.0%) | 5 | Promotional discount percentage offered to customers. | `0`, `5`, `10`, `15`, `20` |
| `Weather Condition` | `string` | 0 (0.0%) | 4 | Local ambient weather condition on the date. | `'Rainy'`, `'Sunny'`, `'Cloudy'`, `'Snowy'` |
| `Holiday/Promotion` | `integer (0/1)` | 0 (0.0%) | 2 | Binary indicator of active holiday or promotional marketing campaign. | `0`, `1` |
| `Competitor Pricing`| `float` | 0 (0.0%) | 9,751 | Benchmark price for equivalent product at local competitor ($). | `29.69`, `66.16`, `31.32` |
| `Seasonality` | `string` | 0 (0.0%) | 4 | Seasonal calendar cycle indicator. | `'Autumn'`, `'Summer'`, `'Winter'`, `'Spring'` |

---

## 2. Incompatible Datasets Evaluated

### 2.1 `customer_shopping_data.csv`
- **Business Role**: Mall Invoices (Istanbul) | **Rows**: 99,457 | **Columns**: 10
- **Columns**: `invoice_no` (str), `customer_id` (str), `gender` (str), `age` (int), `category` (str), `quantity` (int), `price` (float), `payment_method` (str), `invoice_date` (str), `shopping_mall` (str).
- **Exclusion Reason**: Lacks SKU product IDs (only 8 broad categories); store entities are Turkish shopping malls; lacks inventory tracking.

### 2.2 `online-retail-dataset.csv`
- **Business Role**: E-Commerce Giftware Transactions (UK) | **Rows**: 541,909 | **Columns**: 8
- **Columns**: `InvoiceNo` (str), `StockCode` (str), `Description` (str), `Quantity` (int), `InvoiceDate` (str), `UnitPrice` (float), `CustomerID` (float), `Country` (str).
- **Exclusion Reason**: Timeframe (2010–2011) has zero overlap with 2022–2024; non-store transactional log; contains cancellations (negative quantities); no store dimensions.

### 2.3 `export.csv`
- **Business Role**: Wholesale Liquor Operations (Montgomery County DLC) | **Rows**: 341,037 | **Columns**: 9
- **Columns**: `YEAR` (int), `MONTH` (int), `SUPPLIER` (str), `ITEM CODE` (str), `ITEM DESCRIPTION` (str), `ITEM TYPE` (str), `RETAIL SALES` (float), `RETAIL TRANSFERS` (float), `WAREHOUSE SALES` (float).
- **Exclusion Reason**: Coarse monthly granularity across only 4 months (2020-06 to 2020-09); domain specific to government wholesale alcoholic beverage distribution.

### 2.4 `retail_sales_dataset.csv`
- **Business Role**: Demographic Order Log | **Rows**: 4,310 | **Columns**: 21
- **Columns**: `order_id`, `order_date`, `customer_id`, `customer_name`, `age`, `gender`, `region`, `city`, `product_category`, `product_name`, `quantity`, `unit_price`, `discount_pct`, `sales_amount`, `profit`, `shipping_cost`, `payment_method`, `customer_satisfaction`, `return_flag`, `order_status`, `days_to_ship`.
- **Exclusion Reason**: Extremely sparse transaction log (4,310 orders across 4 years nationally); lacks store IDs; product names are generic non-SKU items (`Sugar`, `T-shirt`).

### 2.5 `data.csv`
- **Business Role**: B2B Commercial Equipment Orders (Australia) | **Rows**: 5,000 | **Columns**: 24
- **Columns**: `Order No`, `Order Date`, `Customer Name`, `Address`, `City`, `State`, `Customer Type`, `Account Manager`, `Order Priority`, `Product Name`, `Product Category`, `Product Container`, `Ship Mode`, `Ship Date`, `Cost Price`, `Retail Price`, `Profit Margin`, `Order Quantity`, `Sub Total`, `Discount %`, `Discount $`, `Order Total`, `Shipping Cost`, `Total`.
- **Exclusion Reason**: Timeframe (2013–2017); wholesale B2B office equipment; incompatible geography (Sydney/Melbourne).

### 2.6 `amazon.csv`
- **Business Role**: Product Reviews & Ratings (Amazon India) | **Rows**: 1,465 | **Columns**: 16
- **Columns**: `product_id`, `product_name`, `category`, `discounted_price`, `actual_price`, `discount_percentage`, `rating`, `rating_count`, `about_product`, `user_id`, `user_name`, `review_id`, `review_title`, `review_content`, `img_link`, `product_link`.
- **Exclusion Reason**: Review catalog without temporal sales history; Amazon ASIN identifiers do not match retail SKUs; no store dimension.

### 2.7 `P  L March 2021.csv`
- **Business Role**: Apparel Marketplace MRP Comparison | **Rows**: 1,330 | **Columns**: 18
- **Columns**: `index`, `Sku`, `Style Id`, `Catalog`, `Category`, `Weight`, `TP 1`, `TP 2`, `MRP Old`, `Final MRP Old`, `Ajio MRP`, `Amazon MRP`, `Amazon FBA MRP`, `Flipkart MRP`, `Limeroad MRP`, `Myntra MRP`, `Paytm MRP`, `Snapdeal MRP`.
- **Exclusion Reason**: Static single-month pricing comparison matrix; no time series; incompatible apparel SKU namespace.

### 2.8 `Sales Dataset.csv`
- **Business Role**: Superstore Order Log | **Rows**: 1,194 | **Columns**: 12
- **Columns**: `Order ID`, `Amount`, `Profit`, `Quantity`, `Category`, `Sub-Category`, `PaymentMode`, `Order Date`, `CustomerName`, `State`, `City`, `Year-Month`.
- **Exclusion Reason**: Sparse consumer orders across 18 US cities; lacks SKU IDs and store identifiers.

### 2.9 `sales_data.csv`
- **Business Role**: Sales Representative Commission Log | **Rows**: 1,000 | **Columns**: 14
- **Columns**: `Product_ID`, `Sale_Date`, `Sales_Rep`, `Region`, `Sales_Amount`, `Quantity_Sold`, `Product_Category`, `Unit_Cost`, `Unit_Price`, `Customer_Type`, `Discount`, `Payment_Method`, `Sales_Channel`, `Region_and_Sales_Rep`.
- **Exclusion Reason**: Only 1,000 transactions across 100 products (10 transactions per product per year); sparse transactions unsuitable for daily time-series forecasting.
