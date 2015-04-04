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
int waiting_init = 0, waiting_time = 0;
int draw_info_init = 0;
String dest;
int car;
String timer = "", price = "", content = "";
char tmp, tmp2;
int get_car = 1;
int waiting_price = 0;

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

    // Check input buttons (1,2,3)
    if ( get_car )
    {
        for (i = 0; i < 3; ++i)
        {
            if (analogRead(buttons[i]) < 400 )
            {
                Serial.println(i);
                car = i;
                get_car = 0;
                waiting_init = 1;
            }
        }
    }

    // Restart Button (4)
    if(analogRead(buttons[3]) < 400 )
    {
        Serial.println("STOP");
        Screen_Initiate();
        waiting_time = 0;
        waiting_init = 0;
        get_car = 1;
    }

    // Get initial information
    if (waiting_init)
    {
        content = "";
        char character;
        int number;
        while(Serial.available())
        {
            character = Serial.read();
            if ( character == '&' )
            {   
                break;
            }
            content.concat(character);
            delay(1);
        }

        if (content != ""){
            waiting_init = 0;
            waiting_price = 1;
        }
    }

    // Update display with price
    if (waiting_price)
    {
        price = "";
        while(Serial.available())
        {
            tmp = Serial.read();
            price.concat(tmp);
            delay(1);
        }
        if (price != ""){
            Draw_Destination(content, car, "00", price);
            waiting_price = 0;
            waiting_time = 1;
        }
    }

    // Update the time on the display
    if (waiting_time)
    {
        String timer = "";
        while( Serial.available())
        {
            tmp = Serial.read();
            timer.concat(tmp);
            delay(1);
        }
        if (timer != "") Update_Time(timer);
    }
}

void Draw_Destination(String dest, int car, String timer, String price)
{
    tft.fillScreen(BLACK);

    // Print the destination to screen
    tft.setCursor(10,10);
    tft.setTextSize(3);
    tft.println(dest);

    // A nice little underline
    tft.fillRect(0, 70, 250, 5, WHITE);

    // Timer
    tft.setCursor(50, 160);
    tft.setTextSize(20);
    tft.println(timer);

    // Minutes
    tft.setCursor(300, 230);
    tft.setTextSize(10);
    tft.println("MIN");

    // Car
    tft.setCursor(10, 80);
    tft.setTextSize(5);
    switch(car)
    {
        case 0: tft.println("uberX"); break;
        case 1: tft.println("uberXL"); break;
        case 2: tft.println("uberBK"); break;
        default: break;
    }   

    // Price
    tft.setTextColor(getColor(20,254,30));
    tft.setCursor(320, 50);
    tft.setTextSize(8);
    tft.print("$");
    tft.println(price);
    tft.setTextColor(WHITE);
}

void Update_Time(String timer)
{
    tft.fillRect(0, 130, 320, 480, BLACK);
    tft.setCursor(50,160);
    tft.setTextSize(20);
    tft.print(timer);

    // Minutes
    tft.setCursor(300, 230);
    tft.setTextSize(10);
    tft.println("MIN");
}

void Screen_Initiate( void )
{
    tft.setRotation(1);
    tft.fillScreen(BLACK);
    tft.setTextColor(WHITE); tft.setTextSize(10);
    
    tft.setCursor(0,50);
    tft.println("Uber");
    tft.setCursor(0, 160);
    tft.println("Instant");
}

