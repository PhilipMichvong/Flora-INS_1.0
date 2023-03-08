import cv2
import numpy as np
import pathlib
import os


def shape_test(img1: str, img2: str) -> bool:

    photo1 = cv2.imread(img1)
    photo2 = cv2.imread(img2)

    if photo1.shape == photo2.shape:
        print("shape of photos are the same, all tests can be conducted")
        return True
    else:
        print("starting to resizing photos..")
        return False


def is_simlar_1(photo1_name: str, photo2_name: str) -> None:

    photo1_dir = pathlib.Path.absolute(
        pathlib.Path(f'.\\{photo1_name}')
    )

    photo2_dir = pathlib.Path.absolute(
        pathlib.Path(f'.\\{photo2_name}')


    )
    # print(type(photo1_dir))
    photo1 = cv2.imread(str(photo1_dir))
    photo2 = cv2.imread(str(photo2_dir))
    # os.path.exists(sonar_path) == True
    if os.path.exists(photo1_name) == True and os.path.exists(photo2_name == True):
        if photo1.shape == photo2.shape:
            print("The image have same size ad chanels")
            differec = cv2.subtract(photo1, photo2)
            b, g, r = cv2.split(differec)

            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                print("The images are completly equal")
            else:
                print("images are not equal")

        # sift algoritm
        sift = cv2.SIFT_create()

        # key points and desc
        kp_1, desc_1 = sift.detectAndCompute(photo1, None)
        kp_2, desc_2 = sift.detectAndCompute(photo2, None)

        # broodforce method, compare 1 to 1 (slower)

        # flan base method, organize desc to make it faster

        index_params = dict(algorithm=0, trees=5)
        search_params = dict()
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # looking for matches

        matches = flann.knnMatch(desc_1, desc_2, k=2)
        # print(len(matches))

        result = cv2.drawMatchesKnn(photo1, kp_1, photo2, kp_2, matches, None)
        # tests
        cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
        cv2.imshow("test1", photo1)
        cv2.imshow("tset2", photo2)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("check if u wrote correct name of photos")


def mse(img1, img2) -> tuple:
    h, w = img1.shape
    diff = cv2.subtract(img1, img2)
    err = np.sum(diff**2)
    mse = err/(float(h*w))
    return mse, diff


def is_simlar_2(img1_dir: str, img2_dir: str) -> None:

    if os.path.exists(img1_dir) == True and os.path.exists(img2_dir == True):
        img1 = cv2.imread(img1_dir)
        img2 = cv2.imread(img2_dir)

        img1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)

        error, diff = mse(img1, img2)
        print("Image matching error between the two images:", error)

        cv2.imshow("difference", diff)

        cv2.waitKey(0)

        cv2.destroyAllWindows()
    else:
        print("check if u wrote correct name of photos")


def menu() -> None:
    if shape_test("test1.png", "test2.png") == True:
        print("")
        print("")
        print("========================== test 1 ==============================")
        print("")
        print("")
        is_simlar_1(photo1_name="test1.png", photo2_name="test2.png")
        print("========================== test 2 ==============================")
        print("")
        print("")
        is_simlar_2("test1.png", "test2.png")
    else:
        print("work in progress...")


if __name__ == "__main__":
    menu()
