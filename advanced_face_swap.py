#!/usr/bin/env python3
"""
Advanced Face Swap - Phiên bản nâng cao với nhiều face detector
"""

import cv2
import numpy as np
import os

class AdvancedFaceSwapper:
    def __init__(self):
        """Khởi tạo với multiple face detectors"""
        # Haar Cascade
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # DNN Face Detector (more accurate)
        try:
            # Tải DNN model nếu có
            self.net = cv2.dnn.readNetFromTensorflow('opencv_face_detector_uint8.pb', 
                                                   'opencv_face_detector.pbtxt')
            self.use_dnn = True
        except:
            self.use_dnn = False
            print("DNN model không có, sử dụng Haar Cascade")
    
    def detect_faces_haar(self, image):
        """Detect faces sử dụng Haar Cascade"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.05,  # Giảm scale factor để sensitive hơn
            minNeighbors=3,    # Giảm minNeighbors
            minSize=(30, 30),  # Kích thước tối thiểu nhỏ hơn
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces
    
    def detect_faces_dnn(self, image):
        """Detect faces sử dụng DNN"""
        if not self.use_dnn:
            return []
        
        h, w = image.shape[:2]
        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), [104, 117, 123])
        self.net.setInput(blob)
        detections = self.net.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                x1 = int(detections[0, 0, i, 3] * w)
                y1 = int(detections[0, 0, i, 4] * h)
                x2 = int(detections[0, 0, i, 5] * w)
                y2 = int(detections[0, 0, i, 6] * h)
                faces.append([x1, y1, x2-x1, y2-y1])
        
        return np.array(faces)
    
    def detect_faces_contour(self, image):
        """Detect faces bằng cách tìm contour lớn nhất"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Blur để giảm noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Threshold để tìm vùng da
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Tìm contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return []
        
        # Lấy contour lớn nhất
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Tính bounding rectangle
        x, y, w, h = cv2.boundingRect(largest_contour)
        
        # Kiểm tra tỷ lệ hợp lý cho khuôn mặt
        aspect_ratio = w / h
        if 0.5 <= aspect_ratio <= 2.0 and w > 50 and h > 50:
            return np.array([[x, y, w, h]])
        
        return []
    
    def detect_faces_template(self, image):
        """Detect faces bằng template matching với face template đơn giản"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Tạo template khuôn mặt đơn giản
        template = np.zeros((100, 80), dtype=np.uint8)
        
        # Vẽ khuôn mặt template
        cv2.ellipse(template, (40, 50), (35, 45), 0, 0, 360, 200, -1)
        cv2.circle(template, (30, 40), 4, 0, -1)  # Mắt trái
        cv2.circle(template, (50, 40), 4, 0, -1)  # Mắt phải
        cv2.ellipse(template, (40, 65), (10, 5), 0, 0, 180, 0, -1)  # Miệng
        
        # Template matching
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        # Nếu match tốt
        if max_val > 0.3:
            x, y = max_loc
            w, h = template.shape[1], template.shape[0]
            return np.array([[x, y, w, h]])
        
        return []
    
    def detect_faces_adaptive(self, image):
        """Detect faces với adaptive method"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Adaptive histogram equalization
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Multiple scale detection
        faces = []
        
        # Thử nhiều scale factors
        for scale in [1.05, 1.1, 1.15, 1.2]:
            detected = self.face_cascade.detectMultiScale(
                enhanced,
                scaleFactor=scale,
                minNeighbors=2,
                minSize=(20, 20),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            if len(detected) > 0:
                faces.extend(detected)
        
        # Remove duplicates
        if len(faces) > 0:
            faces = np.array(faces)
            # Simple duplicate removal
            unique_faces = []
            for face in faces:
                is_duplicate = False
                for existing in unique_faces:
                    if (abs(face[0] - existing[0]) < 20 and 
                        abs(face[1] - existing[1]) < 20):
                        is_duplicate = True
                        break
                if not is_duplicate:
                    unique_faces.append(face)
            return np.array(unique_faces)
        
        return []
    
    def detect_faces(self, image):
        """Detect faces sử dụng multiple methods"""
        print("🔍 Thử Haar Cascade...")
        faces = self.detect_faces_haar(image)
        if len(faces) > 0:
            print(f"✅ Haar Cascade tìm thấy {len(faces)} khuôn mặt")
            return faces
        
        print("🔍 Thử Adaptive method...")
        faces = self.detect_faces_adaptive(image)
        if len(faces) > 0:
            print(f"✅ Adaptive method tìm thấy {len(faces)} khuôn mặt")
            return faces
        
        if self.use_dnn:
            print("🔍 Thử DNN detector...")
            faces = self.detect_faces_dnn(image)
            if len(faces) > 0:
                print(f"✅ DNN tìm thấy {len(faces)} khuôn mặt")
                return faces
        
        print("🔍 Thử Contour method...")
        faces = self.detect_faces_contour(image)
        if len(faces) > 0:
            print(f"✅ Contour method tìm thấy {len(faces)} khuôn mặt")
            return faces
        
        print("🔍 Thử Template matching...")
        faces = self.detect_faces_template(image)
        if len(faces) > 0:
            print(f"✅ Template matching tìm thấy {len(faces)} khuôn mặt")
            return faces
        
        return []
    
    def create_face_landmarks(self, face_rect):
        """Tạo landmarks từ face rectangle"""
        x, y, w, h = face_rect
        
        # 16 điểm landmarks cho khuôn mặt
        landmarks = np.array([
            # Đường viền khuôn mặt (8 điểm)
            [x, y + h//4],                    # Trái trên
            [x, y + h//2],                    # Trái giữa
            [x, y + 3*h//4],                  # Trái dưới
            [x + w//4, y + h],                # Dưới trái
            [x + w//2, y + h],                # Dưới giữa
            [x + 3*w//4, y + h],              # Dưới phải
            [x + w, y + 3*h//4],              # Phải dưới
            [x + w, y + h//2],                # Phải giữa
            [x + w, y + h//4],                # Phải trên
            [x + 3*w//4, y],                  # Trên phải
            [x + w//2, y],                    # Trên giữa
            [x + w//4, y],                    # Trên trái
            
            # Điểm đặc trưng (4 điểm)
            [x + w//4, y + h//3],             # Mắt trái
            [x + 3*w//4, y + h//3],           # Mắt phải
            [x + w//2, y + h//2],             # Mũi
            [x + w//2, y + 2*h//3],           # Miệng
        ], dtype=np.int32)
        
        return landmarks
    
    def create_seamless_mask(self, image_shape, landmarks):
        """Tạo mask mượt cho blending"""
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        
        # Tạo convex hull
        hull = cv2.convexHull(landmarks)
        cv2.fillPoly(mask, [hull], 255)
        
        # Blur mask để tạo hiệu ứng mượt
        mask = cv2.GaussianBlur(mask, (15, 15), 0)
        
        return mask
    
    def color_transfer(self, source, target, mask):
        """Transfer màu sắc từ target sang source"""
        # Chuyển sang LAB color space
        source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB)
        target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB)
        
        # Tính mean và std của target trong vùng mask
        target_masked = cv2.bitwise_and(target_lab, target_lab, mask=mask)
        
        # Tính statistics
        target_mean = cv2.mean(target_masked, mask=mask)[:3]
        target_std = np.std(target_masked.reshape(-1, 3), axis=0)
        
        source_mean = cv2.mean(source_lab)[:3]
        source_std = np.std(source_lab.reshape(-1, 3), axis=0)
        
        # Color transfer
        result_lab = source_lab.copy().astype(np.float32)
        for i in range(3):
            if source_std[i] > 0:
                result_lab[:,:,i] = (result_lab[:,:,i] - source_mean[i]) * (target_std[i] / source_std[i]) + target_mean[i]
        
        # Clamp values
        result_lab = np.clip(result_lab, 0, 255).astype(np.uint8)
        
        # Convert back to BGR
        return cv2.cvtColor(result_lab, cv2.COLOR_LAB2BGR)
    
    def swap_faces(self, source_path, target_path, output_path):
        """Thực hiện face swapping nâng cao"""
        print(f"📖 Đọc ảnh nguồn: {source_path}")
        source_img = cv2.imread(source_path)
        
        print(f"📖 Đọc ảnh đích: {target_path}")
        target_img = cv2.imread(target_path)
        
        if source_img is None or target_img is None:
            print("❌ Lỗi: Không thể đọc ảnh!")
            return False
        
        # Detect faces
        print("\n🔍 Detecting khuôn mặt trong ảnh nguồn...")
        source_faces = self.detect_faces(source_img)
        
        print("\n🔍 Detecting khuôn mặt trong ảnh đích...")
        target_faces = self.detect_faces(target_img)
        
        if len(source_faces) == 0:
            print("❌ Không tìm thấy khuôn mặt trong ảnh nguồn!")
            return False
            
        if len(target_faces) == 0:
            print("❌ Không tìm thấy khuôn mặt trong ảnh đích!")
            return False
        
        # Sử dụng khuôn mặt đầu tiên
        source_face = source_faces[0]
        target_face = target_faces[0]
        
        print(f"✅ Sử dụng khuôn mặt nguồn: {source_face}")
        print(f"✅ Sử dụng khuôn mặt đích: {target_face}")
        
        # Tạo landmarks
        source_landmarks = self.create_face_landmarks(source_face)
        target_landmarks = self.create_face_landmarks(target_face)
        
        # Extract và resize khuôn mặt
        sx, sy, sw, sh = source_face
        tx, ty, tw, th = target_face
        
        source_face_img = source_img[sy:sy+sh, sx:sx+sw]
        source_face_resized = cv2.resize(source_face_img, (tw, th))
        
        # Tạo mask
        mask = self.create_seamless_mask((th, tw), 
                                       self.create_face_landmarks([0, 0, tw, th]))
        
        # Color transfer
        print("🎨 Điều chỉnh màu sắc...")
        target_roi = target_img[ty:ty+th, tx:tx+tw]
        source_face_colored = self.color_transfer(source_face_resized, target_roi, mask)
        
        # Tạo kết quả
        result = target_img.copy()
        
        # Blend với mask
        mask_3d = cv2.merge([mask, mask, mask]) / 255.0
        
        blended_roi = source_face_colored * mask_3d + target_roi * (1 - mask_3d)
        result[ty:ty+th, tx:tx+tw] = blended_roi.astype(np.uint8)
        
        # Lưu kết quả
        cv2.imwrite(output_path, result)
        print(f"✅ Đã lưu kết quả tại: {output_path}")
        
        return True

def create_realistic_images():
    """Tạo ảnh realistic hơn để test"""
    print("🎨 Tạo ảnh realistic để test...")
    
    # Ảnh nguồn - selfie với kính
    img1 = np.ones((500, 400, 3), dtype=np.uint8)
    
    # Background gradient
    for i in range(500):
        for j in range(400):
            img1[i, j] = [min(255, 200 + i//20), min(255, 210 + j//20), min(255, 220 + i//30)]
    
    # Khuôn mặt oval realistic
    center = (200, 250)
    axes = (90, 110)
    
    # Da mặt với gradient
    for angle in range(360):
        for r in range(110):
            x = int(center[0] + r * np.cos(np.radians(angle)) * axes[0] / 110)
            y = int(center[1] + r * np.sin(np.radians(angle)) * axes[1] / 110)
            if 0 <= x < 400 and 0 <= y < 500:
                shade = 200 - r//3
                img1[y, x] = [shade-20, shade-10, shade]
    
    # Tóc
    cv2.ellipse(img1, (200, 180), (100, 70), 0, 0, 180, (40, 25, 15), -1)
    
    # Mắt với detail
    # Mắt trái
    cv2.ellipse(img1, (175, 230), (20, 12), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img1, (175, 230), 8, (100, 50, 30), -1)
    cv2.circle(img1, (175, 228), 4, (0, 0, 0), -1)
    cv2.circle(img1, (177, 226), 1, (255, 255, 255), -1)
    
    # Mắt phải  
    cv2.ellipse(img1, (225, 230), (20, 12), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img1, (225, 230), 8, (100, 50, 30), -1)
    cv2.circle(img1, (225, 228), 4, (0, 0, 0), -1)
    cv2.circle(img1, (227, 226), 1, (255, 255, 255), -1)
    
    # Lông mày
    cv2.ellipse(img1, (175, 210), (25, 8), 0, 0, 180, (60, 40, 25), -1)
    cv2.ellipse(img1, (225, 210), (25, 8), 0, 0, 180, (60, 40, 25), -1)
    
    # Mũi với shadow
    cv2.ellipse(img1, (200, 250), (8, 20), 0, 0, 360, (180, 150, 130), -1)
    cv2.line(img1, (200, 240), (200, 260), (160, 130, 110), 2)
    
    # Miệng
    cv2.ellipse(img1, (200, 280), (25, 10), 0, 0, 180, (160, 100, 100), -1)
    cv2.line(img1, (180, 280), (220, 280), (120, 70, 70), 2)
    
    # Kính (như selfie gốc)
    # Gọng kính
    cv2.rectangle(img1, (150, 215), (200, 245), (60, 60, 60), 3)
    cv2.rectangle(img1, (200, 215), (250, 245), (60, 60, 60), 3)
    cv2.line(img1, (200, 230), (200, 230), (60, 60, 60), 3)
    
    # Cầu mũi kính
    cv2.line(img1, (195, 230), (205, 230), (60, 60, 60), 2)
    
    # Phản chiếu trên kính
    cv2.rectangle(img1, (155, 220), (195, 240), (220, 220, 220), 1)
    cv2.rectangle(img1, (205, 220), (245, 240), (220, 220, 220), 1)
    
    cv2.imwrite('/workspace/realistic_source.jpg', img1)
    
    # Ảnh đích - người khác
    img2 = np.ones((600, 450, 3), dtype=np.uint8)
    
    # Background khác
    for i in range(600):
        for j in range(450):
            img2[i, j] = [min(255, 150 + j//20), min(255, 170 + i//25), min(255, 190 + j//20)]
    
    # Khuôn mặt khác
    center2 = (225, 300)
    axes2 = (80, 100)
    
    # Da mặt
    for angle in range(360):
        for r in range(100):
            x = int(center2[0] + r * np.cos(np.radians(angle)) * axes2[0] / 100)
            y = int(center2[1] + r * np.sin(np.radians(angle)) * axes2[1] / 100)
            if 0 <= x < 450 and 0 <= y < 600:
                shade = 210 - r//4
                img2[y, x] = [shade-15, shade-5, shade+5]
    
    # Tóc dài
    cv2.ellipse(img2, (225, 230), (100, 60), 0, 0, 180, (80, 50, 30), -1)
    cv2.ellipse(img2, (225, 300), (120, 90), 0, 90, 270, (80, 50, 30), -1)
    
    # Mắt
    cv2.ellipse(img2, (200, 280), (18, 10), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img2, (200, 280), 6, (50, 100, 50), -1)
    cv2.circle(img2, (200, 278), 3, (0, 0, 0), -1)
    
    cv2.ellipse(img2, (250, 280), (18, 10), 0, 0, 360, (255, 255, 255), -1)
    cv2.circle(img2, (250, 280), 6, (50, 100, 50), -1)
    cv2.circle(img2, (250, 278), 3, (0, 0, 0), -1)
    
    # Lông mày
    cv2.ellipse(img2, (200, 265), (20, 6), 0, 0, 180, (70, 45, 30), -1)
    cv2.ellipse(img2, (250, 265), (20, 6), 0, 0, 180, (70, 45, 30), -1)
    
    # Mũi
    cv2.ellipse(img2, (225, 300), (6, 15), 0, 0, 360, (190, 160, 140), -1)
    
    # Miệng
    cv2.ellipse(img2, (225, 320), (20, 8), 0, 0, 180, (170, 110, 110), -1)
    
    cv2.imwrite('/workspace/realistic_target.jpg', img2)
    
    print("✅ Đã tạo ảnh realistic: realistic_source.jpg và realistic_target.jpg")

def main():
    print("=== ADVANCED FACE SWAP ===")
    print("Công cụ ghép mặt nâng cao với multiple detection methods")
    print()
    
    # Tạo ảnh realistic
    create_realistic_images()
    
    source_path = "/workspace/realistic_source.jpg"
    target_path = "/workspace/realistic_target.jpg"
    output_path = "/workspace/advanced_face_swap_result.jpg"
    
    print(f"📸 Ảnh nguồn: {source_path}")
    print(f"🎯 Ảnh đích: {target_path}")
    print(f"💾 Kết quả: {output_path}")
    print()
    
    # Tạo swapper
    swapper = AdvancedFaceSwapper()
    
    # Thực hiện swap
    success = swapper.swap_faces(source_path, target_path, output_path)
    
    if success:
        print("\n🎉 Advanced Face Swapping hoàn thành!")
        
        # Hiển thị thông tin
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"📁 Kích thước file: {file_size/1024:.1f} KB")
            
            result_img = cv2.imread(output_path)
            if result_img is not None:
                h, w, c = result_img.shape
                print(f"📏 Kích thước ảnh: {w}x{h} pixels")
        
        print(f"\n💡 Sử dụng với ảnh thật:")
        print(f"   python3 advanced_face_swap.py source.jpg target.jpg output.jpg")
        
    else:
        print("\n❌ Advanced Face swapping thất bại!")

if __name__ == "__main__":
    if len(os.sys.argv) == 4:
        # Command line usage
        source = os.sys.argv[1]
        target = os.sys.argv[2]
        output = os.sys.argv[3]
        
        swapper = AdvancedFaceSwapper()
        swapper.swap_faces(source, target, output)
    else:
        # Demo mode
        main()