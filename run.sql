SELECT p.id,
    p.name AS product_name,
    p.price,
    p.description,
    p.quantity,
    p.created_date,
    p.category_id,
    p.location,
    p.image_path
FROM bangazonapi_product p
WHERE p.price >= 1000
ORDER BY p.price ASC;