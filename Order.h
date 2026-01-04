#pragma once
#include <string>
#include <iostream>
#include <ctime>

using namespace std;

enum class OrderType
{
    BUY,
    SELL
};

struct Order
{
    int orderId;
    double price;
    int quantity;
    OrderType type;
    time_t timestamp;

    Order(int id, double p, int qty, OrderType t)
        : orderId(id), price(p), quantity(qty), type(t)
    {
        timestamp = time(nullptr);
    }
};