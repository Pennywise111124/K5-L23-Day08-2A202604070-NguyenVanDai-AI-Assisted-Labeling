# Báo cáo Day 08 — 2A202604070 - Nguyễn Văn Đại

> Một file duy nhất cho cả bài (đã gộp recipe, QC và ghi chú cá nhân). Mọi con số kèm **mẫu số** và nguồn (file nào).

## 1. Model và recipe (Part 2–3)

| Lớp | Gold | Model + cỡ | Ngưỡng | Vì sao (dẫn `run_id` trong `model_log.csv`) |
|---|---|---|---|---|
| person | 23 | YOLO26m | 0.3 (mặc định) | Recall tối đa 20/23 = 87,0% (< 90%) nên không chọn ngưỡng riêng; ở 0.3: recall 19/23 = 82,6%, precision 19/33 = 57,6% (r01, r02, r08) |
| motorbike | 12 | YOLO26m | 0.3 (mặc định) | Recall tối đa 10/12 = 83,3% (< 90%); ở 0.3: recall 8/12 = 66,7%, precision 8/11 = 72,7% (r08) |
| car | 9 | YOLO26m | 0.3 (mặc định) | Recall tối đa 8/9 = 88,9% (< 90%, thiếu 1 xe); ở 0.3: precision 8/13 = 61,5% (r08) |
| bicycle | 4 | YOLO26m | 0.3 (mặc định) | Chỉ 4 vật gold (< 5) nên không chọn ngưỡng theo lớp; ở 0.3: recall 2/4 = 50%, precision 2/5 = 40% (r08) |
| bus | 1 | YOLO26m | 0.3 (mặc định) | 1 vật gold (< 5); ở 0.3: 1/1 (r08) |
| truck | 0 | YOLO26m | 0.3 (mặc định) | Không có vật gold trong 4 ảnh (r08) |
| three_wheeler | 7 | YOLOE-26s, prompt: tuk-tuk, cyclo, cargo tricycle | 0.15 | Recall 7/7 = 100%, precision 7/9 = 77,8%; ở 0.25 (ngưỡng đã dùng ở r03) chỉ 5/7 = 71,4%. YOLO26 không có lớp này (r01, r03, r09) |

Nguồn số đo: `qc/threshold_sweep.csv` (mẫu số: 4 ảnh gold, 56 vật có lớp trong bảng).

- Lệnh `merge_prelabels.py` đã dùng (dán nguyên): <<điền sau khi chạy ở Part 4>>
- **Phiên bản SAM bạn chọn** (SAM 1 / 2.1 / 3) và lý do: <<điền sau Part 5>>
- Lỗi **không sửa được bằng đổi ngưỡng**: YOLO26 chỉ có 80 lớp COCO nên gọi xe ba bánh là car/truck/motorbike/bicycle (r01), và ngưỡng chỉ lọc theo điểm chứ không đổi được nhãn: `img_002` xe bán tải bị gọi `truck 0.73` vẫn còn ở ngưỡng 0.5 (r02). Với `person`, `motorbike` và `car`, trên gold máy bỏ sót 3/23, 2/12 và 1/9 vật ngay cả ở ngưỡng thấp nhất được quét (0.1), vì máy không tạo ra box nào cho các vật đó nên hạ ngưỡng cũng không giúp. Cách xử lý theo kế hoạch: dùng YOLOE cho `three_wheeler` (ngưỡng riêng 0.15), cho YOLOE ưu tiên hơn YOLO26 khi hai box chồng nhau lúc merge, và duyệt tay các bước "bỏ sót" và "sai nhãn" ở Part 4.
- Box **điểm cao mà sai**: `img_002` truck 0.73 (xe bán tải, thuộc `car` theo guideline); `img_011` truck 0.77 (vật ở mép trái); `img_032` bicycle 0.70 (xích lô); `img_012` box three_wheeler 0.45 ở [908,93,116,149] trúng hàng rào chắn kim loại ở mép phải ảnh, không phải xe.
- Box **điểm thấp mà đúng**: `img_012` có hai xe ba bánh gold mà YOLOE chỉ cho điểm 0.24 và 0.19, nên ngưỡng 0.25 mất 2/7 xe và phải hạ xuống 0.15.
- Giới hạn: cả 7 xe ba bánh gold nằm ở 2 ảnh (`img_012`: 4, `img_020`: 3); ngưỡng được chọn và chấm trên chính 4 ảnh gold nên recall 100% là con số lạc quan. Chi phí của 0.15: trên 36 ảnh có 61 box YOLOE ≥ 0.15 so với 47 box ≥ 0.25, tức thêm 14 box cần duyệt. Ở `img_012`, box hàng rào 0.45 có điểm cao hơn cả 4 xe ba bánh đúng (0.19–0.36) nên không ngưỡng nào tách được hai nhóm này; vì vậy ngưỡng 0.15 chỉ có nghĩa là giữ recall và chấp nhận phải xoá box thừa khi review, chứ không loại hết được lỗi.

