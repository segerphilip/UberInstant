#include <Adafruit_GFX.h>
#include <Adafruit_TFTLCD.h>
//#include <TouchScreen.h>

// Pin settings for Touchscreen
#define LCD_CS 10
#define LCD_CD 11
#define LCD_WR 12
#define LCD_RD 13
#define LCD_RESET A4

// Setting up the Touchscreen
Adafruit_TFTLCD tft(LCD_CS, LCD_CD, LCD_WR, LCD_RD, LCD_RESET);

// Color definitions
#define BLACK           0x0000
#define WHITE           0xFFFF

// Function to get color values from RGB
uint16_t getColor(uint8_t red, uint8_t green, uint8_t blue)
{
  red   >>= 3;
  green >>= 2;
  blue  >>= 3;
  return (red << 11) | (green << 5) | blue;
}

/* GENERAL VARIABLE DEFINITIONS */
int i;
byte buttons[] = {A0, A1, A2, A3};
int waiting_comp = 0;

void setup()
{
    Serial.begin(9600);

    // Buttons
    pinMode(A0, INPUT_PULLUP); // 2
    pinMode(A1, INPUT_PULLUP); // 3               
    pinMode(A2, INPUT_PULLUP); // 4               
    pinMode(A3, INPUT_PULLUP); // 1               

    tft.reset();
    uint16_t identifier = tft.readID();
    tft.begin(identifier);

    Screen_Initiate();

}

void loop()
{
    for( i = 0; i < 4; ++i)
    {
        //Serial.print(analogRead(buttons[i]));
        if ( !waiting_comp && analogRead(buttons[i]) < 400 && i < 3)
        {
            Serial.println(i);
            waiting_comp = 1;
        }
        else if (analogRead(buttons[i] < 400))
        {
            Serial.println("STOP");
            waiting_comp = 0;
        }
    }
    if (waiting_comp)
    {
        String content = "";
        char character;
        while( Serial.available())
        {
            character = Serial.read();
            content.concat(character);
        }
        if (content != "")
        {
            Serial.println(content);
        }
    }

}

void Update_Destination(String dest)
{
}

void Update_Time(int timer)
{
}

void Screen_Initiate( void )
{
    tft.setRotation(1);
    tft.fillScreen(BLACK);
    tft.setTextColor(WHITE); tft.setTextSize(6);
    
    tft.setCursor(0,0);
    tft.println("Uber Instant");
}

