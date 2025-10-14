# Face Swapping Tool - Công cụ ghép mặt chất lượng cao

## Mô tả
Công cụ ghép mặt sử dụng công nghệ computer vision hiện đại để thực hiện face swapping một cách tự nhiên và chất lượng cao.

## Tính năng
- ✅ Detect khuôn mặt tự động
- ✅ Trích xuất facial landmarks (68 điểm)
- ✅ Delaunay triangulation để alignment chính xác
- ✅ Seamless blending để kết quả tự nhiên
- ✅ Hỗ trợ nhiều định dạng ảnh (JPG, PNG, BMP)

## Cài đặt
Các thư viện đã được cài đặt:
```bash
pip install opencv-python dlib face-recognition numpy pillow
```

## Cách sử dụng

### 1. Sử dụng script chính
```bash
python3 face_swapper.py --source ảnh_nguồn.jpg --target ảnh_đích.jpg --output kết_quả.jpg
```

### 2. Sử dụng demo
```bash
python3 demo_face_swap.py
```

### 3. Sử dụng với ảnh của bạn
1. Copy ảnh của bạn vào thư mục `/workspace/`
2. Chạy demo và chọn ảnh từ danh sách
3. Hoặc sử dụng script chính với đường dẫn cụ thể

## Tham số

### Script chính (face_swapper.py)
- `--source` hoặc `-s`: Đường dẫn đến ảnh nguồn (khuôn mặt cần ghép)
- `--target` hoặc `-t`: Đường dẫn đến ảnh đích (ảnh sẽ được ghép mặt)
- `--output` hoặc `-o`: Đường dẫn lưu ảnh kết quả

## Yêu cầu ảnh đầu vào
- **Chất lượng**: Ảnh rõ nét, không bị mờ
- **Khuôn mặt**: Khuôn mặt phải nhìn thấy rõ, không bị che khuất
- **Góc chụp**: Tốt nhất là góc thẳng hoặc nghiêng nhẹ
- **Kích thước**: Tối thiểu 200x200 pixels
- **Định dạng**: JPG, PNG, BMP

## Kết quả
- Ảnh kết quả sẽ có cùng kích thước với ảnh đích
- Khuôn mặt từ ảnh nguồn sẽ được ghép vào ảnh đích một cách tự nhiên
- Màu da và ánh sáng sẽ được điều chỉnh để phù hợp

## Lưu ý
- Công cụ hoạt động tốt nhất với ảnh chân dung rõ nét
- Nếu không detect được khuôn mặt, hãy thử ảnh khác hoặc cải thiện chất lượng ảnh
- Kết quả phụ thuộc vào chất lượng và góc chụp của ảnh đầu vào

## Ví dụ
```bash
# Ghép mặt từ selfie.jpg vào group_photo.jpg
python3 face_swapper.py -s selfie.jpg -t group_photo.jpg -o result.jpg

# Chạy demo với giao diện tương tác
python3 demo_face_swap.py
```

## Troubleshooting
1. **Lỗi "Không detect được khuôn mặt"**:
   - Kiểm tra chất lượng ảnh
   - Đảm bảo khuôn mặt không bị che khuất
   - Thử ảnh với góc chụp khác

2. **Kết quả không tự nhiên**:
   - Sử dụng ảnh có ánh sáng tương tự
   - Đảm bảo kích thước khuôn mặt tương đương

3. **Lỗi thư viện**:
   - Kiểm tra lại việc cài đặt các thư viện
   - Đảm bảo Python version >= 3.7