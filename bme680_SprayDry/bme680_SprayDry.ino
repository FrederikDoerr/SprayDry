/***************************************************************************
  This is a library for the BME680 gas, humidity, temperature & pressure sensor

  Designed specifically to work with the Adafruit BME680 Breakout
  ----> http://www.adafruit.com/products/3660

  These sensors use I2C or SPI to communicate, 2 or 4 pins are required
  to interface.

  Adafruit invests time and resources providing this open source code,
  please support Adafruit and open-source hardware by purchasing products
  from Adafruit!

  Written by Limor Fried & Kevin Townsend for Adafruit Industries.
  Adapted by Frederik Doerr (CMAC, frederik.doerr@strath.ac.uk, GitHub: https://github.com/frederik-d)
  BSD license, all text above must be included in any redistribution
 ***************************************************************************/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme680; // I2C
//Adafruit_BME680 bme(BME_CS); // hardware SPI
//Adafruit_BME680 bme(BME_CS, BME_MOSI, BME_MISO,  BME_SCK);

void setup() {
  Serial.begin(9600);
  while (!Serial);
  // Serial.println(F("BME680 SprayDryer Outlet Sensor >>> Connected <<<\n\n\n"));

  if (!bme680.begin()) {
    Serial.println("Device error!");
    while (1);
  }

  // Set up oversampling and filter initialization
  bme680.setTemperatureOversampling(BME680_OS_8X);
  bme680.setHumidityOversampling(BME680_OS_2X);
  bme680.setPressureOversampling(BME680_OS_4X);
  bme680.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme680.setGasHeater(320, 150); // 320*C for 150 ms
}

void loop() {
  if (! bme680.performReading()) {
    Serial.println("Failed to perform reading :(");
    return;
  }
  Serial.print("T_C;"); Serial.print(bme680.temperature); Serial.print(";");
  Serial.print("RH_%;"); Serial.print(bme680.humidity); Serial.print(";");
  Serial.print("VOC_Ohms;"); Serial.print(bme680.gas_resistance); Serial.print(";");
  Serial.print("P_Pa;"); Serial.print(bme680.pressure); Serial.print("\n");
  
  delay(1000);

}
