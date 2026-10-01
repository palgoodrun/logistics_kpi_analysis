SELECT
    DR.delivery_id,
    DR.carrier_name,
    CM.carrier_code,
    DR.prefecture,
    AM.area_code,
    CRM.freight_rate
FROM delivery_records AS DR
LEFT JOIN carrier_master AS CM
    ON DR.carrier_name = CM.carrier_name
LEFT JOIN area_master AS AM
    ON DR.prefecture = AM.prefecture
LEFT JOIN carrier_rate_master AS CRM
    ON CM.carrier_code = CRM.carrier_code
    AND AM.area_code = CRM.area_code
    WHERE
        CM.carrier_code IS NULL
        OR AM.area_code IS NULL
        OR CRM.freight_rate IS NULL;