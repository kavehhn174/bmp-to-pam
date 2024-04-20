import cv2


def convert_bmp_to_pam():
    input_file = input("Enter input BMP file name: ")
    output_file = input("Enter output PAM file name: ")
    with open(input_file, 'rb') as in_file:
        # Read BMP file headers
        bmp_file_header = bytearray(in_file.read(14))
        bmp_info_header = bytearray(in_file.read(40))

        # Check if the file is a valid BMP
        if bmp_file_header[0:2] != b'BM':
            print("Error: Input file is not a valid BMP file")
            return

        # Extract header information
        width = int.from_bytes(bmp_info_header[4:8], byteorder='little')
        height = int.from_bytes(bmp_info_header[8:12], byteorder='little')
        bits_per_pixel = int.from_bytes(bmp_info_header[14:16], byteorder='little')
        if bits_per_pixel != 24:
            print("Error: Only 24-bit color depth BMP files are supported")
            return

        # Write PAM header
        with open(output_file, 'wb') as out_file:
            pam_header = f'P6\n{width} {height}\n255\n'.encode()
            out_file.write(pam_header)

            # Read and write pixel data
            pixel_data_offset = int.from_bytes(bmp_file_header[10:14], byteorder='little')
            in_file.seek(pixel_data_offset)
            row_padding = (width * 3) % 4 or 0
            for row in range(height - 1, -1, -1):  # Reverse row order
                in_file.seek(pixel_data_offset + row * (width * 3 + row_padding))
                row_data = in_file.read(width * 3)
                out_file.write(row_data)

    print("Conversion complete.")


def show_pam():
    input_file = input("Enter input BMP file name: ")
    # Read the PAM file
    image = cv2.imread(input_file, cv2.IMREAD_UNCHANGED)

    # Check if the image was loaded successfully
    if image is None:
        print("Error: Failed to load the PAM file.")
    else:
        # Display the image
        cv2.imshow("PAM Image", image)
        cv2.waitKey(0)  # Wait for a key press to close the window
        cv2.destroyAllWindows()


def convert_to_pam():
    # Load the BMP image
    bmp_image = cv2.imread("image1.bmp")

    # Check if the image was loaded successfully
    if bmp_image is None:
        print("Error: Failed to load the BMP file.")
    else:
        # Convert the BMP image to PAM format
        pam_image = cv2.imencode(".pam", bmp_image)[1]

        # Save the PAM image to a file
        cv2.imwrite("image1.pam", pam_image)
        print("PAM file saved successfully.")


def main():
    while True:
        choice = input(
            "1. Show the PAM image,\n"
            "2. Convert BMP to PAM using OpenCV \n"
            "3. Convert BMP to PAM without Library \n"
            "q. Quit \n ")

        if choice == '1':
            show_pam()
        elif choice == '2':
            convert_to_pam()
        elif choice == '3':
            convert_bmp_to_pam()
        elif choice.lower() == 'q':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
