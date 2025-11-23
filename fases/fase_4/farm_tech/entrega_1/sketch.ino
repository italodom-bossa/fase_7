#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "DHT.h"

// --- Definição de Pinos ---
// Uso de 'constexpr uint8_t' para economizar memória RAM (ocupa apenas 1 byte)
constexpr uint8_t PINO_FOSFORO = 14;
constexpr uint8_t PINO_POTASSIO = 4;
constexpr uint8_t PINO_LDR = 36;
constexpr uint8_t PINO_DHT = 5;
constexpr uint8_t PINO_RELE = 18;

// --- Sensor DHT ---
#define DHTTYPE DHT22
DHT dht(PINO_DHT, DHTTYPE);

// --- LCD I2C ---
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Display LCD 16x2 padrão com I2C

// --- Variáveis Globais ---
// Utilização de tipos otimizados para economia de RAM no ESP32
bool fosforo = false;                 // bool ocupa apenas 1 byte
bool potassio = false;
float umidade = 0.0f;                // 'float' necessário para leitura com casas decimais
float ph = 7.0f;
bool bombaLigada = false;

void setup() {
  Serial.begin(115200);

  // Configuração de pinos com pull-up interno reduz consumo
  pinMode(PINO_FOSFORO, INPUT_PULLUP);
  pinMode(PINO_POTASSIO, INPUT_PULLUP);
  pinMode(PINO_RELE, OUTPUT);

  dht.begin();

  // Inicialização do barramento I2C (padrão ESP32 SDA=21, SCL=22)
  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Iniciando...");
  delay(1000);
}

// --- Função: Simula leitura de pH via LDR ---
// Retorna valor de pH estimado entre 0 e 14
float lerPhSimulado() {
  int leituraLDR = analogRead(PINO_LDR);  // analogRead retorna int (0 a 4095)
  return (leituraLDR / 4095.0f) * 14.0f;  // Resultado convertido para escala de pH
}

// --- Função: Lê os sensores e atualiza variáveis globais ---
void lerSensores() {
  // Sensores digitais com pull-up: lógica invertida
  fosforo = !digitalRead(PINO_FOSFORO);
  potassio = !digitalRead(PINO_POTASSIO);

  // Leitura de umidade com verificação de falha
  float leituraUmidade = dht.readHumidity();
  umidade = isnan(leituraUmidade) ? -1.0f : leituraUmidade;

  // Leitura de pH simulada
  ph = lerPhSimulado();
}

// --- Função: Regras para ativar bomba ---
bool deveAtivarBomba() {
  // Avaliação simples de três condições
  const bool nutrientePresente = fosforo || potassio;
  const bool phOk = (ph >= 5.5f && ph <= 7.5f);
  const bool umidadeBaixa = (umidade > 0 && umidade < 40.0f);
  return nutrientePresente && phOk && umidadeBaixa;
}

// --- Função: Aciona ou desliga a bomba ---
void atualizarRele(bool ligar) {
  digitalWrite(PINO_RELE, ligar ? HIGH : LOW);
  bombaLigada = ligar;
}

// --- Função: Exibição de dados no Monitor Serial e no Plotter ---
void exibirSerial() {
  // Saída para leitura humana
  Serial.print("[Sensores] Fósforo: ");
  Serial.print(fosforo);
  Serial.print(" | Potássio: ");
  Serial.print(potassio);
  Serial.print(" | pH: ");
  Serial.print(ph, 2);
  Serial.print(" | Umidade: ");
  Serial.print(umidade, 1);
  Serial.print("% | Bomba: ");
  Serial.println(bombaLigada ? "Ligada" : "Desligada");

  // Linha em branco separadora
  Serial.println();

  // Saída para Serial Plotter com separação por tabulação
  Serial.print("Umidade: "); Serial.print(umidade, 2);
  Serial.print("\t");
  Serial.print("pH: "); Serial.print(ph, 2);
  Serial.print("\t");
  Serial.print("Bomba: "); Serial.println(bombaLigada ? 1 : 0);
}

// --- Função: Atualiza display LCD com métricas principais ---
void exibirLCD() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Umi:");
  lcd.print(umidade, 0);
  lcd.print("% pH:");
  lcd.print(ph, 1);

  lcd.setCursor(0, 1);
  lcd.print("Bomba: ");
  lcd.print(bombaLigada ? "Ligada" : "Deslig.");
}

// --- Loop principal ---
// Executa leitura, decisão e exibição a cada 2s
void loop() {
  lerSensores();
  bool ativar = deveAtivarBomba();
  atualizarRele(ativar);

  exibirSerial();
  exibirLCD();

  delay(2000);  // Intervalo reduzido para otimizar processamento e visualização
}