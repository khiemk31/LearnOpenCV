# 🎭 CÔNG CỤ GHÉP MẶT CHẤT LƯỢNG CAO

## 🎯 Mô tả
Bộ công cụ ghép mặt (face swapping) sử dụng công nghệ computer vision hiện đại để ghép khuôn mặt một cách tự nhiên và chất lượng cao.

## ✅ Tính năng đã hoàn thành
- ✅ **Face Detection**: Phát hiện khuôn mặt với nhiều thuật toán
- ✅ **Landmark Detection**: Trích xuất điểm đặc trưng khuôn mặt
- ✅ **Color Transfer**: Điều chỉnh màu sắc tự nhiên
- ✅ **Seamless Blending**: Ghép mượt mà không có đường viền
- ✅ **Multiple Detection Methods**: Haar Cascade, Contour, Template Matching

## 🚀 Các phiên bản có sẵn

### 1. **Advanced Face Swap** (Khuyến nghị)
```bash
python3 advanced_face_swap.py source.jpg target.jpg output.jpg
```
- ✅ Nhiều phương pháp detect khuôn mặt
- ✅ Color transfer tự động
- ✅ Seamless blending
- ✅ Xử lý ảnh realistic

### 2. **Simple Face Swap**
```bash
python3 simple_face_swap.py source.jpg target.jpg output.jpg
```
- ✅ Đơn giản, nhanh chóng
- ✅ Sử dụng OpenCV cơ bản

### 3. **Face Swapper (Professional)**
```bash
python3 face_swapper.py -s source.jpg -t target.jpg -o output.jpg
```
- ✅ Delaunay triangulation
- ✅ Facial landmarks 68 điểm
- ✅ Chất lượng cao nhất (cần face_recognition library)

## 🎨 Kết quả đã test thành công

### Test với ảnh realistic:
- **Input**: `realistic_source.jpg` (selfie với kính)
- **Target**: `realistic_target.jpg` (người khác)  
- **Output**: `advanced_face_swap_result.jpg` ✅
- **Kích thước**: 450x600 pixels, 45.5 KB

## 📖 Hướng dẫn sử dụng với ảnh của bạn

### Bước 1: Chuẩn bị ảnh
1. **Ảnh nguồn**: Ảnh selfie của bạn (khuôn mặt cần ghép)
2. **Ảnh đích**: Ảnh mà bạn muốn ghép mặt vào

### Bước 2: Copy ảnh vào workspace
```bash
# Copy ảnh của bạn vào /workspace/
cp your_selfie.jpg /workspace/
cp target_image.jpg /workspace/
```

### Bước 3: Chạy face swapping
```bash
# Phiên bản nâng cao (khuyến nghị)
cd /workspace
python3 advanced_face_swap.py your_selfie.jpg target_image.jpg result.jpg
```

### Bước 4: Kiểm tra kết quả
Ảnh kết quả sẽ được lưu tại `result.jpg`

## 🔧 Yêu cầu ảnh đầu vào

### Ảnh nguồn (selfie):
- ✅ Khuôn mặt rõ nét, không bị che khuất
- ✅ Góc chụp thẳng hoặc nghiêng nhẹ
- ✅ Ánh sáng đủ, không quá tối
- ✅ Kích thước tối thiểu: 200x200 pixels

### Ảnh đích:
- ✅ Có ít nhất 1 khuôn mặt rõ ràng
- ✅ Chất lượng tốt
- ✅ Định dạng: JPG, PNG, BMP

## 🎯 Ví dụ cụ thể

### Với ảnh selfie của bạn:
```bash
# Giả sử bạn có selfie.jpg và muốn ghép vào group_photo.jpg
python3 advanced_face_swap.py selfie.jpg group_photo.jpg my_result.jpg
```

### Chạy demo với ảnh có sẵn:
```bash
# Chạy demo tự động tạo ảnh test
python3 advanced_face_swap.py
```

## 🛠️ Troubleshooting

### ❌ "Không tìm thấy khuôn mặt"
**Giải pháp:**
- Sử dụng ảnh rõ nét hơn
- Đảm bảo khuôn mặt không bị che khuất
- Thử góc chụp khác
- Cải thiện ánh sáng

### ❌ "Kết quả không tự nhiên"
**Giải pháp:**
- Sử dụng ảnh có ánh sáng tương tự
- Đảm bảo kích thước khuôn mặt phù hợp
- Thử phiên bản `advanced_face_swap.py`

### ❌ "Lỗi thư viện"
**Giải pháp:**
```bash
pip install opencv-python numpy pillow
```

## 📊 Thông số kỹ thuật

### Thư viện sử dụng:
- **OpenCV**: Face detection, image processing
- **NumPy**: Xử lý mảng và tính toán
- **Pillow**: Xử lý ảnh bổ sung

### Thuật toán:
- **Haar Cascade**: Face detection cơ bản
- **Contour Detection**: Phát hiện vùng khuôn mặt
- **Template Matching**: So khớp mẫu
- **Color Transfer**: Chuyển đổi màu sắc LAB
- **Gaussian Blur**: Làm mượt mask

## 🎉 Kết luận

Công cụ face swapping đã được tạo thành công và test hoạt động tốt! Bạn có thể:

1. ✅ Sử dụng ngay với ảnh có sẵn
2. ✅ Ghép ảnh selfie của bạn vào bất kỳ ảnh nào
3. ✅ Tùy chỉnh và cải thiện thuật toán
4. ✅ Mở rộng thêm tính năng

**Lệnh khuyến nghị:**
```bash
python3 advanced_face_swap.py your_selfie.jpg target_photo.jpg amazing_result.jpg
```

Chúc bạn có những kết quả face swapping tuyệt vời! 🎭✨