## 2. AI error profile (từ `qc/review_stats.md`)

| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted | <<>> | <<>> | <<box máy>> |
| edited | <<>> | <<>> | <<>> |
| deleted | <<>> | <<>> | <<>> |
| added | <<>> | <<>> | <<đối tượng sau duyệt>> |

- Lớp nào máy tệ nhất? Vì sao (dẫn ảnh)? <<>>
- So với gold: precision / recall của **máy** <<>> (mẫu số: <<đối tượng gold>>)

## 3. Thiên kiến tự động hóa và ảnh bẫy

- Bắt bẫy: <<.../12>>; loại nào lọt: <<>>; vì sao (bạn đã bỏ bước nào của checklist)? <<>>
- Accepted cao mà bắt bẫy thấp (hoặc ngược lại) nói gì về cách bạn duyệt? <<>>

## 4. Máy có đáng dùng không?

- Thời gian (từ `time_log.csv`): gán tay <<... phút/ảnh>> vs duyệt <<... phút/ảnh>>. Thiên lệch (bạn gán gold trước nên đã quen cảnh): <<>>
- Kết luận: <<có / không / chỉ cho lớp nào>>, dựa trên <<số liệu>>
- **Ba quy tắc giảm thiên kiến của bạn** (mỗi quy tắc kiểm tra được bằng số hoặc việc làm):
  1. <<>>
  2. <<>>
  3. <<>>

## 5. Mask SAM cho 3 vật (Part 5)

| Ảnh | SAM (phiên bản) | Số click | Mask gồm người lái / hàng hoá? | Lỗi quan sát | File trong `masks/` |
|---|---|---|---|---|---|
| <<img_0xx>> | <<>> | <<>> | <<>> | <<>> | <<>> |

- Đối chiếu guideline mục 4.2: quy tắc nào giúp, quy tắc nào thiếu? <<>>
- *(Tuỳ chọn)* Interactor SAM trong CVAT: làm được / không (lỗi gì, đã thử gì); khác gì offline: <<>>

## 6. Calibration (Part 6)

- Số quyết định: <<>> (`calibration_decisions.csv`); quan trọng nhất (dẫn `CAL-xx`): <<>>
- Quy tắc mới đã vào `guideline_v1.1_calibrated.md`: <<>>
- Nguyên nhân gốc: <<guideline mơ hồ / chưa nắm quy tắc / máy>>

## 7. QC và quyết định (Part 6)

- Mẫu: <<n>> ảnh (<<m>> ảnh `can_review` + <<k>> ngẫu nhiên, seed 42); người kiểm: bạn (**hạn chế**: bạn vừa là người duyệt).
- Lỗi theo **đối tượng**: <<.../... = ...%>> · theo **ảnh**: <<.../... = ...%>> (ngưỡng Release ≤ 2%)
- Top lỗi (trong: bỏ sót, thừa, sai lớp, sai vị trí/kích thước, sai thuộc tính, sai mask) + một ảnh ví dụ mỗi loại: <<>>
- **Giới hạn mẫu nhỏ** (cận trên 95% trong `qc_report_auto.md`): <<>>
- Script kiểm được / không kiểm được (ví dụ ôm sát, cùng bỏ sót với máy, theo checklist thật): <<>>

**Quyết định: <<Release / Hold / Rework>>**, ngày <<YYYY-MM-DD>>. Lý do (đi theo Hold → Rework → Release): <<>>
Nếu Rework / Hold, việc cần làm tiếp: <<>>

## 8. Ghi chú cá nhân

- **Dùng AI để làm bài** (công cụ nào, việc gì, kiểm tra thế nào; "không dùng" nếu không): <<>>
- Gold có bị nhiễm không (bạn có nhìn pre-label hay hỏi AI trước khi gán xong)? <<không / có, như sau: ...>>
- Máy / GPU / CVAT dùng; vướng mắc cài đặt: <<>>
- Dùng cache `data/cache/` thay vì tự chạy? <<không / có, vì ...>>
- Lỗi / bug script đã gặp (nếu có): <<>>
- Một điều bạn làm khác lần sau: <<>>
