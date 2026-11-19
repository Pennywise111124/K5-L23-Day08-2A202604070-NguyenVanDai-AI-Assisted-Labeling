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

- Lệnh `merge_prelabels.py` đã dùng (dán nguyên): python scripts/merge_prelabels.py work/prelabel/yoloe_all/pre.coco.json work/prelabel/y26_all/pre.coco.json --iou 0.6 --conf 0.3 --thr "three_wheeler=0.15" --split "batch,gold" --out work/prelabel/merged_review/pre.coco.json
- **Phiên bản SAM bạn chọn:** `sam2.1_b.pt` (SAM 2.1), vì trên cùng 10 click ở `img_013` bản này cho mask đầy đủ hơn `mobile_sam`: mui xe 48,0% so với 11,0%, bánh sau 95,1% so với 75,5% (`mobile_sam` cắt cụt đáy bánh ở khoảng y = 656), tổng 38,3% so với 24,8% ảnh, IoU giữa hai mask 0,61. Với `sam2.1_b` tôi làm được cả 3 vật khác loại (tuk-tuk, xích lô, ba gác) trong 15 phút. Đổi lại `sam2.1_b` chậm hơn khoảng 2 lần trên CPU (5,49 so với 2,69 s/ảnh, r06 và r07) và để lại nhiều phần chân người lái hơn (52,1% so với 24,3%). Giới hạn: chỉ so sánh với `mobile_sam` trên 1 vật (`img_013`) và dùng cùng bộ click cho cả hai bản, nên chưa tối ưu click riêng cho từng bản; hai vật còn lại chỉ chạy `sam2.1_b`.
- Lỗi **không sửa được bằng đổi ngưỡng**: YOLO26 chỉ có 80 lớp COCO nên gọi xe ba bánh là car/truck/motorbike/bicycle (r01), và ngưỡng chỉ lọc theo điểm chứ không đổi được nhãn: `img_002` xe bán tải bị gọi `truck 0.73` vẫn còn ở ngưỡng 0.5 (r02). Với `person`, `motorbike` và `car`, trên gold máy bỏ sót 3/23, 2/12 và 1/9 vật ngay cả ở ngưỡng thấp nhất được quét (0.1), vì máy không tạo ra box nào cho các vật đó nên hạ ngưỡng cũng không giúp. Cách xử lý theo kế hoạch: dùng YOLOE cho `three_wheeler` (ngưỡng riêng 0.15), cho YOLOE ưu tiên hơn YOLO26 khi hai box chồng nhau lúc merge, và duyệt tay các bước "bỏ sót" và "sai nhãn" ở Part 4.
- Box **điểm cao mà sai**: `img_002` truck 0.73 (xe bán tải, thuộc `car` theo guideline); `img_011` truck 0.77 (vật ở mép trái); `img_032` bicycle 0.70 (xích lô); `img_012` box three_wheeler 0.45 ở [908,93,116,149] trúng hàng rào chắn kim loại ở mép phải ảnh, không phải xe.
- Box **điểm thấp mà đúng**: `img_012` có hai xe ba bánh gold mà YOLOE chỉ cho điểm 0.24 và 0.19, nên ngưỡng 0.25 mất 2/7 xe và phải hạ xuống 0.15.
- Giới hạn: cả 7 xe ba bánh gold nằm ở 2 ảnh (`img_012`: 4, `img_020`: 3); ngưỡng được chọn và chấm trên chính 4 ảnh gold nên recall 100% là con số lạc quan. Chi phí của 0.15: trên 36 ảnh có 61 box YOLOE ≥ 0.15 so với 47 box ≥ 0.25, tức thêm 14 box cần duyệt. Ở `img_012`, box hàng rào 0.45 có điểm cao hơn cả 4 xe ba bánh đúng (0.19–0.36) nên không ngưỡng nào tách được hai nhóm này; vì vậy ngưỡng 0.15 chỉ có nghĩa là giữ recall và chấp nhận phải xoá box thừa khi review, chứ không loại hết được lỗi.

## 2. AI error profile (từ `qc/review_stats.md`)

Mẫu: 24 ảnh batch; 519 box máy; 495 đối tượng sau duyệt. Đã loại 21 đối tượng nằm quanh 12 ảnh bẫy khỏi bảng (lỗi nhân tạo, không phản ánh chất lượng máy).

| Trạng thái | Số | Tỉ lệ | Mẫu số |
|---|---|---|---|
| accepted | 471 | 90,8% | 519 box máy |
| edited | 9 | 1,7% | 519 box máy |
| deleted | 34 | 6,6% | 519 box máy |
| added | 15 | 3,0% | 495 đối tượng sau duyệt |

