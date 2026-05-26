/**
 * EchoWall ESP32-S3 Firmware - Main Entry Point
 * Sovereign Through-Wall Sensing System
 * 
 * Features:
 * - Wi-Fi CSI (Channel State Information) capture
 * - Acoustic FMCW chirp generation (18-22 kHz)
 * - Local FFT processing for breathing detection
 * - MQTT publish to LOCAL broker ONLY
 * - Hardware-seeded privacy jitter
 * 
 * NO CLOUD DEPENDENCIES - 100% Offline Processing
 * 
 * License: Apache 2.0 + Sovereignty Clause
 * Copyright (c) 2026 KHAWRIZM Project
 */

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"

#include "esp_system.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"

#include "mqtt_client.h"
#include "driver/i2s.h"

// Local headers
#include "csi_capture.h"
#include "acoustic.h"
#include "fusion.h"

// Configuration
#define ECHOWALL_VERSION "0.5.0"
#define TAG "ECHOWALL"

// Network Configuration (LOCAL ONLY)
#define WIFI_SSID      "ECHOWALL_AP"
#define WIFI_PASS      "sovereignty2026"
#define MQTT_BROKER    "mqtt://192.168.1.100:1883"  // Raspberry Pi
#define MQTT_TOPIC     "echowall/data"

// Privacy Configuration
#define CSI_JITTER_SEED 0xDEADBEEF  // Hardware privacy seed
#define SENSING_RATE_HZ 1           // 1 Hz update rate

// Status flags
static EventGroupHandle_t s_wifi_event_group;
static esp_mqtt_client_handle_t mqtt_client;
static bool mqtt_connected = false;

#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT      BIT1

/**
 * Wi-Fi Event Handler
 * Manages connection to local AP (no internet required)
 */
static void wifi_event_handler(void* arg, esp_event_base_t event_base,
                               int32_t event_id, void* event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
        ESP_LOGI(TAG, "Connecting to local AP...");
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        ESP_LOGW(TAG, "Disconnected from AP, retrying...");
        esp_wifi_connect();
        xEventGroupClearBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
        ESP_LOGI(TAG, "Connected! IP: " IPSTR, IP2STR(&event->ip_info.ip));
        xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

/**
 * MQTT Event Handler
 * Handles connection to LOCAL broker only
 */
static void mqtt_event_handler(void *handler_args, esp_event_base_t base,
                               int32_t event_id, void *event_data)
{
    esp_mqtt_event_handle_t event = event_data;
    
    switch (event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "MQTT connected to LOCAL broker");
            mqtt_connected = true;
            break;
            
        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGW(TAG, "MQTT disconnected from broker");
            mqtt_connected = false;
            break;
            
        case MQTT_EVENT_ERROR:
            ESP_LOGE(TAG, "MQTT error occurred");
            mqtt_connected = false;
            break;
            
        default:
            break;
    }
}

/**
 * Initialize Wi-Fi Station Mode
 * Connects to local AP (no internet gateway required)
 */
static void wifi_init_sta(void)
{
    s_wifi_event_group = xEventGroupCreate();

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    
    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                        ESP_EVENT_ANY_ID,
                                                        &wifi_event_handler,
                                                        NULL,
                                                        &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT,
                                                        IP_EVENT_STA_GOT_IP,
                                                        &wifi_event_handler,
                                                        NULL,
                                                        &instance_got_ip));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());

    ESP_LOGI(TAG, "Wi-Fi initialization complete");
}

/**
 * Initialize MQTT Client
 * Connects to LOCAL Raspberry Pi broker ONLY
 */
static void mqtt_init(void)
{
    esp_mqtt_client_config_t mqtt_cfg = {
        .uri = MQTT_BROKER,
        .username = NULL,  // No auth for local broker
        .password = NULL,
    };

    mqtt_client = esp_mqtt_client_init(&mqtt_cfg);
    esp_mqtt_client_register_event(mqtt_client, ESP_EVENT_ANY_ID, 
                                   mqtt_event_handler, NULL);
    esp_mqtt_client_start(mqtt_client);

    ESP_LOGI(TAG, "MQTT client initialized (LOCAL broker only)");
}

