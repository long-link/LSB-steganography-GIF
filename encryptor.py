import os    # для указания пути, так проще))
             # в принципе уйдет с интерфейсом


class EncryptorGIF:
    # все переделать под интерфейс
    key_decryptor = [1, 0, 1, 0, 1, 0, 1, 0]    # [1, 1, 1, 0, 0, 0]

    def __init__(self, file_name):
        self.file_name = str(file_name)
        self.byte_image = self.read_bytes()
        self.number_current_byte = 13  # c 13 байта начинается палитра

    # прверка формата GIF
    def check_format(self):
        format_GIF = ''
        for i in range(6):
            try:
                format_GIF += self.byte_image[i].decode('utf-8', 'strict')
            except ValueError:
                print('ggNeGif')
                return False
        if format_GIF == 'GIF89a':  # переместить в другое место
            print('kaef format')
            return True
        else:
            print('ne rabotaem s takim gif formatom')
            return False

    # подходит ли сообщение под максимальную длинну
    def compare_message_size(self, entered_message):
        number_colors = pow(2, self.find_size_palette() + 1)
        max_length_message = number_colors * 3 / 4  # 3/4 потому что два бита(1/4) занимает соообщение
        print(len(entered_message))
        if len(entered_message) < max_length_message:
            print('good size')
            return entered_message
        else:
            print('no good')
            return False

    # определение размера палитры
    def find_size_palette(self):
        int_byte = int.from_bytes(self.byte_image[10], byteorder='big')
        palette_size = int(bin(int_byte)[-3:], 2)
        print(palette_size)
        return palette_size

    # показывает что в картинке в битах. Не нужна. Вспомогательная функция, использовал при кодинге
    def show_bytes_image(self):
        z = 13
        for i in range(20):
            int_byte = int.from_bytes(self.byte_image[z], byteorder='big')
            print(f"raw({self.byte_image[z]}) - int({int_byte}) - binary({bin(int_byte)})")
            z += 1

    # нужно реализовать три шага. 1) вставка ключа: 2)вставка размера сообщения: 3)вставка самого сообщения
    # 1)вставка ключа
    def insert_decryption_key(self):
        for i in range(4):
            current_bits = self.byte_to_bits(self.byte_image[self.number_current_byte])
            # current_bits = bin(int.from_bytes(self.byte_image[self.number_current_byte], byteorder='big'))
            # тоже самое только без доп.функц
            if len(current_bits) == 3:
                current_bits += '0'
            current_bits = current_bits[:-2]
            current_bits += str(self.key_decryptor[i * 2])
            current_bits += str(self.key_decryptor[i * 2 + 1])
            self.byte_image[self.number_current_byte] = int(current_bits, 2).to_bytes(1, byteorder='big')
            self.number_current_byte += 1

    # 2-3)вставка самого сообщения
    def symbol_insertion(self, received_text):
        for i in range(len(received_text)):
            message_bits = self.message_to_byte(received_text[i])[2:]
            while len(message_bits) != 8:
                message_bits = '0' + message_bits
            for j in range(4):
                current_image_bits = self.byte_to_bits(self.byte_image[self.number_current_byte])
                if len(current_image_bits) == 3:
                    current_image_bits += '0'
                current_image_bits = current_image_bits[:-2]
                current_image_bits += message_bits[j * 2]
                current_image_bits += message_bits[j * 2 + 1]
                self.byte_image[self.number_current_byte] = int(current_image_bits, 2).to_bytes(1, byteorder='big')
                self.number_current_byte += 1

    # функция преревода byte в bit. Можно брать если будет вызываться только в одном месте
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

    # создания картинки с зашифрованным текстом
    def create_new_GIF(self, new_name):
        with open(os.path.join("C:\\Users\\evgen\\PycharmProjects\\steganographyGIF", new_name + ".gif"), "wb") as file:
            for i in self.byte_image:
                file.write(i)


def main():
    encryptor_test = EncryptorGIF(input('имя файла '))
    if not encryptor_test.check_format():
        return
    entered_message = encryptor_test.compare_message_size(input('введите текст сообщения '))  # str()
    if not entered_message:
        return
    encryptor_test.insert_decryption_key()
    length = str(len(entered_message))
    while len(length) != 3:
        length = '0' + length
    encryptor_test.symbol_insertion(length)
    encryptor_test.symbol_insertion(entered_message)
    encryptor_test.create_new_GIF(input('имя нового файла '))


if __name__ == "__main__":
    main()
