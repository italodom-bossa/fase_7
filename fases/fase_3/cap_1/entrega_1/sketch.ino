#include "DHT.h"

// --- Definição dos Pinos ---
#define PINO_FOSFORO 14    // Botão representando a presença de fósforo
#define PINO_POTASSIO 4    // Botão representando a presença de potássio
#define PINO_LDR 36        // Pino analógico simulando a leitura de pH (com LDR)
#define PINO_DHT 5         // Sensor de umidade e temperatura DHT22 no pino digital 5
#define PINO_RELE 18       // Pino conectado ao relé ou LED que simula a bomba de irrigação

// --- Configuração do Sensor DHT ---
#define DHTTYPE DHT22
DHT dht(PINO_DHT, DHTTYPE);  // Cria um objeto DHT para interagir com o sensor

void setup() {
  Serial.begin(115200);  // Inicializa a comunicação serial para monitoramento

  // Configura os botões como entradas com resistor de pull-up ativado
  pinMode(PINO_FOSFORO, INPUT_PULLUP);
  pinMode(PINO_POTASSIO, INPUT_PULLUP);

  // Configura o pino do relé (LED) como saída
  pinMode(PINO_RELE, OUTPUT);

  // Inicializa o sensor DHT
  dht.begin();
}

// Função que simula a leitura do pH através do valor analógico do LDR
float ler_ph_simulado() {
  int valor_analogico = analogRead(PINO_LDR);  // Lê valor entre 0 e 4095
  return (valor_analogico / 4095.0) * 14.0;    // Converte para escala de pH (0 a 14)
}

void loop() {
  // --- Leitura dos Botões ---
  // Como os botões estão com PULLUP, o valor lido é invertido: LOW significa pressionado.
  bool fosforo = !digitalRead(PINO_FOSFORO);   // true se botão de fósforo estiver pressionado
  bool potassio = !digitalRead(PINO_POTASSIO);// true se botão de potássio estiver pressionado

  // --- Leitura da Umidade ---
  float umidade = dht.readHumidity();          // Lê a umidade do ar
  if (isnan(umidade)) {                        // Se a leitura falhar, evita usar valor inválido
    umidade = -1;                              // Valor inválido para indicar erro
  }

  // --- Leitura do pH Simulado ---
  float ph = ler_ph_simulado();                // Simula a leitura de pH com o LDR

  // --- Lógica para Acionamento da Bomba ---

  // Verifica se há algum nutriente presente (fósforo ou potássio)
  bool nutriente_presente = fosforo || potassio;

  // Verifica se o pH está dentro da faixa adequada (entre 5.5 e 7.5)
  bool ph_adequado = (ph >= 5.5 && ph <= 7.5);

  // Verifica se a umidade está baixa (abaixo de 40%)
  bool umidade_baixa = (umidade > 0 && umidade < 40);

  // A bomba só será ativada se:
  // 1. Houver algum nutriente presente.
  // 2. O pH estiver adequado.
  // 3. A umidade estiver baixa.
  bool ativar_bomba = nutriente_presente && ph_adequado && umidade_baixa;

  // --- Controle da Bomba ---
  // Liga ou desliga o relé (ou LED) conforme a necessidade de irrigação
  digitalWrite(PINO_RELE, ativar_bomba ? HIGH : LOW);

  // --- Monitoramento via Serial ---
  // Exibe no monitor serial os valores das leituras e o estado da bomba
  Serial.print("Fósforo: "); Serial.print(fosforo);
  Serial.print(" | Potássio: "); Serial.print(potassio);
  Serial.print(" | pH: "); Serial.print(ph, 2);
  Serial.print(" | Umidade: "); Serial.print(umidade, 1);
  Serial.print("% | Bomba: "); Serial.println(ativar_bomba ? "Ligada" : "Desligada");

  // Aguarda 2 segundos antes de repetir o ciclo
  delay(2000);
}