SELECT
    COUNT(delivery_id) AS total_deliveries,
    SUM(quantity) AS total_quantity
FROM delivery_records AS DR;
