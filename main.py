import Decoder
import SoundGen

a = "hello"
a = Decoder.string_to_binary(a)
print(a)
print(Decoder.binary_string_to_text(a))
SoundGen.sound_speaker(SoundGen.bin_to_sound(a))