#!/bin/bash
g++ ./base/Base.cpp -fPIC -shared -o ./release/Base.so -pthread -O3 -march=native -std=c++11
