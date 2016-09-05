#include <SmartMatrix3.h>
#include <EEPROM.h>

#define FIRMWARE_VER 2

namespace CMDTYPE
{
    enum CMDTYPE
    {
        SETUP_DATA = 1,
        PIXEL_DATA = 2,
        BRIGHTNESS = 3,
        GETID      = 4,
        SETID      = 5,
        GETVER	   = 6
    };
}

namespace RETURN_CODES
{
    enum RETURN_CODES
    {
        SUCCESS = 255,
        REBOOT = 42,
        ERROR = 0,
        ERROR_SIZE = 1,
        ERROR_UNSUPPORTED = 2,
        ERROR_PIXEL_COUNT = 3,
        ERROR_BAD_CMD = 4,
    };
}

// Only here so we can retrieve and ignore from BiblioPixel
typedef struct __attribute__((__packed__))
{
    uint8_t type;
    uint16_t pixelCount;
    uint8_t spiSpeed;
} config_t;
config_t config;

#define COLOR_DEPTH 24                  // known working: 24, 48 - If the sketch uses type `rgb24` directly, COLOR_DEPTH must be 24
const uint8_t kMatrixWidth = 128;        // known working: 32, 64, 96, 128
const uint8_t kMatrixHeight = 32;       // known working: 16, 32, 48, 64
const uint8_t kRefreshDepth = 36;       // known working: 24, 36, 48
const uint8_t kDmaBufferRows = 4;       // known working: 2-4, use 2 to save memory, more to keep from dropping frames and automatically lowering refresh rate
const uint8_t kPanelType = SMARTMATRIX_HUB75_32ROW_MOD16SCAN;   // use SMARTMATRIX_HUB75_16ROW_MOD8SCAN for common 16x32 panels
const uint8_t kMatrixOptions = (SMARTMATRIX_OPTIONS_NONE);      // see http://docs.pixelmatix.com/SmartMatrix for options
const uint8_t kBackgroundLayerOptions = (SM_BACKGROUND_OPTIONS_NONE);
const uint8_t kScrollingLayerOptions = (SM_SCROLLING_OPTIONS_NONE);
const uint8_t kIndexedLayerOptions = (SM_INDEXED_OPTIONS_NONE);

SMARTMATRIX_ALLOCATE_BUFFERS(matrix, kMatrixWidth, kMatrixHeight, kRefreshDepth, kDmaBufferRows, kPanelType, kMatrixOptions);
SMARTMATRIX_ALLOCATE_BACKGROUND_LAYER(backgroundLayer, kMatrixWidth, kMatrixHeight, COLOR_DEPTH, kBackgroundLayerOptions);

#define numLEDs (kMatrixWidth * kMatrixHeight)
#define bytesPerPixel 3
#define packSize (numLEDs * bytesPerPixel)

// rgb24 * _LEDS;

void setup()
{
    pinMode(13, OUTPUT);
    Serial.begin(1000000);
    Serial.setTimeout(10);

    matrix.addLayer(&backgroundLayer);
    matrix.begin();

    backgroundLayer.setBrightness(255);

    backgroundLayer.fillScreen({0,0,0});
    backgroundLayer.enableColorCorrection(true);

    backgroundLayer.swapBuffers();
}

#define EMPTYMAX 100
inline void getData()
{
    static char cmd = 0;
    static uint16_t size = 0;
    static uint16_t count = 0;
    static uint8_t emptyCount = 0;
    static size_t c = 0;

    static uint8_t _buf[packSize];

    if (Serial.available())
    {
        cmd = Serial.read();
        size = 0;
        Serial.readBytes((char*)&size, 2);

        if (cmd == CMDTYPE::PIXEL_DATA)
        {
            count = 0;
            emptyCount = 0;
            rgb24 *buffer = backgroundLayer.backBuffer();

            if (size == packSize)
            {
                while (count < packSize)
                {
                    c = Serial.readBytes(((char*)_buf) + count, packSize - count);
                    //c = Serial.readBytes(((char*)buffer) + count, packSize - count);
                    if (c == 0)
                    {
                        emptyCount++;
                        if(emptyCount > EMPTYMAX) break;
                    }
                    else
                    {
                        emptyCount = 0;
                    }

                    count += c;
                }
            }

            uint8_t resp = RETURN_CODES::SUCCESS;
            if (count == packSize)
            {
                memcpy(buffer, _buf, packSize);
                backgroundLayer.swapBuffers(false);
            }
            else {
                resp = RETURN_CODES::ERROR_SIZE;
            }
            Serial.write(resp);
        }
        else if(cmd == CMDTYPE::GETID)
        {
            Serial.write(EEPROM.read(16));
        }
        else if(cmd == CMDTYPE::SETID)
        {
            if(size != 1)
            {
                Serial.write(RETURN_CODES::ERROR_SIZE);
            }
            else
            {
                uint8_t id = Serial.read();
                EEPROM.write(16, id);
                Serial.write(RETURN_CODES::SUCCESS);
            }
        }
        else if (cmd == CMDTYPE::SETUP_DATA)
        {
            uint8_t result = RETURN_CODES::SUCCESS;
            config_t temp;

            if (size != sizeof(config_t))
            {
                result = RETURN_CODES::ERROR_SIZE;
            }
            else
            {
                size_t read = Serial.readBytes((char*)&temp, sizeof(config_t));
                if (read != size)
                {
                    result = RETURN_CODES::ERROR_SIZE;
                }
                else
                {
                    temp.pixelCount = temp.pixelCount / bytesPerPixel;

                    if(temp.pixelCount != numLEDs){
                        result = RETURN_CODES::ERROR_PIXEL_COUNT;
                    }

                    //On config we reset the brightness.
                    //Otherwise previous brightness values could
                    //still be in memory.
                    backgroundLayer.setBrightness(255);
                }
            }

            Serial.write(result);
        }
        else if (cmd == CMDTYPE::BRIGHTNESS)
        {
            uint8_t result = RETURN_CODES::SUCCESS;
            if (size != 1)
                result = RETURN_CODES::ERROR_SIZE;
            else
            {
                uint8_t brightness = 255;
                size_t read = Serial.readBytes((char*)&brightness, 1);
                if (read != size)
                    result = RETURN_CODES::ERROR_SIZE;
                else
                {
                    backgroundLayer.setBrightness(brightness);
                }
            }

            Serial.write(result);
        }
        else if (cmd == CMDTYPE::GETVER)
        {
            Serial.write(RETURN_CODES::SUCCESS);
            Serial.write(FIRMWARE_VER);
        }
        else
        {
            Serial.write(RETURN_CODES::ERROR_BAD_CMD);
        }


        Serial.flush();
    }
}

void loop()
{
    getData();
}
