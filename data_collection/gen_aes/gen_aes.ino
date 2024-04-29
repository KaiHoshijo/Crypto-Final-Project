#include "Crypto.h"
#include "RNG.h"
#include "TransistorNoiseSource.h"
#include "CBC.h"
#include "AES.h"

// Number of times to generate and encrypt plaintext
#define COUNT 1000

TransistorNoiseSource noise(A1);
CBC<AESTiny128> cbc;
byte key[16] = {0xA2,0xD6,0xBF,0x5A,0x35,0xA1,0x38,0x66,0x6f,0x24,0xC0,0x9C,0x50,0xAE,0xFC,0x43};
byte iv[16] = {0xD7,0xB3,0x00,0x8E,0xE1,0xFD,0x8A,0x05,0xC7,0x5D,0x30,0x4D,0x36,0xA6,0x45,0xBB};

void setup() {
  // Creating the RNG class
  RNG.begin("Crypto Final Project");
  RNG.addNoiseSource(noise);
  // Generating the key
  // RNG.rand(key, sizeof(key));
  // RNG.rand(iv, sizeof(iv));
  cbc.setKey(key, sizeof(key));
  cbc.setIV(iv, sizeof(iv));
  // Setting A2 to digital to trigger in AES128 right after the subbytes
  pinMode(A2, OUTPUT);
  Serial.begin(9600);
  // Output the key
  Serial.print("key ");
  for (uint8_t i = 0; i < 16; i++) {
    Serial.print(key[i], HEX);
    Serial.print(' ');
  }
  Serial.println();
  // Output the iv
  Serial.print("iv ");
  for (uint8_t i = 0; i < 16; i++) {
    Serial.print(iv[i], HEX);
    Serial.print(' ');
  }
  Serial.print('\n');
}

void loop() {
  RNG.loop();
  byte input[16];
  byte output[16];
  for (uint16_t i = 0; i < COUNT; i++) {
    // Wait until the oscope code sends the command to run
    while (!Serial.available());
    String incoming = Serial.readString();
    // Generate the plaintext
    RNG.rand(input, sizeof(input));
    // Output the newly generated plaintext
    Serial.print("input ");
    for (uint8_t j = 0; j < 16; j++) {
      Serial.print(input[j], HEX);
      Serial.print(' ');
    }
    Serial.println();
    // Encrypting the plaintext using aes-cbc
    cbc.encrypt(output, input, sizeof(input));
    // Set the pin set in the aes-cbc code to low
    digitalWrite(A2, LOW);
  }
  // Idle once the 255 waves are retrieved
  for(;;);
}