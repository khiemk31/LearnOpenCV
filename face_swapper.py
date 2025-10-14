#!/usr/bin/env python3
"""
Face Swapping Tool - Công cụ ghép mặt chất lượng cao
Sử dụng OpenCV, dlib và face_recognition để thực hiện face swapping tự nhiên
"""

import cv2
import numpy as np
import face_recognition
import dlib
from PIL import Image
import argparse
import os
import sys

class FaceSwapper:
    def __init__(self):
        """Khởi tạo Face Swapper với các detector cần thiết"""
        self.detector = dlib.get_frontal_face_detector()
        # Sử dụng shape predictor để detect facial landmarks
        try:
            # Tải shape predictor model (68 facial landmarks)
            self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        except:
            print("Cảnh báo: Không tìm thấy shape_predictor_68_face_landmarks.dat")
            print("Sẽ sử dụng face_recognition library thay thế")
            self.predictor = None
    
    def get_face_landmarks(self, image):
        """Lấy facial landmarks từ ảnh"""
        # Sử dụng face_recognition để detect landmarks
        face_landmarks_list = face_recognition.face_landmarks(image)
        
        if not face_landmarks_list:
            return None
        
        # Lấy landmarks của khuôn mặt đầu tiên
        landmarks = face_landmarks_list[0]
        
        # Chuyển đổi landmarks thành format numpy array
        points = []
        for feature in ['chin', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 
                       'nose_tip', 'left_eye', 'right_eye', 'top_lip', 'bottom_lip']:
            if feature in landmarks:
                points.extend(landmarks[feature])
        
        return np.array(points, dtype=np.int32)
    
    def get_face_mask(self, image, landmarks):
        """Tạo mask cho khuôn mặt dựa trên landmarks"""
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        
        # Tạo convex hull từ landmarks
        hull = cv2.convexHull(landmarks)
        cv2.fillPoly(mask, [hull], 255)
        
        return mask
    
    def apply_affine_transform(self, src, src_tri, dst_tri, size):
        """Áp dụng affine transformation"""
        # Tính toán affine transform matrix
        warp_mat = cv2.getAffineTransform(np.float32(src_tri), np.float32(dst_tri))
        
        # Áp dụng transformation
        dst = cv2.warpAffine(src, warp_mat, (size[0], size[1]), None, 
                           flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        
        return dst
    
    def warp_triangle(self, img1, img2, t1, t2):
        """Warp triangle từ img1 sang img2"""
        # Tìm bounding rectangle
        r1 = cv2.boundingRect(np.float32([t1]))
        r2 = cv2.boundingRect(np.float32([t2]))
        
        # Offset points by left top corner of the respective rectangles
        t1_rect = []
        t2_rect = []
        t2_rect_int = []
        
        for i in range(0, 3):
            t1_rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
            t2_rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
            t2_rect_int.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
        
        # Get mask by filling triangle
        mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.int32(t2_rect_int), (1.0, 1.0, 1.0), 16, 0)
        
        # Apply warpImage to small rectangular patches
        img1_rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        
        size = (r2[2], r2[3])
        img2_rect = self.apply_affine_transform(img1_rect, t1_rect, t2_rect, size)
        
        img2_rect = img2_rect * mask
        
        # Copy triangular region of the rectangular patch to the output image
        img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] * ((1.0, 1.0, 1.0) - mask)
        img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]] + img2_rect
    
    def delaunay_triangulation(self, points, size):
        """Thực hiện Delaunay triangulation"""
        # Tạo rectangle
        rect = (0, 0, size[0], size[1])
        
        # Tạo subdiv
        subdiv = cv2.Subdiv2D(rect)
        
        # Insert points vào subdiv
        for p in points:
            subdiv.insert((int(p[0]), int(p[1])))
        
        # Lấy triangles
        triangle_list = subdiv.getTriangleList()
        
        # Chuyển đổi triangle list thành indices
        delaunay_tri = []
        
        for t in triangle_list:
            pt = []
            pt.append((int(t[0]), int(t[1])))
            pt.append((int(t[2]), int(t[3])))
            pt.append((int(t[4]), int(t[5])))
            
            # Kiểm tra xem triangle có nằm trong rectangle không
            if self.rect_contains(rect, pt[0]) and self.rect_contains(rect, pt[1]) and self.rect_contains(rect, pt[2]):
                # Tìm index của points
                ind = []
                for j in range(0, 3):
                    for k in range(0, len(points)):
                        if abs(pt[j][0] - points[k][0]) < 1.0 and abs(pt[j][1] - points[k][1]) < 1.0:
                            ind.append(k)
                            break
                
                if len(ind) == 3:
                    delaunay_tri.append((ind[0], ind[1], ind[2]))
        
        return delaunay_tri
    
    def rect_contains(self, rect, point):
        """Kiểm tra xem point có nằm trong rectangle không"""
        if point[0] < rect[0]:
            return False
        elif point[1] < rect[1]:
            return False
        elif point[0] > rect[2]:
            return False
        elif point[1] > rect[3]:
            return False
        return True
    
    def seamless_clone(self, src, dst, mask):
        """Thực hiện seamless cloning để blend tự nhiên"""
        # Tìm center của mask
        center = self.get_mask_center(mask)
        
        # Sử dụng cv2.seamlessClone
        try:
            result = cv2.seamlessClone(src, dst, mask, center, cv2.NORMAL_CLONE)
            return result
        except:
            # Fallback: simple blending
            return self.simple_blend(src, dst, mask)
    
    def get_mask_center(self, mask):
        """Tìm center của mask"""
        moments = cv2.moments(mask)
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
        else:
            # Fallback: center of image
            cy, cx = mask.shape[0] // 2, mask.shape[1] // 2
        
        return (cx, cy)
    
    def simple_blend(self, src, dst, mask):
        """Simple blending method"""
        mask_3d = np.dstack([mask] * 3) / 255.0
        result = src * mask_3d + dst * (1 - mask_3d)
        return result.astype(np.uint8)
    
    def swap_faces(self, source_path, target_path, output_path):
        """Thực hiện face swapping chính"""
        print(f"Đang xử lý: {source_path} -> {target_path}")
        
        # Đọc ảnh
        source_img = cv2.imread(source_path)
        target_img = cv2.imread(target_path)
        
        if source_img is None or target_img is None:
            print("Lỗi: Không thể đọc ảnh!")
            return False
        
        # Chuyển sang RGB cho face_recognition
        source_rgb = cv2.cvtColor(source_img, cv2.COLOR_BGR2RGB)
        target_rgb = cv2.cvtColor(target_img, cv2.COLOR_BGR2RGB)
        
        # Lấy landmarks
        source_landmarks = self.get_face_landmarks(source_rgb)
        target_landmarks = self.get_face_landmarks(target_rgb)
        
        if source_landmarks is None or target_landmarks is None:
            print("Lỗi: Không thể detect khuôn mặt trong một hoặc cả hai ảnh!")
            return False
        
        print(f"Đã detect {len(source_landmarks)} landmarks từ ảnh nguồn")
        print(f"Đã detect {len(target_landmarks)} landmarks từ ảnh đích")
        
        # Tạo mask cho khuôn mặt nguồn
        source_mask = self.get_face_mask(source_img, source_landmarks)
        
        # Thực hiện triangulation
        size = target_img.shape
        triangles = self.delaunay_triangulation(target_landmarks, (size[1], size[0]))
        
        # Tạo ảnh warped
        warped_img = np.copy(target_img).astype(np.float32)
        
        # Warp từng triangle
        for triangle in triangles:
            if len(triangle) == 3:
                # Lấy triangle points
                t1 = [source_landmarks[triangle[0]], source_landmarks[triangle[1]], source_landmarks[triangle[2]]]
                t2 = [target_landmarks[triangle[0]], target_landmarks[triangle[1]], target_landmarks[triangle[2]]]
                
                # Warp triangle
                self.warp_triangle(source_img.astype(np.float32), warped_img, t1, t2)
        
        # Tạo mask cho khuôn mặt đích
        target_mask = self.get_face_mask(target_img, target_landmarks)
        
        # Seamless cloning
        result = self.seamless_clone(warped_img.astype(np.uint8), target_img, target_mask)
        
        # Lưu kết quả
        cv2.imwrite(output_path, result)
        print(f"Đã lưu kết quả tại: {output_path}")
        
        return True

def main():
    parser = argparse.ArgumentParser(description='Face Swapping Tool - Công cụ ghép mặt chất lượng cao')
    parser.add_argument('--source', '-s', required=True, help='Đường dẫn đến ảnh nguồn (khuôn mặt cần ghép)')
    parser.add_argument('--target', '-t', required=True, help='Đường dẫn đến ảnh đích (ảnh sẽ được ghép mặt)')
    parser.add_argument('--output', '-o', required=True, help='Đường dẫn lưu ảnh kết quả')
    
    args = parser.parse_args()
    
    # Kiểm tra file tồn tại
    if not os.path.exists(args.source):
        print(f"Lỗi: Không tìm thấy ảnh nguồn: {args.source}")
        return
    
    if not os.path.exists(args.target):
        print(f"Lỗi: Không tìm thấy ảnh đích: {args.target}")
        return
    
    # Tạo Face Swapper
    swapper = FaceSwapper()
    
    # Thực hiện face swap
    success = swapper.swap_faces(args.source, args.target, args.output)
    
    if success:
        print("✅ Face swapping hoàn thành thành công!")
    else:
        print("❌ Face swapping thất bại!")

if __name__ == "__main__":
    main()