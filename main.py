import tkinter as tk
import cv2
import easyocr
from spellchecker import SpellChecker


def capture_image_from_camera():
    # Starting the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise ValueError("Could not open the webcam.")


    ret, frame = cap.read()
    if not ret:
        cap.release()
        raise ValueError("Failed to capture image from webcam.")

    # close camera
    cap.release()

    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Saving the pic in jpg.
    image_path = "captured_image.jpg"
    cv2.imwrite(image_path, gray_image)

    return image_path


def preprocess_image(image):

    return image


def recognize_handwritten_text(image_path, reader):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or unable to load.")
    # Preprocess the image
    preprocessed_image = preprocess_image(image)
    # Perform OCR prediction using EasyOCR reader
    result = reader.readtext(preprocessed_image)
    # Decode the predicted text
    decoded_text = decode_prediction(result)
    return decoded_text


def decode_prediction(prediction):
    decoded_text = ' '.join([res[1] for res in prediction])
    return decoded_text


def correct_spelling(text):
    # start the spellchecker
    spell = SpellChecker()
    # Split the text into words
    words = text.split()
    # Correct spelling of each word
    corrected_words = [spell.correction(word) for word in words]
    corrected_text = ' '.join(corrected_words)
    return corrected_text


def sorted_word(word):
    """Return sorted version of a word."""
    return ''.join(sorted(word))


def find_similar_words(input_word, word_bank):
    sorted_input_word = sorted_word(input_word)

    similar_words = []

    # Compare word bank with input word
    for word in word_bank:
        sorted_word_bank_word = sorted_word(word)

        if sorted_input_word == sorted_word_bank_word:
            similar_words.append(word)

    return similar_words


def test_button_callback():
    try:
        # Capture and save the pic from the camera
        image_path = capture_image_from_camera()
        print(f"Grayscale image captured and saved to {image_path}")
        reader = easyocr.Reader(['en'])
        recognized_text = recognize_handwritten_text(image_path, reader)
        print("Recognized Text:", recognized_text)
        corrected_text = correct_spelling(recognized_text)
        print("Corrected Text:", corrected_text)

        # Read words from a text file and create word bank
        word_bank_file = "D:\\Main Project\\Final Output\\wordstxt\\words.txt"
        with open(word_bank_file, "r") as file:
            word_bank = [word.strip() for word in file.readlines()]
        similar_words_data = {}
        for word in corrected_text.split():
            similar_words = find_similar_words(word, word_bank)
            similar_words_data[word] = similar_words

        # inputing the results into the boxes
        recognized_text_var.set(recognized_text)
        corrected_text_var.set(corrected_text)
        similar_words_var.set(similar_words_data)

    except ValueError as e:
        print(e)


# Create the main window
window = tk.Tk()
window.title("Handwritten Text Recognition")
window_width = 800
window_height = 600
window.geometry(f"{window_width}x{window_height}")


recognized_text_var = tk.StringVar()
corrected_text_var = tk.StringVar()
similar_words_var = tk.StringVar()


font_size = 14
recognized_box = tk.Label(window, text="Recognized Text:", font=("Arial", font_size))
recognized_box.pack()
recognized_text_entry = tk.Entry(window, textvariable=recognized_text_var, width=50, font=("Arial", font_size))
recognized_text_entry.pack()

corrected_box = tk.Label(window, text="Corrected Text:", font=("Arial", font_size))
corrected_box.pack()
corrected_text_entry = tk.Entry(window, textvariable=corrected_text_var, width=50, font=("Arial", font_size))
corrected_text_entry.pack()

similar_words_box = tk.Label(window, text="Similar Words:", font=("Arial", font_size))
similar_words_box.pack()
similar_words_entry = tk.Entry(window, textvariable=similar_words_var, width=50, font=("Arial", font_size))
similar_words_entry.pack()


test_button = tk.Button(window, text="Test", command=test_button_callback, font=("Arial", font_size))
test_button.pack(side=tk.BOTTOM)

window.mainloop()
