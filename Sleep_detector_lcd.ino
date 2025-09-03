#include<LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2);
char incomingData;
void setup() {
  lcd.begin(16,2);
  lcd.backlight();
  Serial.begin(9600);
  lcd.setCursor(0,0);
  

}

void loop() {
  if(Serial.available()>0){
    incomingData = Serial.read();
    if (incomingData == 'A'){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Awake");
      }
      else if(incomingData == 'B')
      {  lcd.clear();
        lcd.setCursor(0,0);
        lcd.print("Sleeping");
      }
      
    }
  

}
