cmake_minimum_required(VERSION 3.26)
project(wisielec_degejm C)

set(CMAKE_C_STANDARD 17)

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake_modules)

#SDL2
set(SDL2_PATH "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/JetBrains/SDL2-2.30.2/x86_64-w64-mingw32")
find_package(SDL2 REQUIRED)
include_directories(${SDL2_INCLUDE_DIR})

#TTF
set(SDL2_TTF_PATH "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/JetBrains/SDL2_ttf-2.22.0/x86_64-w64-mingw32")
find_package(SDL2_ttf REQUIRED)
include_directories(${SDL2_TTF_INCLUDE_DIRS})

#MIXER
set(SDL2_MIXER_PATH "C:/ProgramData/Microsoft/Windows/Start Menu/Programs/JetBrains/SDL2_mixer-2.8.0/x86_64-w64-mingw32")
find_package(SDL2_mixer REQUIRED)
include_directories(${SDL2_MIXER_INCLUDE_DIRS})


add_executable(wisielec_degejm main.c)

target_link_libraries(${PROJECT_NAME} ${SDL2_LIBRARY} ${SDL2_TTF_LIBRARIES} ${SDL2_MIXER_LIBRARIES})
