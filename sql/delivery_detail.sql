SELECT
    DR.delivery_id,
    DR.delivery_date,
    DR.carrier_name,
    DR.prefecture,
    DR.quantity,
    DR.delayed,
    DR.origin_code,
    DR.completion_date,
    CRM.freight_rate
FROM delivery_records AS DR
LEFT JOIN carrier_master AS CM
    ON DR.carrier_name = CM.carrier_name
LEFT JOIN area_master AS AM
    ON DR.prefecture = AM.prefecture
LEFT JOIN carrier_rate_master AS CRM
    ON CM.carrier_code = CRM.carrier_code
    AND AM.area_code = CRM.area_code;