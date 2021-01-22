from termcolor import colored, cprint
import time
from GPIOSimulator_v1 import *
GPIO = GPIOSimulator()

MORSE_CODE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
              '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
              '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
              '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
              '---..': '8', '----.': '9', '-----': '0'}

class MorseDecoder():

    def create_decoded(self, key):
        temp = ''
        for e in key:
            if e == '.':
                temp+='0'
            else:
                temp+='1'
        return temp

    def count_symbols(self, symbol, signal):
        counter = 0
        temp = 0
        for i in signal:
            if i == str(symbol):
                temp += 1
            else:
                temp = 0
            if temp > counter:
                counter = temp
        return counter

    def __init__(self):
        self.decoded = {self.create_decoded(key): value for key, value in MORSE_CODE.items()}
        self.reset()

        self.BASE_TIME = 0.9

        GPIO.setup(PIN_BTN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(PIN_RED_LED_0, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_RED_LED_1, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_RED_LED_2, GPIO.OUT, GPIO.LOW)
        GPIO.setup(PIN_BLUE_LED, GPIO.OUT, GPIO.LOW)

    def reset(self):
        self.current_signal = ''
        self.current_stream = ''
        self.current_symbol = ''
        self.current_word = ''
        self.current_sentence = ''
        self.switch = 0
        self.switch_2 = 1
    
    def read_one_signal(self):
        if keyboard.is_pressed('space'):
            GPIO.pin_states[PIN_BTN] = GPIO.PUD_DOWN
            self.switch = 1
        else:
            GPIO.pin_states[PIN_BTN] = GPIO.PUD_UP
        return GPIO.input(PIN_BTN)
            

    def decoding_loop(self):
        while True:
            signal = self.read_one_signal()
            if  signal == GPIO.PUD_DOWN:
                self.process_signal(signal)
            elif signal == GPIO.PUD_UP:
                self.process_signal(signal)
            time.sleep(self.BASE_TIME)

    def process_signal(self, signal):
        if self.switch:
            self.current_signal += str(signal)
            """print(self.current_signal)"""
            if len(self.current_signal) > 1:
                if self.count_symbols(0, self.current_signal[:-1]) >= 7 and self.current_signal[-1] == '1':
                    self.process_symbol(self.current_signal[:-1])
                    self.current_signal = self.current_signal[-1]
                    self.handle_word_end()
                if self.count_symbols(0, self.current_signal[:-1]) == 3 and self.current_signal[-1] == '1':
                    self.process_symbol(self.current_signal[:-1])
                    self.current_signal = self.current_signal[-1]
                    self.handle_symbol_end()
            self.show_message()
                
            

    def process_symbol(self, symbol):
        temp_2 = symbol.split('0')
        temp_2 = list(filter(lambda item: item, temp_2))
        for e in temp_2:                       
            counter = self.count_symbols(1, e)
            if counter == 3:
                self.current_stream += '1'
            elif counter == 1:
                self.current_stream += '0'
            else:
                message = '\nInvalid length of press: {} seconds'.format(counter*self.BASE_TIME)
                cprint(message, 'red', attrs=['bold'], file=sys.stderr)
                raise KeyboardInterrupt
        for i in self.current_stream:
            self.update_current_symbol(i)
        try:
            self.current_word += self.decoded[self.current_symbol]
        except KeyError:
            cprint('Your input is invalid!', 'red', attrs=['bold'], file=sys.stderr)
            raise KeyboardInterrupt
        
        self.current_stream = ''
        

    def update_current_symbol(self, signal):
        self.current_symbol += signal

    def handle_symbol_end(self):
        self.current_symbol = ''

    def handle_word_end(self):
        self.handle_symbol_end()
        self.current_sentence += self.current_word + ' '
        self.current_word = ''

    def show_message(self):
            message = 'Current signal: {}'.format(self.current_signal)
            message2 = 'Current word: {}'.format(self.current_word)
            message3 = 'Current sentence: {} \r'.format(self.current_sentence)
            print(colored(message, 'cyan', attrs=['reverse', 'blink']), colored(message2, 'green'), colored(message3, 'blue'), end = ' \r')

def main():
    try:
        M_decoder = MorseDecoder()
        M_decoder.decoding_loop()
    except KeyboardInterrupt:
        show_error_and_exit(colored('\nProgram terminated', 'red'))
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()
