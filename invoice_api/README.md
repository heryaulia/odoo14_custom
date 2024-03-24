# Invoice API Documentation

This documentation outlines the API endpoints available in the `InvoiceAPI` class, which facilitates interactions with invoice-related functionalities in an Odoo system.

## Endpoints

### POST `/api/invoices`

This endpoint is used to create one or more invoices based on the provided JSON payload.

#### Parameters:

- `invoices`: A JSON array containing the invoice data to be created.
 - `partner_id`: The ID of the partner for the invoice.
 - `invoice_line_ids`: An array of invoice line items.
   - `product_id`: The ID of the product for the line item.
   - `quantity`: The quantity of the product.
   - `price_unit`: The unit price of the product.

```json
{
 "invoices": [
   {
     "partner_id": 1,
     "invoice_line_ids": [
       {
         "product_id": 1,
         "quantity": 2,
         "price_unit": 30.5
       },
       {
         "product_id": 2,
         "quantity": 3,
         "price_unit": 45.0
       }
     ]
   },
   {
     "partner_id": 2,
     "invoice_line_ids": [
       {
         "product_id": 3,
         "quantity": 1,
         "price_unit": 15.5
       }
     ]
   }
 ]
}
```



#### Response:

A JSON object containing the operation's success status and a message.

#### Example Response:

```json
{
  "success": true,
  "message": "Invoice creation tasks have been enqueued"
}
```



### POST `/api/invoice/payment`

This endpoint is used to register payment for an invoice based on the provided JSON payload.

#### Parameters:

- `jsonrpc`: The JSON-RPC protocol version.
- `method`: The method to be called. In this case, `call`.
- `params`: A dictionary containing the parameters for the method.
  - `invoice_id`: The ID of the invoice for which the payment is being made.
  - `amount`: The amount to be paid.
  - `journal_id`: The ID of the journal in which the payment should be recorded.
- `id`: A unique identifier for the request.

```json
{
  "jsonrpc": "2.0",
  "method": "call",
  "params": {
    "invoice_id": 10,
    "amount": 3143750,
    "journal_id": 6
  },
  "id": 1
}
```



#### Response:

A JSON object containing the operation's success status and a message.

#### Example Response:

```json
{
    "jsonrpc": "2.0",
    "id": 1,
    "result": {
        "success": true,
        "message": "Payment created and associated with invoice successfully",
        "payment_id": 3
    }
}
```



## Endpoints

### GET `/api/invoice?invoice_id={id}`

This endpoint is used to retrieve the details of a specific invoice, including its payment information.

#### Parameters:

- `invoice_id`: The ID of the invoice to be retrieved. This should be passed as a query parameter in the URL.

#### Response:

A JSON object containing the invoice details and payment information.

#### Example Response:

```json
{
  "success": true,
  "data": {
    "invoice_id": 85,
    "invoice_ref": "INV/2024/03/0030",
    "partner_name": "Deco Addict",
    "state": "posted",
    "amount_total": 169.05,
    "outstanding_balance": 0.0,
    "payments": [
      {
        "payment_id": 189,
        "payment_ref": "Customer Payment $ 169.05 - Deco Addict - 03/24/2024",
        "payment_date": "2024-03-24",
        "payment_amount": 169.05,
        "currency": "$"
      }
    ]
  }
}
```


## Endpoints

### PUT `/api/invoice`

This endpoint is used to update an existing invoice.

#### Parameters:

- `invoice_id`: The ID of the invoice to be updated.
- `invoice_date`: The new date for the invoice (optional).
- `partner_id`: The new partner ID for the invoice (optional).
- `invoice_lines`: A JSON array containing the updated invoice line items.
  - `product_id`: The ID of the product.
  - `quantity`: The quantity of the product.
  - `price_unit`: The unit price of the product.

```json
{
  "invoice_id": 107,
  "invoice_date": "2023-03-24",
  "partner_id": 2,
  "invoice_lines": [
    {
      "product_id": 1,
      "quantity": 2.0,
      "price_unit": 10.0
    },
    {
      "product_id": 2,
      "quantity": 3.0,
      "price_unit": 15.0
    }
  ]
}
``` 




#### Response:
A JSON object containing the operation's success status and a message.

#### Example Response:
```json
{
 "success": true,
 "message": "Invoice updated successfully"
}
``` 

