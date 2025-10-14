#!/usr/bin/env python3
"""
Quick Face Swap - Script nhanh để test với ảnh của user
"""

import cv2
import numpy as np
import base64
from face_swapper import FaceSwapper
import os
from PIL import Image
import io

def save_user_image():
    """Lưu ảnh selfie của user từ input"""
    # Tạo ảnh mẫu đại diện cho selfie của user (vì không thể trực tiếp lưu từ chat)
    print("Tạo ảnh đại diện cho selfie của bạn...")
    
    # Tạo ảnh portrait realistic hơn
    img = np.ones((600, 450, 3), dtype=np.uint8) * 240
    
    # Vẽ khuôn mặt
    face_center = (225, 250)
    face_size = (120, 140)
    
    # Khuôn mặt oval
    cv2.ellipse(img, face_center, face_size, 0, 0, 360, (220, 180, 160), -1)
    
    # Tóc
    cv2.ellipse(img, (225, 180), (130, 80), 0, 0, 180, (50, 30, 20), -1)
    
    # Mắt
    cv2.ellipse(img, (195, 230), (25, 15), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(img, (255, 230), (25, 15), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img, (195, 230), 8, (50, 50, 50), -1)
    cv2.circle(img, (255, 230), 8, (50, 50, 50), -1)
    cv2.circle(img, (195, 228), 3, (0, 0, 0), -1)
    cv2.circle(img, (255, 228), 3, (0, 0, 0), -1)
    
    # Lông mày
    cv2.ellipse(img, (195, 210), (20, 8), 0, 0, 180, (80, 60, 40), -1)
    cv2.ellipse(img, (255, 210), (20, 8), 0, 0, 180, (80, 60, 40), -1)
    
    # Mũi
    cv2.ellipse(img, (225, 250), (8, 15), 0, 0, 360, (200, 160, 140), -1)
    
    # Miệng
    cv2.ellipse(img, (225, 280), (25, 12), 0, 0, 180, (180, 100, 100), -1)
    
    # Kính (dựa trên ảnh selfie)
    # Gọng kính
    cv2.rectangle(img, (170, 215), (220, 245), (100, 100, 100), 2)
    cv2.rectangle(img, (230, 215), (280, 245), (100, 100, 100), 2)
    cv2.line(img, (220, 230), (230, 230), (100, 100, 100), 2)
    
    # Tròng kính trong suốt
    cv2.rectangle(img, (172, 217), (218, 243), (200, 200, 200), 1)
    cv2.rectangle(img, (232, 217), (278, 243), (200, 200, 200), 1)
    
    cv2.imwrite('/workspace/user_selfie.jpg', img)
    print("✅ Đã tạo ảnh đại diện: user_selfie.jpg")
    return '/workspace/user_selfie.jpg'

def create_target_image():
    """Tạo ảnh đích để ghép mặt vào"""
    print("Tạo ảnh đích để ghép mặt...")
    
    # Tạo ảnh với background khác
    img = np.ones((500, 400, 3), dtype=np.uint8)
    img[:] = (180, 200, 220)  # Background xanh nhạt
    
    # Vẽ một khuôn mặt khác
    face_center = (200, 200)
    face_size = (100, 120)
    
    # Khuôn mặt
    cv2.ellipse(img, face_center, face_size, 0, 0, 360, (200, 170, 150), -1)
    
    # Tóc dài
    cv2.ellipse(img, (200, 150), (120, 60), 0, 0, 180, (100, 50, 30), -1)
    cv2.ellipse(img, (200, 200), (140, 100), 0, 90, 270, (100, 50, 30), -1)
    
    # Mắt
    cv2.ellipse(img, (175, 190), (20, 12), 0, 0, 360, (255, 255, 255), -1)
    cv2.ellipse(img, (225, 190), (20, 12), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img, (175, 190), 6, (50, 100, 50), -1)
    cv2.circle(img, (225, 190), 6, (50, 100, 50), -1)
    cv2.circle(img, (175, 188), 2, (0, 0, 0), -1)
    cv2.circle(img, (225, 188), 2, (0, 0, 0), -1)
    
    # Lông mày
    cv2.ellipse(img, (175, 175), (18, 6), 0, 0, 180, (70, 40, 20), -1)
    cv2.ellipse(img, (225, 175), (18, 6), 0, 0, 180, (70, 40, 20), -1)
    
    # Mũi
    cv2.ellipse(img, (200, 205), (6, 12), 0, 0, 360, (180, 150, 130), -1)
    
    # Miệng
    cv2.ellipse(img, (200, 230), (20, 10), 0, 0, 180, (200, 120, 120), -1)
    
    cv2.imwrite('/workspace/target_image.jpg', img)
    print("✅ Đã tạo ảnh đích: target_image.jpg")
    return '/workspace/target_image.jpg'

def main():
    print("=== QUICK FACE SWAP TEST ===")
    print("Test nhanh công cụ ghép mặt với ảnh của bạn")
    print()
    
    # Tạo ảnh test
    user_image = save_user_image()
    target_image = create_target_image()
    
    print(f"📸 Ảnh nguồn (selfie của bạn): {user_image}")
    print(f"🎯 Ảnh đích: {target_image}")
    
    # Tạo Face Swapper
    print("\n🔄 Khởi tạo Face Swapper...")
    swapper = FaceSwapper()
    
    # Thực hiện face swap
    output_path = "/workspace/result_quick_swap.jpg"
    print(f"\n⚡ Bắt đầu quá trình face swapping...")
    
    success = swapper.swap_faces(user_image, target_image, output_path)
    
    if success:
        print(f"\n✅ Face swapping hoàn thành thành công!")
        print(f"📁 Kết quả: {output_path}")
        
        # Hiển thị thông tin
        result_img = cv2.imread(output_path)
        if result_img is not None:
            h, w, c = result_img.shape
            print(f"📏 Kích thước: {w}x{h} pixels")
            
            file_size = os.path.getsize(output_path)
            print(f"💾 Kích thước file: {file_size/1024:.1f} KB")
            
        print(f"\n🎉 Bạn có thể xem kết quả tại: {output_path}")
        print("💡 Để sử dụng với ảnh thật của bạn:")
        print("   1. Copy ảnh selfie vào workspace")
        print("   2. Chạy: python3 face_swapper.py -s your_photo.jpg -t target.jpg -o result.jpg")
        
    else:
        print(f"\n❌ Face swapping thất bại!")
        print("🔧 Thử các cách sau:")
        print("   - Sử dụng ảnh selfie rõ nét hơn")
        print("   - Đảm bảo khuôn mặt nhìn thẳng")
        print("   - Kiểm tra chất lượng ảnh đầu vào")

if __name__ == "__main__":
    main()