- 471 + 9 + 34 = 514; 5 box máy còn lại nằm trong vùng `ignore_region` tôi vẽ (cả 5 vùng ở `img_024`) nên script không tính là deleted.
- Trong deleted + added có 12 trường hợp là đổi lớp (box đúng chỗ, sai lớp), nên máy bỏ sót thật chỉ khoảng 15 − 12 = 3 vật.

| Lớp | Box máy | accepted | edited | deleted | added |
|---|---|---|---|---|---|
| person | 271 | 267 (98,5%) | 1 | 3 | 0 |
| motorbike | 138 | 135 (97,8%) | 1 | 2 | 1 |
| car | 49 | 48 (98,0%) | 0 | 1 | 4 |
| bicycle | 8 | 6 (75,0%) | 0 | 2 | 2 |
| bus | 3 | 3 (100%) | 0 | 0 | 3 |
| truck | 5 | 1 (20,0%) | 0 | 4 | 3 |
| three_wheeler | 40 | 11 (27,5%) | 7 | 22 | 2 |

- **Lớp máy tệ nhất: `three_wheeler`.** Trong 40 box máy chỉ 11 (27,5%) được giữ nguyên, 22 (55,0%) bị xoá, 7 bị sửa. Ba lớp lớn (person, motorbike, car) đều được giữ nguyên khoảng 98%. `truck` và `bus` chỉ có 5 và 3 box máy nên không đủ mẫu để kết luận. **Không chỉ do ngưỡng 0.15 thấp:** trong 22 box bị xoá có 8 box điểm ≥ 0.5, cao nhất 0.85. Các kiểu lỗi quan sát được: (1) YOLOE gán `three_wheeler` cho xe tải và xe buýt với điểm cao: `img_034` box 0.85 (tôi gán lại thành `truck`), `img_003` box 0.61 (`truck`), `img_013` box 0.63 và `img_018` box 0.53 (`bus`); (2) gán cho vật không phải xe: ở `img_014` cả 3 box `three_wheeler` trúng gánh hàng rong và kệ hàng nên bị xoá hết; (3) tách một xe thành hai box nửa xe chồng nhau (`img_013`, tôi gộp lại thành một box). Đổi ngưỡng không giúp được: ở 0.25 chỉ loại 6/22 box thừa nhưng mất 4/18 box được giữ; ở 0.5 vẫn còn 8/22 box thừa mà mất 9/18 box được giữ (18 = accepted + edited; so `pre_traps.coco.json` với `batch_reviewed.json`, đã loại vùng quanh bẫy).
- **So với gold** (4 ảnh, 56 vật gold): precision của máy 45/68 = 66,2% (KTC 95%: 54–76%), recall 45/56 = 80,4% (KTC 95%: 68–89%). Số này lạc quan vì ngưỡng được chọn trên chính 4 ảnh gold (in-sample).

## 3. Thiên kiến tự động hóa và ảnh bẫy

- **Bắt bẫy: 6/12 = 50,0%** (KTC 95%: 25–75%; ngưỡng đạt 80%). Theo loại: `extra` 3/3, `wrong_class` 2/3, `loose` 1/3, `missing` 0/3. Lọt: `img_021`, `img_024`, `img_013` (missing); `img_033` (wrong_class); `img_035`, `img_014` (loose).
- **Vì sao lọt:** Cả 3 bẫy `missing` lọt hết. Đây là loại lỗi chỉ phát hiện được khi tự quét ảnh trước khi nhìn nhãn máy (bước 0–1 của checklist). Hai trong ba ảnh (`img_021` có 38 vật, `img_024` có 42 vật sau duyệt) thuộc nhóm ảnh dày xe máy. Ngược lại `extra` bắt 3/3 vì box thừa nằm sẵn trên màn hình, chỉ cần kiểm có vật thật hay không.
- **Accepted cao mà bắt bẫy thấp** (90,8% so với 50,0%) cho thấy tôi giữ nguyên rất nhiều box, một phần vì máy thật sự tốt ở ba lớp lớn (~98%), nhưng 6/12 lỗi nhân tạo vẫn lọt nên "accepted cao" không chứng minh tôi duyệt tốt. Đây là dấu hiệu thiên kiến tự động hóa, rõ nhất ở lỗi bỏ sót (0/3). `added` chỉ 3,0% nhưng không có nghĩa máy ít sót: 3 bẫy `missing` bị xoá hộ không được tôi vẽ lại, và recall của máy trên gold chỉ 80,4% (FN 11/56, gồm cả sai lớp). Hai con số này gợi ý (chưa chứng minh được, vì gold và batch là các ảnh khác nhau) rằng tôi có thể đã bỏ sót nhiều lỗi bỏ sót trong batch.
- Hạn chế khác của lần duyệt: 10 box cao dưới 20 px chưa chuyển sang `ignore_region` (`img_018` ×5, `img_025`, `img_027` ×2, `img_033`, `img_034`); `ignore_region` chỉ dùng ở `img_024`. Sau duyệt, `img_003` (không phải ảnh bẫy) vẫn còn 3 box `three_wheeler` chồng lên cùng một chiếc xe ba gác (box cả xe, box phần mui IoU 0,36, box phần thân dưới IoU 0,46); hai box từng phần là box máy tôi đã giữ nguyên (điểm 0,21 và 0,80). Đây là lỗi tôi bỏ sót ngoài 12 bẫy, nên accepted 90,8% đã bao gồm cả những box sai như vậy.

