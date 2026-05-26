# EchoWall ESP32-S3 Firmware
# Sovereign through-wall sensing with Wi-Fi CSI + Acoustic fusion
# NO CLOUD DEPENDENCIES - 100% Local Processing

cmake_minimum_required(VERSION 3.16)

# Project configuration
set(SUPPORTED_TARGETS esp32s3)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)

project(echowall)

# Compiler flags for optimization
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Os -ffunction-sections -fdata-sections")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Os -ffunction-sections -fdata-sections")

# Component dependencies (ALL LOCAL)
set(EXTRA_COMPONENT_DIRS
    ${CMAKE_CURRENT_LIST_DIR}/components
)

# Build configuration
idf_build_set_property(COMPILE_OPTIONS "-Wno-unused-variable" APPEND)
