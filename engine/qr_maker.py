

import qrcode
import sys


class QRCodeGenerator():
    def __init__(self, base_url) -> None:
        self._save_path = '.'
        self._base_url = base_url

    def make_code(self, code_number):
        # Create a QR code object with the URL
        qr = qrcode.make(self._base_url+'/'+str(code_number))

        # Save the QR code image with a filename based on the URL
        # Removing special characters from the URL to create a clean filename
        filename = self._base_url.replace("https://", "").replace("http://", "").replace("/", "_").replace(":", "") +str(code_number)+ ".png"
        qr.save(filename, scale=2)

        return(filename)          


if __name__ == '__main__':
	num_args = len(sys.argv)

	if num_args != 2:
		print('You must provide a url for the site you want to qr encode...')
		sys.exit(0)
	else:
		web_url = sys.argv[1]



	qr_generator = QRCodeGenerator(web_url)

	qr_file_name = qr_generator.make_code('')

	print(qr_file_name)