## 4. Máy có đáng dùng không?

- **Thời gian** (`time_log.csv`): gán tay 32 phút / 4 ảnh = 8,0 phút/ảnh (0,57 phút/vật; 56 vật gold); duyệt có pre-label 40 phút / 24 ảnh = 1,67 phút/ảnh (0,08 phút/vật; 503 đối tượng, không tính 5 vùng `ignore_region`). Tiết kiệm 79,2% theo phút/ảnh và 86,1% theo phút/vật. **Thiên lệch:** tôi gán gold trước nên đã quen kiểu cảnh; batch dày hơn gold (21,0 so với 14,0 vật/ảnh) nên so phút/vật công bằng hơn phút/ảnh; và 1,67 phút/ảnh thấp hơn mức khoảng 3 phút/ảnh mà tài liệu gợi ý, nên phần tiết kiệm này một phần có thể đến từ việc duyệt nhanh hơn (xem mục 3: bắt bẫy 6/12). Tiết kiệm thời gian vì vậy không đồng nghĩa với chất lượng tương đương.
- **Kết luận:** pre-label **đáng dùng cho `person`, `motorbike`, `car`** (giữ nguyên khoảng 98% box máy, rất ít phải sửa), **không đáng tin cho `three_wheeler`** (chỉ 27,5% giữ nguyên, 55,0% bị xoá, nên lớp này phải duyệt như vẽ mới). Không dùng accepted 90,8% để kết luận máy tốt, vì bắt bẫy chỉ 50% và recall trên gold 80,4%: lỗi bỏ sót vẫn còn và máy không tự báo.
- **Ba quy tắc giảm thiên kiến của tôi** (mỗi quy tắc kiểm tra được):
  1. Với mọi ảnh, ghi vào log số vật tôi tự đếm ở bước 0 (khi nhãn máy bị ẩn) trước khi hiện nhãn; kiểm bằng log đủ 24/24 ảnh và đối chiếu với số vật cuối cùng.
  2. Với ảnh dày (trên 30 vật, như `img_021`, `img_024`), quét theo bốn góc phần tư và dành ít nhất khoảng 3 phút/ảnh; kiểm bằng log thời gian từng nhóm 5 ảnh và bằng số bẫy `missing` bắt được ở lần đo sau (mục tiêu ≥ 2/3).
  3. Với lớp máy hay sai (`three_wheeler`), lọc theo nhãn (Filters) và xem từng box bằng mắt trước khi chấp nhận, không dựa vào `conf`; kiểm bằng số box `three_wheeler` bị giữ nguyên so với số bị xoá trong `review_stats`.

## 5. Mask SAM cho 3 vật (Part 5)

