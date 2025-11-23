
 #include "DHT.h"

 #define DHTPIN 4   //Pino de dados do DHT22
 #define DHTTYPE DHT22

 int sensorSolo = 34; // Onde está o sensor LDR (simulando umidade)
 int bombaPin = 26; // Onde está o LED (simulando bomba)
 int fosforoBtn = 12;
 int potassioBtn = 13;

 DHT dht(DHTPIN, DHTTYPE);

 void setup(){
  Serial.begin(115200);
  pinMode(bombaPin, OUTPUT);
  pinMode(fosforoBtn, INPUT_PULLUP);
  pinMode(potassioBtn, INPUT_PULLUP);
  dht.begin();
 }

 void loop(){
  int solo = analogRead(sensorSolo);
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();

  Serial.print("Umidade do solo");
  Serial.println(solo);
  Serial.print("Temp:");
  Serial.print(temp);
  Serial.print("C-Umidade do ar:");
  Serial.print(umid);
  Serial.println("%");

  if(solo<2000){
    digitalWrite(bombaPin, HIGH);
    Serial.println("Bomba LIGADA");
  }else{
    digitalWrite(bombaPin, LOW);
    Serial.println("Bomba DESLIGADA");
  }

  if(digitalRead(fosforoBtn)==LOW){
    Serial.println("Adicionando FÓSFORO...");
  }

  if(digitalRead(potassioBtn)==LOW){
    Serial.println("Adicionando POTÁSSIO...");
  }

  delay(2000);
 }



