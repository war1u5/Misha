import cv2
import pyzed.sl as sl


def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
    init_params.camera_fps = 60  # Set fps at 60

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        exit(1)

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()

    # Prepare new image size to retrieve half-resolution images
    image_size = sl.Resolution(int(zed.get_camera_information().camera_resolution.width / 2),
                               int(zed.get_camera_information().camera_resolution.height / 2))

    # Declare your sl.Mat matrices
    image_zed = sl.Mat(image_size.width, image_size.height, sl.MAT_TYPE.U8_C4)
    key = ' '

    while key != 113:  # for 'q' key
        err = zed.grab(runtime_parameters)
        if err == sl.ERROR_CODE.SUCCESS:
            # Retrieve the left image in sl.Mat
            zed.retrieve_image(image_zed, sl.VIEW.LEFT, resolution=image_size)

            # Get the RGBA image from sl.Mat and convert it to RGB image using cv2
            image_ocv = image_zed.get_data()[:, :, :3]

            # Display the image
            cv2.imshow("ZED Camera", image_ocv)

        key = cv2.waitKey(10)

    # Close the camera
    zed.close()


if __name__ == "__main__":
    main()