| Ảnh | SAM (phiên bản) | Số click | Mask gồm người lái / hàng hoá? | Lỗi quan sát | File trong `masks/` |
|---|---|---|---|---|---|
| `img_013` (tuk-tuk có người lái và hành khách) | sam2.1_b.pt (bản chọn); so với mobile_sam.pt | Bản cuối `v3`: 10 click (6 dương: thân, mui, sàn, bánh sau, bánh trước, ghế; 4 âm: người lái ×3, hành khách). Đã thử `v1` (5 click), `v2` (7 click); `mobile_sam` dùng lại đúng 10 click của `v3` | `v3`: loại phần lớn người lái (đầu 5,7%, áo 16,3% vùng bị tô) và hành khách (2,9%); **chân và quần người lái vẫn bị tô khoảng một nửa (52,1%)**. Không có hàng hoá nhô ra ở ảnh này. | `v1`: 300.177 px (43,0% ảnh; 57,0% box xe 526.879 px), dính người lái (đầu 73,1%, chân 91,3%) vì click dương thứ 3 đặt trúng chân ông ấy. `v2`: 109.285 px (15,6% ảnh; 20,7% box xe), loại được người nhưng mất bánh sau (7,9%), bánh trước (3,2%), ghế (1,6%) vì 4 click âm gần thân co mask lại và không có click dương trên bánh. `v3`: 271.009 px (38,8% ảnh; 51,4% box xe), 1 polygon, giữ bánh sau 95,1%, bánh trước 69,6%, thân có biển số 93,4%; còn lỗi chân người lái và vài lỗ nhỏ ở mui, ghế. `v3` với `mobile_sam`: ≈ 173.000 px (24,8% ảnh), loại người lái sạch hơn (áo 1,2%, chân 24,3%) nhưng mui xe chỉ còn 11,0% và đáy bánh sau bị cắt cụt ở khoảng y = 656; IoU hai mask 0,61. | `tuktuk_img013.jpg`, `tuktuk_img013_v2.jpg`, `tuktuk_img013_v3.jpg`, `tuktuk_img013_v3_mobile.jpg` |
| `img_010` (xích lô nhìn từ sau, 3 bánh, có người đạp và khách) | sam2.1_b.pt | 11 click (6 dương: mui, 3 bánh, 2 ghế; 5 âm: người đạp ×2, người áo trắng, mui xích lô phía sau, người áo kaki); chạy 1 lần | Không: loại người đạp (áo khoác 2,4%, quần 5,6% vùng bị tô), người áo trắng (8,6%) và người áo kaki (0,8%). Không có hàng hoá. | 54.390 px (7,8% ảnh; 24,7% box xe 220.016 px), 2 polygon. Tốt: mui 81,5%, bánh trái 86,3%, không tràn sang xích lô phía sau. Còn thiếu: ghế xám chỉ phủ 28–34%, bánh phải 49,8%, bánh giữa 46,9%; mask chủ yếu là các thanh khung mảnh, đúng với 4.2.2 (bỏ khoảng trống lớn xuyên khung) nhưng khiến mask khá rỗng. | `xichlo_img010.jpg` |
| `img_008` (xe ba gác chở chuối, xe thứ hai liền kề) | sam2.1_b.pt | 9 click (4 dương: bánh trái, bánh phải, tấm ván xanh, thanh khung; 5 âm: chuối ×2, người bán, bánh và thùng đỏ của xe liền kề); chạy 1 lần | Không gồm hàng hoá: chuối bị loại (hàng trên 1,3%, hàng dưới 1,0% vùng bị tô); không có người lái; xe liền kề không bị tràn (bánh 0,8%, thùng đỏ 2,0%). | 29.435 px (4,2% ảnh; 25,3% box xe 116.293 px), **4 polygon**: chuối che gần hết thùng nên mask vỡ thành nhiều mảnh rời. Bánh trái 83,7% nhưng bánh phải chỉ 31,0%, tấm ván xanh 50,8%, thanh khung ngang 10,3%: thiếu phần lớn khung và bánh phải bị rỗng. | `bagac_img008.jpg` |

- Đối chiếu guideline mục 4.2: **giúp:** 4.2.4 (hai vật chạm nhau không chồng lên nhau) là cơ sở để loại người ngồi (img_013, img_010) và xe liền kề (img_008) khỏi mask; 4.2.1 (bánh xe thuộc vật) cho biết `v2` của `img_013` và `mobile_sam` cắt cụt bánh là lỗi; 4.2.2 (bỏ lỗ lớn, không vẽ lỗ nhỏ) giải thích mask rỗng của xích lô `img_010`. **Thiếu:** (1) người ngồi *bên trong* xe ba bánh khung hở (người lái, hành khách) có thuộc mask xe không: guideline không nói, tôi tự quyết định loại; (2) chân người lái chạm sàn xe (`img_013`): "vùng chạm thuộc vật ở phía trước" không xác định được vật nào ở phía trước; (3) hàng hoá chất trên thùng xe (`img_008`): guideline 4.1.5 chỉ nói về hàng nhô ra khỏi xe quá 20% và câu hỏi mở số 3 ở mục 6 vẫn chưa chốt, nên tôi chọn loại chuối khỏi mask; (4) một vật bị che thành nhiều mảnh (`img_008`, 4 polygon): không nói nên dùng một polygon hay nhiều. Cả bốn là ứng viên cho calibration ở Part 6.

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
