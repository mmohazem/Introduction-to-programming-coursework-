class ImageSteganography:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = self.load_image()
 
    def load_image(self):
        with open(self.image_path, 'rb') as img_file:
            return bytearray(img_file.read())
 
    def save_image(self, output_path):
        with open(output_path, 'wb') as img_file:
            img_file.write(self.image)
 
    def hide_message(self, message):
        message += '\0'  
        message_bytes = message.encode('utf-8')
        message_length = len(message_bytes)
 
       
        header_size = 54
        if message_length * 8 > len(self.image) - header_size:
            raise ValueError("Message is too long to hide in this image.")
 
        for i in range(message_length):
            for j in range(8):
                bit = (message_bytes[i] >> (7 - j)) & 1  
                self.image[header_size + i * 8 + j] = (
                    self.image[header_size + i * 8 + j] & 0xFE  
                ) | bit  
 
 
    def extract_message(self):
        message_bytes = bytearray()
 
        
        header_size = 54
        for i in range((len(self.image) - header_size) // 8):
            byte = 0
            for j in range(8):
                bit = self.image[header_size + i * 8 + j] & 1  
                byte = (byte << 1) | bit  
            if byte == 0:  
                break
            message_bytes.append(byte)
            print(f"Decoded byte {i}: {byte}")  
       
        try:
            return message_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            print(f"Error during decoding: {e}")  
            return "Error decoding the message. It might be corrupted."
 
 
 
if __name__ == "__main__":
    steganography = ImageSteganography(r"C:\Users\bolat\Downloads\sample_640×426.bmp")
 
    action = input("Press (h) to hide a message or (e) to extract a message: ")
    if action.lower() == "h":
        secret_message = input("Enter the message to hide: ")
        steganography.hide_message(secret_message)
        output_path = input("Enter the output path for the modified image: ")
        steganography.save_image(output_path)
        print("Message hidden successfully.")
    elif action.lower() == "e":
        image_path = input("Enter the path to the image to extract the message from: ")
        steganography = ImageSteganography(image_path)  
        extracted_message = steganography.extract_message()
        print("Extracted message:", extracted_message)
 
    else:
        print("Invalid action.")