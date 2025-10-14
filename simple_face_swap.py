#!/usr/bin/env python3
"""
Simple Face Swap - Phiên bản đơn giản sử dụng OpenCV
"""

import cv2
import numpy as np
import os

class SimpleFaceSwapper:
    def __init__(self):
        """Khởi tạo với OpenCV face detector"""
        # Sử dụng Haar Cascade để detect khuôn mặt
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
    def detect_faces(self, image):
        """Detect khuôn mặt trong ảnh"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
        return faces
    
    def get_face_landmarks_simple(self, image, face_rect):
        """Tạo landmarks đơn giản từ face rectangle"""
        x, y, w, h = face_rect
        
        # Tạo 8 điểm landmarks cơ bản
        landmarks = np.array([
            [x, y],                    # Top-left
            [x + w//2, y],            # Top-center  
            [x + w, y],               # Top-right
            [x + w, y + h//2],        # Right-center
            [x + w, y + h],           # Bottom-right
            [x + w//2, y + h],        # Bottom-center
            [x, y + h],               # Bottom-left
            [x, y + h//2],            # Left-center
        ], dtype=np.int32)
        
        return landmarks
    
    def create_face_mask(self, image, landmarks):
        """Tạo mask cho khuôn mặt"""
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        hull = cv2.convexHull(landmarks)
        cv2.fillPoly(mask, [hull], 255)
        return mask
    
    def resize_and_position_face(self, source_img, source_landmarks, target_landmarks):
        """Resize và position khuôn mặt nguồn để fit với target"""
        # Tính bounding box
        src_x, src_y, src_w, src_h = cv2.boundingRect(source_landmarks)
        tgt_x, tgt_y, tgt_w, tgt_h = cv2.boundingRect(target_landmarks)
        
        # Extract khuôn mặt nguồn
        source_face = source_img[src_y:src_y+src_h, src_x:src_x+src_w]
        
        # Resize để fit target
        resized_face = cv2.resize(source_face, (tgt_w, tgt_h))
        
        return resized_face, (tgt_x, tgt_y, tgt_w, tgt_h)
    
    def blend_faces(self, target_img, source_face, position, mask):
        """Blend khuôn mặt nguồn vào ảnh đích"""
        x, y, w, h = position
        
        # Tạo ảnh kết quả
        result = target_img.copy()
        
        # Đảm bảo không vượt quá boundaries
        x = max(0, x)
        y = max(0, y)
        w = min(w, target_img.shape[1] - x)
        h = min(h, target_img.shape[0] - y)
        
        if w <= 0 or h <= 0:
            return result
        
        # Resize source face và mask
        source_face_resized = cv2.resize(source_face, (w, h))
        mask_resized = cv2.resize(mask, (w, h))
        
        # Tạo mask 3 channels
        mask_3d = cv2.merge([mask_resized, mask_resized, mask_resized]) / 255.0
        
        # Blend
        roi = result[y:y+h, x:x+w]
        blended = source_face_resized * mask_3d + roi * (1 - mask_3d)
        result[y:y+h, x:x+w] = blended.astype(np.uint8)
        
        return result
    
    def swap_faces(self, source_path, target_path, output_path):
        """Thực hiện face swapping"""
        print(f"Đọc ảnh nguồn: {source_path}")
        source_img = cv2.imread(source_path)
        
        print(f"Đọc ảnh đích: {target_path}")
        target_img = cv2.imread(target_path)
        
        if source_img is None or target_img is None:
            print("❌ Lỗi: Không thể đọc ảnh!")
            return False
        
        print("🔍 Detecting khuôn mặt...")
        
        # Detect faces
        source_faces = self.detect_faces(source_img)
        target_faces = self.detect_faces(target_img)
        
        if len(source_faces) == 0:
            print("❌ Không tìm thấy khuôn mặt trong ảnh nguồn!")
            return False
            
        if len(target_faces) == 0:
            print("❌ Không tìm thấy khuôn mặt trong ảnh đích!")
            return False
        
        print(f"✅ Tìm thấy {len(source_faces)} khuôn mặt trong ảnh nguồn")
        print(f"✅ Tìm thấy {len(target_faces)} khuôn mặt trong ảnh đích")
        
        # Sử dụng khuôn mặt đầu tiên
        source_face = source_faces[0]
        target_face = target_faces[0]
        
        # Tạo landmarks
        source_landmarks = self.get_face_landmarks_simple(source_img, source_face)
        target_landmarks = self.get_face_landmarks_simple(target_img, target_face)
        
        # Tạo mask
        source_mask = self.create_face_mask(source_img, source_landmarks)
        
        # Resize và position
        source_face_img, position = self.resize_and_position_face(
            source_img, source_landmarks, target_landmarks
        )
        
        print("🎨 Blending khuôn mặt...")
        
        # Blend faces
        result = self.blend_faces(target_img, source_face_img, position, source_mask)
        
        # Lưu kết quả
        cv2.imwrite(output_path, result)
        print(f"✅ Đã lưu kết quả tại: {output_path}")
        
        return True

def create_test_images():
    """Tạo ảnh test"""
    print("Tạo ảnh test...")
    
    # Ảnh nguồn - selfie style
    img1 = np.ones((400, 300, 3), dtype=np.uint8) * 220
    
    # Vẽ khuôn mặt oval
    cv2.ellipse(img1, (150, 200), (80, 100), 0, 0, 360, (200, 170, 150), -1)
    
    # Tóc
    cv2.ellipse(img1, (150, 140), (90, 60), 0, 0, 180, (60, 40, 20), -1)
    
    # Mắt
    cv2.circle(img1, (125, 180), 8, (0, 0, 0), -1)
    cv2.circle(img1, (175, 180), 8, (0, 0, 0), -1)
    
    # Mũi
    cv2.circle(img1, (150, 200), 3, (180, 150, 130), -1)
    
    # Miệng
    cv2.ellipse(img1, (150, 220), (15, 8), 0, 0, 180, (150, 100, 100), -1)
    
    # Kính (như trong selfie gốc)
    cv2.rectangle(img1, (110, 165), (140, 195), (80, 80, 80), 2)
    cv2.rectangle(img1, (160, 165), (190, 195), (80, 80, 80), 2)
    cv2.line(img1, (140, 180), (160, 180), (80, 80, 80), 2)
    
    cv2.imwrite('/workspace/source_selfie.jpg', img1)
    
    # Ảnh đích - khác style
    img2 = np.ones((450, 350, 3), dtype=np.uint8) * 200
    
    # Background gradient
    for i in range(450):
        img2[i, :] = (180 + i//10, 190 + i//15, 210 + i//20)
    
    # Khuôn mặt khác
    cv2.ellipse(img2, (175, 225), (70, 90), 0, 0, 360, (210, 180, 160), -1)
    
    # Tóc dài
    cv2.ellipse(img2, (175, 170), (85, 50), 0, 0, 180, (100, 60, 40), -1)
    cv2.ellipse(img2, (175, 225), (100, 80), 0, 90, 270, (100, 60, 40), -1)
    
    # Mắt
    cv2.circle(img2, (155, 205), 6, (0, 0, 0), -1)
    cv2.circle(img2, (195, 205), 6, (0, 0, 0), -1)
    
    # Mũi
    cv2.circle(img2, (175, 225), 2, (190, 160, 140), -1)
    
    # Miệng
    cv2.ellipse(img2, (175, 245), (12, 6), 0, 0, 180, (160, 110, 110), -1)
    
    cv2.imwrite('/workspace/target_person.jpg', img2)
    
    print("✅ Đã tạo ảnh test: source_selfie.jpg và target_person.jpg")

def main():
    print("=== SIMPLE FACE SWAP ===")
    print("Công cụ ghép mặt đơn giản sử dụng OpenCV")
    print()
    
    # Tạo ảnh test
    create_test_images()
    
    source_path = "/workspace/source_selfie.jpg"
    target_path = "/workspace/target_person.jpg"
    output_path = "/workspace/simple_face_swap_result.jpg"
    
    print(f"📸 Ảnh nguồn: {source_path}")
    print(f"🎯 Ảnh đích: {target_path}")
    print(f"💾 Kết quả: {output_path}")
    print()
    
    # Tạo swapper
    swapper = SimpleFaceSwapper()
    
    # Thực hiện swap
    success = swapper.swap_faces(source_path, target_path, output_path)
    
    if success:
        print("\n🎉 Face swapping hoàn thành!")
        
        # Hiển thị thông tin file
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"📁 Kích thước file kết quả: {file_size/1024:.1f} KB")
            
            # Đọc và hiển thị thông tin ảnh
            result_img = cv2.imread(output_path)
            if result_img is not None:
                h, w, c = result_img.shape
                print(f"📏 Kích thước ảnh: {w}x{h} pixels")
        
        print(f"\n💡 Hướng dẫn sử dụng với ảnh thật:")
        print(f"   python3 simple_face_swap.py source.jpg target.jpg output.jpg")
        
    else:
        print("\n❌ Face swapping thất bại!")

if __name__ == "__main__":
    if len(os.sys.argv) == 4:
        # Command line usage
        source = os.sys.argv[1]
        target = os.sys.argv[2]
        output = os.sys.argv[3]
        
        swapper = SimpleFaceSwapper()
        swapper.swap_faces(source, target, output)
    else:
        # Demo mode
        main()