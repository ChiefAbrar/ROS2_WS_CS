#define LED_PIN 13
void setup()
{
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    int valueA = random(-100, 101);
    float valueB = random(-100, 101) / 100.0;
    int valueC = random(0, 1024);
    String valueD = "Henlo";
    Serial.print(valueA);
    Serial.print(',');
    Serial.print(valueB);
    Serial.print(',');
    Serial.print(valueC);
    Serial.print(',');
    Serial.println(valueD);
    delay(200);

    if (Serial.available())
    {
        char c = Serial.read();
        if (c == '1')
            digitalWrite(LED_PIN, HIGH);
        if (c == '0')
            digitalWrite(LED_PIN, LOW);
    }
}