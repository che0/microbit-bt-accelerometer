#include <math.h>
#include <stdlib.h>
#include "MicroBit.h"

MicroBit uBit;
MicroBitAccelerometerService *accelerometerService;

int connected = 0;
int accelerometerDisplay = 0;

static void flashLetter(const char * letter)
{
    uBit.display.print(letter);
    uBit.sleep(400);
    uBit.display.clear();
}

void onConnected(MicroBitEvent)
{

    connected = 1;
    flashLetter("C");
}

void onDisconnected(MicroBitEvent)
{
    connected = 0;
    flashLetter("D");
}


void onAccelerometer(MicroBitEvent)
{
    int x = uBit.accelerometer.getX();
    int y = uBit.accelerometer.getY();
    int z = uBit.accelerometer.getZ();
    double activity = fabs(sqrt(x * x + y * y + z * z) - 1000) / 50;

    for (int px = 0; px < 5; px++) for (int py = 0; py < 5; py++)
    {
        int distanceCu = (px - 2) * (px - 2) + (py - 2) * (py - 2);
        int brightness = activity / ((distanceCu > 0) ? distanceCu : 1);
        uBit.display.image.setPixelValue(px, py, brightness > 255 ? 255 : brightness);
    }
}

void onButtonA(MicroBitEvent)
{
    flashLetter(connected ? "C" : "D");
}

void onButtonB(MicroBitEvent)
{
    if (!accelerometerDisplay) {
        uBit.display.clear();
        for (int i = 0; i < 255; i += 16)
        {
            uBit.display.image.setPixelValue(2, 2, i);
            uBit.sleep(20);
        }
        uBit.messageBus.listen(MICROBIT_ID_ACCELEROMETER, MICROBIT_ACCELEROMETER_EVT_DATA_UPDATE, onAccelerometer);
    }
    else
    {
        uBit.messageBus.ignore(MICROBIT_ID_ACCELEROMETER, MICROBIT_ACCELEROMETER_EVT_DATA_UPDATE, onAccelerometer);
        for (int i = 0; i < 3; i++)
        {
            uBit.display.clear();
            uBit.display.image.setPixelValue(2, 2 + i, 255 - i * 24);
            uBit.sleep(100);
        }
        uBit.display.clear();
    }
    accelerometerDisplay = !accelerometerDisplay;
}

int main()
{
    // Initialise the micro:bit runtime and stuff.
    uBit.init();

    uBit.messageBus.listen(MICROBIT_ID_BLE, MICROBIT_BLE_EVT_CONNECTED, onConnected);
    uBit.messageBus.listen(MICROBIT_ID_BLE, MICROBIT_BLE_EVT_DISCONNECTED, onDisconnected);
    uBit.messageBus.listen(MICROBIT_ID_BUTTON_A, MICROBIT_BUTTON_EVT_CLICK, onButtonA);
    uBit.messageBus.listen(MICROBIT_ID_BUTTON_B, MICROBIT_BUTTON_EVT_CLICK, onButtonB);

    uBit.accelerometer.setPeriod(40);

    accelerometerService = new MicroBitAccelerometerService(*uBit.ble, uBit.accelerometer);

    // Welcome heart
    uBit.display.setDisplayMode(DISPLAY_MODE_BLACK_AND_WHITE);
    uBit.display.setBrightness(0);
    MicroBitImage smiley("0,255,0,255, 0\n255,255,255,255,255\n255,255,255,255,255\n0,255,255,255,0\n0,0,255,0,0\n");
    uBit.display.print(smiley);
    for (int i = 0; i < 5; i++) {
        uBit.display.setBrightness(16 * i);
        uBit.sleep(70);
    }
    for (int i = 0; i < 5; i++) {
        uBit.display.setBrightness(64 - 16 * i);
        uBit.sleep(100);
    }
    uBit.display.clear();
    uBit.display.setBrightness(255);
    uBit.display.setDisplayMode(DISPLAY_MODE_GREYSCALE);

    release_fiber();
}
