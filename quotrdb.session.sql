DELETE FROM quotrapi_item
WHERE make = "Sony";

SELECT * FROM quotrapi_item
WHERE make = "Sony";

DELETE  FROM quotrapi_accessory
WHERE id > 0;

SELECT * FROM quotrapi_item
WHERE make = "Belden"
or model = "Belden"
or cost = "Belden"
or description = "Belden";