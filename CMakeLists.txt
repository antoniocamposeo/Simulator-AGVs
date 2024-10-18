# Versione minima di CMake richiesta
cmake_minimum_required(VERSION 3.10)

# Nome del progetto
project(project1)

# Imposta lo standard C++
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Aggiungi l'includepath (dove cercare gli header)
include_directories(${PROJECT_SOURCE_DIR}/include)

# Aggiungi l'eseguibile e i file sorgente
add_executable(project1
    src/main.cpp
    src/Agv.cpp
    
)