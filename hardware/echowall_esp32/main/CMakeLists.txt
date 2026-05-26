idf_component_register(
    SRCS 
        "echowall.c"
        "csi_capture.c"
        "acoustic.c"
        "fusion.c"
    INCLUDE_DIRS "."
    REQUIRES 
        esp_wifi
        mqtt
        driver
        nvs_flash
)
