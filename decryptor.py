class DecryptorGIF:
    key_decryptor = '10101010'  # [1, 1, 1, 0, 0, 0]

    def __init__(self, file_name):
        self.file_name = str(file_name)
        self.byte_image = self.read_bytes()
        self.number_current_byte = 13  # c 13 байта начинается палитра

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

    # прверка формата GIF
    def check_format(self):
        format_GIF = ''
        for i in range(6):
            try:
                format_GIF += self.byte_image[i].decode('utf-8', 'strict')
            except ValueError:
                print('ggNeGif')
                return False
        if format_GIF == 'GIF89a':
            print('kaef format')
            return True
        else:
            print('ne rabotaem s takim gif formatom')
            return False

    # определение размера палитры
    def find_size_palette(self):
        int_byte = int.from_bytes(self.byte_image[10], byteorder='big')
        palette_size = int(bin(int_byte)[-3:], 2)
        print(palette_size)
        return palette_size

    # проверим ключ
    def check_key(self):
        size_message = ''
        for i in range(4):
            current_bits = self.byte_to_bits(self.byte_image[self.number_current_byte])[2:]
            length = len(current_bits)
            if length == 1:
                current_bits = '0' + current_bits
            first_bit = current_bits[length - 1]
            second_bit = current_bits[length - 2]
            size_message += second_bit + first_bit
            self.number_current_byte += 1

        if size_message == self.key_decryptor:  # заменить на key_decryptor
            print('key not gey')
            return True
        else:
            print('you are gey')
            return False

    # преобразования битов в текст. т.е. узнаем размер сообщения и само сообщения
    def find_message(self, quantity_bytes):
        message = ''
        for i in range(quantity_bytes):     # !!!один символ в 4 байтах.
            one_symbol = ''
            for j in range(4):
                current_bits = self.byte_to_bits(self.byte_image[self.number_current_byte])[2:]
                length = len(current_bits)
                if length == 1:
                    current_bits = '0' + current_bits
                    length += 1
                first_bit = current_bits[length - 1]
                second_bit = current_bits[length - 2]
                one_symbol += second_bit + first_bit
                self.number_current_byte += 1
            one_symbol = int(one_symbol, 2).to_bytes(1, byteorder='big')
            message += one_symbol.decode('utf-8')
        return message

    @staticmethod
    def byte_to_bits(received_byte):
        bit_send = bin(int.from_bytes(received_byte, byteorder='big'))
        return bit_send


def main():
    decryptor_test = DecryptorGIF(input('имя файла '))
    if not decryptor_test.check_format():
        return
    if not decryptor_test.check_key():
        return
    length_message = int(decryptor_test.find_message(3))  # колличество символов / 4 (1,2,3)
    print(decryptor_test.find_message(length_message))  # длина сообщения (23)


if __name__ == "__main__":
    main()



