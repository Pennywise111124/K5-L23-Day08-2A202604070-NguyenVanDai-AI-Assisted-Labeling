# Label contract — Phố châu Á — BỔ SUNG v1.1 — 2A202604070 - Nguyễn Văn Đại

## 1. Câu hỏi mở đã chốt (từ mục 6 của v1.0)

| # | Câu hỏi | Quyết định | Ảnh ví dụ | `case_id` |
|---|---|---|---|---|
| 2 | Khối xe máy đỗ dày đặc gần camera: từng xe hay `ignore_region`? | Vẽ **từng xe** (một box mỗi xe) khi xe cao từ 20 px trở lên và còn thấy từ 20% diện tích. `ignore_region` chỉ dùng cho cụm vật cao dưới 20 px (4.1.6), không dùng để né các xe lớn gần camera. Thêm **4.1.10**. | `img_006` | CAL-03 |
| 3 | Hàng nhô ra / hàng chất trên thùng: box và mask xe có gồm hàng không? | Hàng nằm trong thùng, khay hoặc giỏ gắn cố định của xe thì **thuộc xe**; hàng chất cao vượt mép thùng hoặc nhô ra khỏi thân xe (hơn ~20% chiều dài xe, 4.1.5) thì **không thuộc xe**. Box và mask dùng **chung một quy tắc**. Thêm **4.1.9**. | `img_008` | CAL-01 |
| 4 | Người ngồi trong xe ba bánh có mui (chỉ thấy thấp thoáng): ngưỡng "còn thấy ≥ 20%" của 4.1.2 | Thay ước lượng % diện tích bằng dấu hiệu nhìn thấy được: gán `person` khi thấy rõ **đầu hoặc vai**; chỉ thấy tay, chân hoặc mảng áo thoáng qua thì không gán; không chắc thì vẫn gán và tick `can_review`. Sửa **4.1.2**. | `img_012`, `img_020` | CAL-02 |
| 1, 5, 6, 7 | Xe đạp điện; kính xe thuộc vật hay không; ảnh đêm; mức `conf` | **Chưa chốt**: không gặp trường hợp nào trong batch 24 ảnh này, nên không có bằng chứng để quyết định. | — | — |

## 2. Ca khó mới (từ lỗi của máy, bẫy lọt, box `can_review`)

| Ảnh | Tình huống | Máy làm gì (model nào) | Quyết định của bạn | Quy tắc mới (vào mục nào của v1.0) |
|---|---|---|---|---|
| `img_013`, `img_003` | Một xe bị tách thành nhiều box | YOLOE: hai box nửa xe (`img_013`); ba box chồng lên một xe ba gác (`img_003`), hai box từng phần bị giữ nguyên khi duyệt | Mỗi vật đúng một box; nếu có box ôm cả xe thì xoá các box từng phần | **4.1.8** (mới): mỗi vật đúng một box, không vẽ box riêng cho từng phần (mui, thân, thùng) của cùng một xe. `case_id` CAL-05 |
| `img_013` | Mask xe có gồm người lái / hành khách ngồi bên trong xe khung hở không | SAM: mask lan sang chân người lái (`sam2.1_b`); `mobile_sam` cắt cụt đáy bánh sau | Mask xe loại người ngồi và người lái (kể cả chân chạm sàn xe), nhưng giữ đủ bánh xe và khung; mask thiếu bánh là lỗi `sai_mask` | **4.2.5** (mới): người ngồi hoặc người lái ở phía trước thân xe nên vùng chạm thuộc người; mask xe phải đủ bánh (theo 4.2.1). `case_id` CAL-07 |
| `img_034`, `img_003`, `img_013`, `img_018` | Xe tải và xe buýt bị gọi `three_wheeler` | YOLOE: điểm 0.85, 0.61, 0.63, 0.53 | Không đổi guideline: lỗi của máy, kiểm từng box `three_wheeler` theo 4.3 (đếm số bánh) khi review | Không đổi (mục 2 và 4.3). `case_id` CAL-04 |
| `img_018`, `img_025`, `img_027`, `img_033`, `img_034` | 10 box cao dưới 20 px vẫn được giữ | Máy: YOLO26 cho các box này; người duyệt chưa chuyển sang `ignore_region` | Không đổi guideline: 4.1.6 đã đủ rõ; đây là lỗi người duyệt | Không đổi (4.1.6). `case_id` CAL-06 |

## 3. Lịch sử thay đổi

| Phiên bản | Thay đổi | Lý do (ca nào, `case_id`) |
|---|---|---|
| v1.0 | Bản giảng viên | — |
| v1.1 | Chốt câu hỏi mở 2, 3, 4; sửa 4.1.2; thêm 4.1.8, 4.1.9, 4.1.10 và 4.2.5; ghi nhận 3 ca không đổi guideline (lỗi máy hoặc lỗi người duyệt) | CAL-01, CAL-02, CAL-03, CAL-05, CAL-07 (quy tắc mới); CAL-04, CAL-06, CAL-08 (không đổi) |
