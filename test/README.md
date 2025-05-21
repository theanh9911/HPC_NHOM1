# Hướng dẫn kiểm thử hiệu suất hệ thống AI dự đoán viêm phổi

Thư mục này chứa các tài liệu và script phục vụ kiểm thử hiệu suất hệ thống AI dự đoán viêm phổi triển khai trên Docker Swarm.

## Nội dung thư mục
- `locustfile.py`: Kịch bản kiểm thử tải với Locust (upload ảnh tới endpoint /predict)
- `swarm_setup.md`: Hướng dẫn chi tiết setup Docker Swarm nhiều node (manager/worker)
- `report_template.md`: Mẫu báo cáo kết quả kiểm thử hiệu suất

## Quy trình kiểm thử hiệu suất

### Bước 1: Chuẩn bị môi trường
- Cài đặt Docker trên các máy (manager/worker) và khởi tạo Swarm theo hướng dẫn trong `swarm_setup.md`.
- Build và deploy ứng dụng với Docker Compose/Swarm, đảm bảo các service đã chạy và truy cập được endpoint `/predict`.
- Cài Python 3.7+ và locust trên máy dùng để test tải:
  ```bash
  pip install locust
  ```
- Chuẩn bị file ảnh test (ví dụ: `test.jpg`) đúng đường dẫn như trong `locustfile.py` hoặc sửa lại biến `IMG_PATH` cho phù hợp.

### Bước 2: Thực hiện kiểm thử tải
- Chạy Locust:
  ```bash
  cd test
  locust -f locustfile.py --host=http://<IP hoặc localhost>:8081
  ```
- Truy cập http://localhost:8089, nhập số lượng user đồng thời (users), tốc độ spawn (spawn rate), nhấn Start để bắt đầu test.
- Theo dõi các chỉ số: response time, throughput, tỷ lệ lỗi... trên giao diện Locust.

### Bước 3: Thu thập số liệu và giám sát
- Ghi lại kết quả test từ giao diện Locust (có thể chụp màn hình).
- Sử dụng lệnh `docker service ls`, `docker stats`, `docker service ps` để theo dõi trạng thái service, mức sử dụng CPU/RAM của các node.

### Bước 4: Báo cáo kết quả
- Ghi nhận các thông số vào file theo mẫu `report_template.md`.
- Đính kèm ảnh chụp màn hình, biểu đồ (nếu có).
- Đánh giá, so sánh hiệu suất giữa các cấu hình (1 node, nhiều node, số replicas khác nhau...).

## 1. Hướng dẫn kiểm thử với Locust

### Chuẩn bị
- Đảm bảo đã cài Python 3.7+ và cài đặt locust:
  ```bash
  pip install locust
  ```
- Đặt file ảnh test (ví dụ: `test.jpg`) đúng đường dẫn như trong `locustfile.py` hoặc sửa lại biến `IMG_PATH` cho phù hợp.

### Chạy Locust
```bash
cd test
locust -f locustfile.py --host=http://<IP hoặc localhost>:8081
```
- Truy cập giao diện web Locust tại: http://localhost:8089
- Nhập số lượng user đồng thời (users), tốc độ spawn (spawn rate), nhấn Start để bắt đầu test.
- Theo dõi kết quả trực tiếp trên giao diện.

## 2. Hướng dẫn setup Swarm nhiều node
- Xem chi tiết trong file `swarm_setup.md` để biết cách khởi tạo swarm, join node, deploy stack, scale replicas, xem log...

## 3. Ghi nhận và báo cáo kết quả
- Sử dụng mẫu trong `report_template.md` để ghi lại các thông số: thời gian phản hồi, throughput, sử dụng CPU/RAM, tỷ lệ lỗi...
- Có thể chụp ảnh màn hình giao diện Locust, docker stats, docker service ls để minh họa.

## 4. Lưu ý
- Chỉ giữ lại các file cần thiết cho kiểm thử: `locustfile.py`, `swarm_setup.md`, `report_template.md`, README này.
- Xóa các file log, file tạm hoặc script không sử dụng để thư mục gọn gàng.

---
Mọi thắc mắc về kiểm thử hoặc báo cáo, vui lòng liên hệ người hướng dẫn hoặc tham khảo tài liệu chi tiết trong từng file. 