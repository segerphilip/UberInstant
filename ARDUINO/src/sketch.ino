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
byte buttons[] = {A2, A3, A0, A1};
int waiting_comp = 0;
int draw_info_init = 0;
String dest;
int car = 0, timer = 0, price = 0;

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
        if ( !waiting_comp && analogRead(buttons[i]) < 400 && i != 3)
        {
            Serial.println(i);
            waiting_comp = 1;
        }
        else if( i == 3 && analogRead(buttons[i]) < 400 )
        {
            Serial.println("STOP");
            waiting_comp = 0;
        }
    }
    if (waiting_comp)
    {
        String content = "";
        char character;
        int number;
        int stringer = 1;
        while( Serial.available())
        {
            if (stringer = 1){
                character = Serial.read();
                if ( character != '&' )
                {
                    content.concat(character);
                }
                else
                {
                    stringer = 0; 
                    Serial.println("CONTAINS KILLER");
                }
            }
            //car = Serial.read();
            //timer = Serial.read();
            //price = Serial.read();
        }
        if (content != "" && draw_info_init == 0)
        {
            dest = content;
            Draw_Destination(dest, car, timer, price);
            draw_info_init = 1;
        }
    }
}

void Draw_Destination(String dest, int car, int timer, int price)
{
    tft.fillScreen(BLACK);

    // Print the destination to screen
    tft.setCursor(10,10);
    tft.setTextSize(3);
    tft.println(dest);

    // A nice little underline
    tft.fillRect(0, 70, 250, 5, WHITE);

    // Print that fuckin Time ya
    tft.setCursor(100, 160);
    tft.setTextSize(20);
    tft.println(timer);

    // Minutes
    tft.setCursor(300, 230);
    tft.setTextSize(10);
    tft.println("MIN");

    // Car
    tft.setCursor(330, 10);
    tft.setTextSize(5);
    switch(car)
    {
        case 0: tft.println("uberX"); break;
        case 1: tft.println("uberXL"); break;
        case 2: tft.println("uberBK"); break;
        default: break;
    }   

    // Price
    tft.setCursor(350, 70);
    tft.setTextSize(8);
    tft.println("$");
    tft.setCursor(400, 70);
    tft.println(price);
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

