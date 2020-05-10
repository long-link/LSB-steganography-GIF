class EncryptorGIF:
    key_decryptor = [1, 0, 1, 0, 1, 0, 1, 0]    # [1, 1, 1, 0, 0, 0]

    def __init__(self, file_name):
        self.file_name = str(file_name)
        self.byte_image = self.read_bytes()

    def check_format(self):
        format_GIF = ''
        for i in range(6):
            try:
                format_GIF += self.byte_image[i].decode('utf-8', 'strict')
            except ValueError:
                return 21
        if format_GIF == 'GIF89a':  # переместить в другое место
            return True
        else:
            return 22

    def compare_message_size(self, entered_message):
        number_colors = pow(2, self.find_size_palette() + 1)
        max_length_message = number_colors * 3 / 4  # 3/4 потому что два бита(1/4) занимает соообщение
        try:
            if self.find_size_message_bytes(entered_message) < max_length_message:
                return entered_message
            else:
                return False
        except TypeError:
            return False

    def find_size_message_bytes(self, entered_message):
        bytes_size = 0
        for i in range(len(entered_message)):
            message_bits = self.message_to_byte(entered_message[i])[2:]
            while len(message_bits) % 8 != 0:
                message_bits = '0' + message_bits
            mbl = len(message_bits)     # mbl this is message_bits_length
            bytes_size += int(mbl / 8)
        return bytes_size

    def find_size_palette(self):
        int_byte = int.from_bytes(self.byte_image[10], byteorder='big')
        palette_size = int(bin(int_byte)[-3:], 2)
        return palette_size

    # показывает что в картинке в битах. Не нужна. Вспомогательная функция, использовал при кодинге
    def show_bytes_image(self):
        z = 13
        for i in range(20):
            int_byte = int.from_bytes(self.byte_image[z], byteorder='big')
            z += 1

    def insert_decryption_key(self):
        number_current_byte = 13
        for i in range(4):
            current_bits = self.byte_to_bits(self.byte_image[number_current_byte])
            if len(current_bits) == 3:
                current_bits += '0'
            current_bits = current_bits[:-2]
            current_bits += str(self.key_decryptor[i * 2])
            current_bits += str(self.key_decryptor[i * 2 + 1])
            self.byte_image[number_current_byte] = int(current_bits, 2).to_bytes(1, byteorder='big')
            number_current_byte += 1

    def symbol_insertion(self, received_text, number_current_byte):
        for i in range(len(received_text)):
            message_bits = self.message_to_byte(received_text[i])[2:]
            while len(message_bits) % 8 != 0:
                message_bits = '0' + message_bits
            for j in range(4 * int(len(message_bits) / 8)):
                current_image_bits = self.byte_to_bits(self.byte_image[number_current_byte])
                if len(current_image_bits) == 3:
                    current_image_bits += '0'
                current_image_bits = current_image_bits[:-2]
                current_image_bits += message_bits[j * 2]
                current_image_bits += message_bits[j * 2 + 1]
                self.byte_image[number_current_byte] = int(current_image_bits, 2).to_bytes(1, byteorder='big')
                number_current_byte += 1

    @staticmethod
    def byte_to_bits(received_byte):
        bit_send = bin(int.from_bytes(received_byte, byteorder='big'))
        return bit_send

    @staticmethod
    def message_to_byte(received_message):
        binary_message = bin(int.from_bytes(received_message.encode('utf-8'), byteorder='big'))
        return binary_message

    # переводим GIF image в набор байтов
    def read_bytes(self):
        array_bytes = []
        with open(self.file_name, 'rb') as file:
            while True:
                byte = file.read(1)
                if byte:
                    array_bytes.append(byte)
                else:
                    break
        return array_bytes

    def create_new_GIF(self, new_name):
        with open(new_name, "wb") as file:
            for i in self.byte_image:
                file.write(i)


class DecryptorGIF:
    key_decryptor = '10101010'  # [1, 1, 1, 0, 0, 0]

    def __init__(self, file_name):
        self.file_name = str(file_name)
        self.byte_image = self.read_bytes()

    # переводим GIF image в набор байтов
    def read_bytes(self):
        array_bytes = []
        with open(self.file_name, 'rb') as file:
            while True:
                byte = file.read(1)
                if byte:
                    array_bytes.append(byte)
                else:
                    break
        return array_bytes

    def check_format(self):
        format_GIF = ''
        for i in range(6):
            try:
                format_GIF += self.byte_image[i].decode('utf-8', 'strict')
            except ValueError:
                return 21
        if format_GIF == 'GIF89a':
            return True
        else:
            return 22

    def check_key(self):
        size_message = ''
        number_current_byte = 13
        for i in range(4):
            current_bits = self.byte_to_bits(self.byte_image[number_current_byte])[2:]
            length = len(current_bits)
            if length == 1:
                current_bits = '0' + current_bits
            first_bit = current_bits[length - 1]
            second_bit = current_bits[length - 2]
            size_message += second_bit + first_bit
            number_current_byte += 1

        if size_message == self.key_decryptor:
            return True
        else:
            return False

    # преобразования битов в текст. т.е. узнаем размер сообщения и само сообщения
    def find_message(self, quantity_bytes, number_current_byte):
        message = ''
        one_symbol = ''
        quantity_bytes_decoding = 0
        for i in range(quantity_bytes):     # !!!один символ в 4 байтах.
            for j in range(4):
                current_bits = self.byte_to_bits(self.byte_image[number_current_byte])[2:]
                length = len(current_bits)
                if length == 1:
                    current_bits = '0' + current_bits
                    length += 1
                first_bit = current_bits[length - 1]
                second_bit = current_bits[length - 2]
                one_symbol += second_bit + first_bit
                number_current_byte += 1
            quantity_bytes_decoding += 1
            # сделать функцией мб
            if (one_symbol[:1] == '0' and quantity_bytes_decoding == 1) or \
                    (one_symbol[:3] == '110' and quantity_bytes_decoding == 2) or \
                    (one_symbol[:4] == '1110' and quantity_bytes_decoding == 3) or \
                    (one_symbol[:5] == '11110' and quantity_bytes_decoding == 4):
                one_symbol = int(one_symbol, 2).to_bytes(quantity_bytes_decoding, byteorder='big')
                message += one_symbol.decode('utf-8')
                one_symbol = ''
                quantity_bytes_decoding = 0
        return message

    @staticmethod
    def byte_to_bits(received_byte):
        bit_send = bin(int.from_bytes(received_byte, byteorder='big'))
        return bit_send


def decode():
    decryptor_test = DecryptorGIF(input('fileName.gif - '))
    if not decryptor_test.check_format():
        return
    if not decryptor_test.check_key():
        return
    length_message = int(decryptor_test.find_message(3, 17))
    print("hidden message - " + decryptor_test.find_message(length_message, 29))



def encode():
    encryptor_test = EncryptorGIF(input('fileName.gif - '))
    if not encryptor_test.check_format():
        return
    entered_message = encryptor_test.compare_message_size(input('write text message '))  # str()
    if not entered_message:
        return
    encryptor_test.insert_decryption_key()
    length = str(encryptor_test.find_size_message_bytes(entered_message))
    while len(length) != 3:
        length = '0' + length
    encryptor_test.symbol_insertion(length, 17)
    encryptor_test.symbol_insertion(entered_message, 29)
    encryptor_test.create_new_GIF(input('NewFile.gif - '))


if __name__ == "__main__":
    action = input('de/en ')
    if action == 'de':
        decode()
    elif action == 'en':
        encode()