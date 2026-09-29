SELECT
    DR.carrier_name,
    COUNT(*) AS delivery_count,
    SUM(DR.quantity) AS total_quantity,
    SUM(CRM.freight_rate) AS total_freight
FROM delivery_records AS DR
LEFT JOIN carrier_master AS CM
    ON DR.carrier_name = CM.carrier_name
LEFT JOIN area_master AS AM
    ON DR.prefecture = AM.prefecture
LEFT JOIN carrier_rate_master AS CRM
    ON CM.carrier_code = CRM.carrier_code
    AND AM.area_code = CRM.area_code
GROUP BY DR.carrier_name;
