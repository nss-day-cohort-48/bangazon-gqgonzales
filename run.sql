SELECT p.id,
    p.name AS product_name,
    p.customer_id,
    p.price,
    p.description,
    p.quantity,
    p.created_date,
    p.category_id,
    p.location,
    p.image_path,
    u.id user_id,
    u.first_name || ' ' || u.last_name AS full_name
FROM bangazonapi_product p
    JOIN bangazonapi_customer c ON p.customer_id = c.id
    JOIN auth_user u ON c.user_id = u.id
WHERE p.price >= 1000
ORDER BY p.price ASC;