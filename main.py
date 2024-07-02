from ImageProcessor import ImageProcessor
from DatabaseHandler import DatabaseHandler
from GUIHandler import GUIHandler

def main():
    # Initialize the image processor with the path to the query image and the Tesseract executable
    image_processor = ImageProcessor(query_image_path='.//images/1411.jpg', tesseract_cmd=r'C:\Program Files\Tesseract-OCR\tesseract.exe')

    # Initialize the database handler with database connection details
    database_handler = DatabaseHandler(host='localhost', database='projet1', user='root', password='')

    # Initialize and run the GUI
    gui_handler = GUIHandler(image_processor, database_handler)
    gui_handler.app.mainloop()

if __name__ == "__main__":
    main()