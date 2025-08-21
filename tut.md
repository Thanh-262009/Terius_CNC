# Hướng Dẫn Sử Dụng Terius CNC

## Lưu Ý Trước Khi Sử Dụng
1. **Không Bán Mã Nguồn Này** - Mã nguồn được cung cấp miễn phí // nếu bán hãy chính sửa lại.
2. **Tùy Chỉnh Được** - Vì đây là mã nguồn CNC, bạn có thể chỉnh sửa (banner & power) để mở bán.

## Hướng Dẫn Sử Dụng
1. **Chạy File Setup**  
   - Trước tiên, chạy file `setup.py` để thiết lập môi trường.
2. **Khởi Động Chương Trình**  
   - Sau khi chạy thành công `setup.py`, tiếp tục chạy file `main.py`.
3. **Kết Nối Qua Putty**  
   - Mở Putty, thiết lập kết nối **Raw** tới địa chỉ IP mà `main.py` hiển thị khi chạy.
4. **Kết Nối Qua Termux**  
   - Nếu sử dụng Termux, thiết lập kết nối Telnet bằng lệnh:  
     ```
     telnet 0.0.0.0 <port>
     ```
     (Thay `<port>` bằng cổng được hiển thị trong `Main.py`).

## Về Tác Giả & Hỗ Trợ
- **Tác Giả**: `@tretraunetwork`  
- **Lời Cảm Ơn**: Cảm ơn tất cả mọi người đã giúp kênh của tôi đạt 200 thành viên!  
- **Tham Gia Cộng Đồng**: Theo dõi `@tretraunetwork` để nhận thêm nhiều mã nguồn miễn phí và hữu ích.  
- **Hỗ Trợ**: Nếu gặp lỗi hoặc có thắc mắc, liên hệ qua `@tretrauchat`.