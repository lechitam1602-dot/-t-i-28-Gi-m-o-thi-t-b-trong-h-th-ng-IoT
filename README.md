\# Đề tài 28: Giả mạo thiết bị trong hệ thống IoT



Chương trình giả lập hệ thống tiếp nhận dữ liệu IoT (Telemetry Server) bằng Flask API, tích hợp cơ chế xác thực danh tính thiết bị ("device\_id" \& "token" / "HMAC") nhằm phát hiện và ngăn chặn các nguy cơ giả mạo thiết bị.



\## Cấu trúc thư mục

Đề tài 28 - Giả mạo thiết bị trong hệ thống IoT

├── README.md               # Hướng dẫn chạy và kiểm thử dự án

├── report/                 # Báo cáo tiểu luận (.docx / .pdf)

├── slides/                 # Slide thuyết trình (.pptx)

├── src/                    # Mã nguồn chương trình

│   └── code\_demo.py        # Flask API kiểm tra và xác thực thiết bị

├── configs/                # Cấu hình hệ thống

│   └── config.json         # Tham số cấu hình server \& bảo mật

├── data/                   # Dữ liệu quản lý

│   └── devices.json        # Danh sách thiết bị hợp lệ (Whitelist)

├── results/                # Kết quả kiểm thử

│   ├── screenshots/        # Ảnh chụp màn hình quá trình test

│   └── logs/               # Nhật ký ghi nhận các truy cập (app.log)

└── references/             # Tài liệu tham khảo

&#x20;   └── link\_nguon.md       # Nguồn OWASP ISVS, Flask, Mbed TLS



**Yêu cầu môi trường \& Cài đặt**



&#x09;Python: Phiên bản 3.8 trở lên.

&#x09;Thư viện phụ thuộc: flask



Cài đặt thư viện Flask bằng lệnh: pip install flask



**Hướng dẫn khởi chạy Server**

&#x09;Mở cửa sổ Terminal / Command Prompt.



&#x09;Di chuyển vào thư mục dự án: cd "Đề tài 28 - Giả mạo thiết bị trong hệ thống IoT"

&#x09;Chạy Server Flask: python src/code\_demo.py

&#x09;Server sẽ khởi chạy tại giao diện: http://127.0.0.1:5000/telemetry



**Hướng dẫn Kiểm thử (Testing)**



Mở một cửa sổ Terminal mới (hoặc sử dụng Postman) để gửi các request kiểm thử:



&#x09;1. Request Hợp lệ (Gửi đúng device\_id \& token):

curl -X POST \[http://127.0.0.1:5000/telemetry](http://127.0.0.1:5000/telemetry) -H "Content-Type: application/json" -d "{\\"device\_id\\": \\"sensor-node-01\\", \\"value\\": 25.5, \\"token\\": \\"secret\_token\_12345\\"}"



&#x09;Kết quả trả về: Status 200 OK với thông điệp chấp nhận dữ liệu.



&#x09;2. Request Giả mạo Device ID (ID không tồn tại):

curl -X POST \[http://127.0.0.1:5000/telemetry](http://127.0.0.1:5000/telemetry) -H "Content-Type: application/json" -d "{\\"device\_id\\": \\"fake-sensor-99\\", \\"value\\": 99.9, \\"token\\": \\"secret\_token\_12345\\"}"



&#x09;Kết quả trả về: Status 401 Unauthorized, báo lỗi thiết bị giả mạo.



&#x09;3. Request Giả mạo Token (Đúng ID nhưng sai Token):

curl -X POST \[http://127.0.0.1:5000/telemetry](http://127.0.0.1:5000/telemetry) -H "Content-Type: application/json" -d "{\\"device\_id\\": \\"sensor-node-01\\", \\"value\\": 25.5, \\"token\\": \\"wrong\_token\_123\\"}"



&#x09;Kết quả trả về: Status 403 Forbidden, báo lỗi Token không hợp lệ.



**Xem nhật ký bảo mật (Log)**

Toàn bộ lịch sử kết nối hợp lệ cũng như các cảnh báo tấn công giả mạo \[SPOOF DETECTED] đều được hệ thống tự động ghi lại tại: results/logs/app.log

