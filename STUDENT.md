# Thông tin học viên

- Họ và tên: Nguyễn Văn Đại
- MSHV: 2A202604070 
- Lớp (L2 / L3 / khác): L2B
- Tài khoản GitHub: Pennywise111124
- Repo bài nộp (URL): https://github.com/Pennywise111124/K5-L23-Day08-2A202604070-NguyenVanDai-AI-Assisted-Labeling
- Commit chốt bài (hash): <<>>
- Máy: Windows, Python 3.12.10, không có GPU (chạy CPU)
- CVAT (Docker): v2.81.0

## Kết quả tóm tắt (điền cuối bài; số lấy từ `submission/qc/*`, kèm mẫu số)

- Máy: accepted / edited / deleted: 471 / 9 / 34 (mẫu số: 519 box máy); added: 15 (mẫu số: 495 đối tượng sau duyệt)
- So với gold: precision / recall của **máy** 66,2% / 80,4% (45/68 và 45/56)
- Bắt bẫy: 6/12 = 50,0%
- Thời gian: gán tay 8,0 phút/ảnh; duyệt có pre-label 1,67 phút/ảnh
- Lỗi QC: 100% theo ảnh (5/5), 6,9% theo đối tượng (7/102)
- **Quyết định:** Rework: ảnh lỗi 100% > 2% và bắt bẫy 6/12 = 50% < 80%
