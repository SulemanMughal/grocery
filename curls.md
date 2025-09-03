## Login API Request
```bash
curl -s -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "StrongP@ss"}'
```



## Refresh Access Token
```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<YOUR_REFRESH_TOKEN>"}'
```


## Create Grocery
```bash
curl -X POST http://localhost:8000/api/v1/groceries/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Downtown Market", "location": "Main & 3rd"}'
```



## Update Grocery
```bash
curl -X PATCH http://localhost:8000/api/v1/groceries/<GROCERY_UID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"location": "Main & 4th"}'
```



## Soft-delete Grocery
```bash
curl -X DELETE http://localhost:8000/api/v1/groceries/<GROCERY_UID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```



## Create Supplier & Assign Grocery
```bash
curl -X POST http://localhost:8000/api/v1/suppliers/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Sam Supplier", "email": "sam@supply.com", "password": "StrongP@ss1", "grocery_uid": "<GROCERY_UID>"}'
```





## Update Supplier
```bash
curl -X PATCH http://localhost:8000/api/v1/suppliers/<SUPPLIER_UID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Samuel Supplier"}'
```




## Soft-delete Supplier
```bash
curl -X DELETE http://localhost:8000/api/v1/suppliers/<SUPPLIER_UID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```




## List Grocery Items (Any Authed User)
```bash
curl -X GET http://localhost:8000/api/v1/groceries/<GROCERY_UID>/items/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```





## Create Grocery Item (Admin or Owning Supplier)
```bash
curl -X POST http://localhost:8000/api/v1/groceries/<GROCERY_UID>/items/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Apple", "item_type": "food", "item_location": "shelf A2", "price": 1.25}'
```





## Update Grocery Item (Admin or Owning Supplier)
```bash
curl -X PATCH http://localhost:8000/api/v1/items/<ITEM_UID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"price": 1.35}'
```



## Soft-delete Grocery Item (Admin or Owning Supplier)
```bash
curl -X DELETE http://localhost:8000/api/v1/items/<ITEM_UID>/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```




## Add Daily Income (Admin or Owning Supplier)
```bash
curl -X POST http://localhost:8000/api/v1/groceries/<GROCERY_UID>/income/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"amount": 4523.75, "date": "2025-09-01"}'
```



## List Daily Income (Admin reads any; Supplier only their grocery)
```bash
curl -X GET "http://localhost:8000/api/v1/groceries/<GROCERY_UID>/income/?start=2025-09-01&end=2025-09-30" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```