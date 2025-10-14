#!/usr/bin/env python3
"""
Demo Face Swap - Script demo để test face swapping
"""

import cv2
import numpy as np
from face_swapper import FaceSwapper
import os

def create_sample_images():
    """Tạo ảnh mẫu để test nếu chưa có ảnh"""
    print("Tạo ảnh mẫu để test...")
    
    # Tạo ảnh đơn giản với hình tròn để test
    img1 = np.ones((400, 400, 3), dtype=np.uint8) * 255
    cv2.circle(img1, (200, 200), 100, (100, 150, 200), -1)  # Khuôn mặt giả
    cv2.circle(img1, (170, 180), 15, (0, 0, 0), -1)  # Mắt trái
    cv2.circle(img1, (230, 180), 15, (0, 0, 0), -1)  # Mắt phải
    cv2.ellipse(img1, (200, 220), (30, 15), 0, 0, 180, (0, 0, 0), 2)  # Miệng
    
    img2 = np.ones((400, 400, 3), dtype=np.uint8) * 200
    cv2.circle(img2, (200, 200), 120, (150, 100, 200), -1)  # Khuôn mặt giả khác
    cv2.circle(img2, (160, 170), 20, (0, 0, 0), -1)  # Mắt trái
    cv2.circle(img2, (240, 170), 20, (0, 0, 0), -1)  # Mắt phải
    cv2.ellipse(img2, (200, 230), (40, 20), 0, 0, 180, (0, 0, 0), 3)  # Miệng
    
    cv2.imwrite('/workspace/sample_face1.jpg', img1)
    cv2.imwrite('/workspace/sample_face2.jpg', img2)
    
    print("Đã tạo ảnh mẫu: sample_face1.jpg và sample_face2.jpg")

def main():
    print("=== DEMO FACE SWAPPING ===")
    print("Công cụ ghép mặt chất lượng cao")
    print()
    
    # Kiểm tra xem có ảnh của user không
    user_image = None
    target_image = None
    
    # Tìm ảnh trong workspace
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    images_found = []
    
    for file in os.listdir('/workspace'):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            images_found.append(file)
    
    print(f"Tìm thấy {len(images_found)} ảnh trong workspace:")
    for i, img in enumerate(images_found):
        print(f"  {i+1}. {img}")
    
    if len(images_found) >= 2:
        print("\nBạn có thể sử dụng các ảnh có sẵn hoặc tạo ảnh mẫu để test.")
        print("Nhập số thứ tự ảnh nguồn (khuôn mặt cần ghép):")
        try:
            source_idx = int(input()) - 1
            user_image = f"/workspace/{images_found[source_idx]}"
        except:
            print("Lựa chọn không hợp lệ, sẽ tạo ảnh mẫu...")
        
        if user_image:
            print("Nhập số thứ tự ảnh đích (ảnh sẽ được ghép mặt):")
            try:
                target_idx = int(input()) - 1
                target_image = f"/workspace/{images_found[target_idx]}"
            except:
                print("Lựa chọn không hợp lệ, sẽ tạo ảnh mẫu...")
    
    # Nếu không có ảnh phù hợp, tạo ảnh mẫu
    if not user_image or not target_image:
        create_sample_images()
        user_image = "/workspace/sample_face1.jpg"
        target_image = "/workspace/sample_face2.jpg"
    
    print(f"\nSử dụng ảnh nguồn: {user_image}")
    print(f"Sử dụng ảnh đích: {target_image}")
    
    # Tạo Face Swapper
    swapper = FaceSwapper()
    
    # Thực hiện face swap
    output_path = "/workspace/result_face_swap.jpg"
    print(f"\nBắt đầu quá trình face swapping...")
    
    success = swapper.swap_faces(user_image, target_image, output_path)
    
    if success:
        print(f"✅ Face swapping hoàn thành!")
        print(f"📁 Kết quả đã được lưu tại: {output_path}")
        
        # Hiển thị thông tin về ảnh kết quả
        result_img = cv2.imread(output_path)
        if result_img is not None:
            h, w, c = result_img.shape
            print(f"📏 Kích thước ảnh kết quả: {w}x{h} pixels")
            
            # Tính kích thước file
            file_size = os.path.getsize(output_path)
            print(f"💾 Kích thước file: {file_size/1024:.1f} KB")
    else:
        print("❌ Face swapping thất bại!")
        print("Có thể do:")
        print("- Không detect được khuôn mặt trong ảnh")
        print("- Chất lượng ảnh không đủ tốt")
        print("- Góc chụp không phù hợp")

if __name__ == "__main__":
    main()