/**
 * Publish Sensing Data to MQTT
 * Format: JSON with presence, breathing rate, confidence
 */
static void publish_sensing_data(sensing_result_t *result)
{
    if (!mqtt_connected) {
        ESP_LOGW(TAG, "MQTT not connected, skipping publish");
        return;
    }

    // Format JSON payload
    char payload[256];
    snprintf(payload, sizeof(payload),
             "{"
             "\"presence\":%s,"
             "\"breathing_rate\":%.2f,"
             "\"confidence\":%.2f,"
             "\"posture\":\"%s\","
             "\"privacy\":\"hardware_jitter_enabled\","
             "\"version\":\"%s\""
             "}",
             result->presence ? "true" : "false",
             result->breathing_rate,
             result->confidence,
             result->posture,
             ECHOWALL_VERSION);

    // Publish to LOCAL broker
    int msg_id = esp_mqtt_client_publish(mqtt_client, MQTT_TOPIC, 
                                         payload, 0, 1, 0);
    
    if (msg_id >= 0) {
        ESP_LOGI(TAG, "Published: %s", payload);
    } else {
        ESP_LOGE(TAG, "Failed to publish data");
    }
}

/**
 * Main Sensing Task
 * Runs at SENSING_RATE_HZ frequency
 */
static void sensing_task(void *pvParameters)
{
    ESP_LOGI(TAG, "Sensing task started");
    
    // Wait for Wi-Fi connection
    xEventGroupWaitBits(s_wifi_event_group,
                       WIFI_CONNECTED_BIT,
                       pdFALSE,
                       pdTRUE,
                       portMAX_DELAY);
    
    // Initialize CSI capture
    csi_init(CSI_JITTER_SEED);
    
    // Initialize acoustic system
    acoustic_init();
    
    // Initialize fusion engine
    fusion_init();
    
    ESP_LOGI(TAG, "All subsystems initialized - starting sensing loop");
    
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = pdMS_TO_TICKS(1000 / SENSING_RATE_HZ);
    
    while (1) {
        // Capture CSI data
        csi_data_t *csi = csi_capture();
        if (!csi) {
            ESP_LOGW(TAG, "CSI capture failed");
            vTaskDelayUntil(&xLastWakeTime, xFrequency);
            continue;
        }
        
        // Capture acoustic data
        acoustic_data_t *acoustic = acoustic_capture();
        if (!acoustic) {
            ESP_LOGW(TAG, "Acoustic capture failed");
            csi_free(csi);
            vTaskDelayUntil(&xLastWakeTime, xFrequency);
            continue;
        }
        
        // Fuse data and detect
        sensing_result_t result;
        if (fusion_process(csi, acoustic, &result)) {
            // Publish to local broker
            publish_sensing_data(&result);
        } else {
            ESP_LOGW(TAG, "Fusion processing failed");
        }
        
        // Cleanup
        csi_free(csi);
        acoustic_free(acoustic);
        
        // Maintain sensing rate
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}

/**
 * Application Main Entry Point
 */
void app_main(void)
{
    ESP_LOGI(TAG, "==============================================");
    ESP_LOGI(TAG, "EchoWall v%s - Sovereign Through-Wall Sensing", ECHOWALL_VERSION);
    ESP_LOGI(TAG, "NO CLOUD DEPENDENCIES - 100%% Local Processing");
    ESP_LOGI(TAG, "==============================================");
    
    // Initialize NVS (required for Wi-Fi)
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    
    // Initialize Wi-Fi (local AP only)
    wifi_init_sta();
    
    // Initialize MQTT (local broker only)
    mqtt_init();
    
    // Start sensing task
    xTaskCreate(sensing_task, "sensing_task", 8192, NULL, 5, NULL);
    
    ESP_LOGI(TAG, "Initialization complete - system operational");
}
