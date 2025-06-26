# Phantom Mask API

API 主機位址：`http://127.0.0.1:8000/`  
所有 API 回傳皆為 JSON 格式。

---

## List all pharmacies open at a specific time and on a day of the week if requested.

`GET /pharmacies/open`  

**描述**: 根據星期與時間查詢營業中的藥局。若未提供參數，預設為目前台灣時間。

### 查詢參數

| 名稱 | 類型 | 必填 | 說明 |
|------|------|------|------|
| day  | string | 否 | 星期，如 `Monday`, `Tuesday`... |
| time | string | 否 | 時間（24 小時制），例如 `14:30` |

### 範例

```
GET /pharmacies/open?day=Tuesday&time=14:30
```

### 回傳格式

```json
[
  {
    "id": 1,
    "name": "DFW Wellness",
    "cash_balance": 328.41
  }
]
```

---

## List all masks sold by a given pharmacy, sorted by mask name or price.

`GET /pharmacies/{pharmacy_id}/masks` 

**描述**: 查詢某藥局販售的所有口罩，可指定排序。

### 查詢參數

| 名稱 | 必填 | 說明 |
|------|------|------|
| pharmacy_id | 是 | 藥局 ID |
| sort_by | 否 | 排序欄位：`name` 或 `price`，預設為 `name` |
| order   | 否 | 排序方式：`asc` 或 `desc`，預設為 `asc` |

### 範例

```
GET /pharmacies/1/masks?sort_by=price&order=desc
```

### 回傳格式

```json
{
  "pharmacy": "DFW Wellness",
  "masks": [
    {
      "name": "True Barrier (green)(3 per pack)",
      "price": 13.7
    }
  ]
}
```

---

## List all pharmacies with more or fewer than x mask products within a specific price range.

`GET /pharmacies/mask_count`  

**描述**: 依價格範圍與口罩數量篩選藥局。

### 查詢參數

| 名稱 | 必填 | 說明 |
|------|------|------|
| min_price | 是 | 價格下限 |
| max_price | 是 | 價格上限 |
| count     | 是 | 要比較的口罩數量 |
| op        | 是 | 運算子：`gt`, `lt`, `ge`, `le`, `eq` |

### 範例

```
GET /pharmacies/pharmacies/mask_count?min_price=10&max_price=50&count=2&op=gt
```

### 回傳格式

```json
[
  {
    "id": 1,
    "name": "DFW Wellness",
    "cash_balance": 347.21,
    "mask_count": 3
  },
]
```

---

## Retrieve the top x users by total transaction amount of masks within a date range.

`GET /users/top_transactions`  

**描述**: 查詢特定期間內交易金額最高的使用者。

### 查詢參數

| 名稱 | 必填 | 說明 |
|------|------|------|
| start | 是 | 起始日期 (YYYY-MM-DD) |
| end   | 是 | 結束日期 (YYYY-MM-DD) |
| top   | 否 | 前幾名，預設為 5 |

### 範例

```
GET /users/top_transactions?start=2021-01-01&end=2021-01-31&top=3
```

### 回傳格式

```json
[
  {
    "user_id": 8,
    "name": "Timothy Schultz",
    "total_spent": 178.28
  }
]
```

---

## Calculate the total number of masks and the total transaction value within a date range.

`GET /purchase/summary`  
**描述**: 統計在指定期間販售的口罩總量與交易總額。

### 查詢參數

| 名稱 | 必填 | 說明 |
|------|------|------|
| start_date | 是 | 起始日期 (YYYY-MM-DD) |
| end_date   | 是 | 結束日期 (YYYY-MM-DD) |

### 範例

```
GET purchase/purchase/summary?start_date=2021-01-01&end_date=2021-01-31
```

### 回傳格式

```json
{
  "total_quantity": 100,
  "total_transaction": 1849.52
}
```

---

## Search for pharmacies or masks by name and rank the results by relevance to the search term.

**Endpoint**: `GET /search`  
**描述**: 搜尋藥局或口罩名稱，並依相關性排序。

### 查詢參數

| 名稱 | 必填 | 說明 |
|------|------|------|
| type    | 是 | `pharmacy` 或 `mask` |
| keyword | 是 | 搜尋關鍵字 |

### 範例

```
GET /search?type=pharmacy&keyword=N
```

### 回傳格式

```json
[
  {
    "id": 9,
    "name": "Centrico"
  },
  {
    "id": 13,
    "name": "Foundation Care"
  },
]
```

---

## Handle the process of a user purchasing masks, possibly from different pharmacies.

**Endpoint**: `POST /purchase`  
**描述**: 使用者購買口罩，可跨藥局。

### 請求格式（JSON）

```json
{
  "user_id": 1,
  "items": [
    {
      "mask_id": 1,
      "quantity": 1
    }
  ]
}
```

### 命令列測試範例

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/purchase/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user_id": 1,
  "items": [
    {
      "mask_id": 1,
      "quantity": 1
    }
  ]
}'
```

### 回傳格式

```json
{
  "message": "Purchase completed",
  "total_spent": 0
}
```

### 失敗回傳
- 無符合口罩
```json
{"detail": "Mask not found"}
```
- 無符合使用者
```json
{"detail": "User not found"}
```
- 使用者餘額不足
```json
{"detail": "Insufficient balance"}
```

---
