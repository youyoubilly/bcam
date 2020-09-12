import numpy as np
import imutils
import cv2

class Stitcher(object):
    
    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        # 发现特征点并解构
        # local invariant descriptors from them
        (imageA, imageB, imageC) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)
        (kpsC, featuresC) = self.detectAndDescribe(imageC)

        # 匹配特征点
        M_AB = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)
        M_AC = self.matchKeypoints(kpsA, kpsC, featuresA, featuresC, ratio, reprojThresh)

        # if the match is None, then there aren't enough matched
        # keypoints to create a panorama
        if M_AB is None:
            return None

        if M_AC is None:
            return None

        # otherwise, apply a perspective warp to stitch the images
        # together
        hA, wA = imageA.shape[:2]
        hB, wB = imageB.shape[:2]
        hC, wC = imageB.shape[:2]

        (matches_AB, H_AB, status_AB) = M_AB
        (matches_AC, H_AC, status_AC) = M_AC

        result_AB = cv2.warpPerspective(imageB, H_AB, (wA, hA))

        result_AC = cv2.warpPerspective(imageC, H_AC, (wA, hA))

        overlapping = cv2.addWeighted(result_AB, 0.5, result_AC, 0.5, 0)
        overlapping = cv2.addWeighted(overlapping, 0.5, imageA, 0.5, 0)

        return overlapping
    
    
    def detectAndDescribe(self, image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 从图片提取关键特征
        descriptor = cv2.xfeatures2d.SIFT_create()
        (kps, features) = descriptor.detectAndCompute(image, None)

        # 将关键点转换乘numpy array
        kps = np.float32([kp.pt for kp in kps])

        # 返回关键点和特征
        return (kps, features)
    

    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        # compute the raw matches and initialize the list of actual
        # matches

        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []

        for m in rawMatches:
            # 确保相应特征点直接的距离在一定范围以内
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        # 确保最少有4个特征点
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])

            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsB, ptsA, cv2.RANSAC, reprojThresh)

            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, H, status)

        # otherwise, no homograpy could be computed
        return None