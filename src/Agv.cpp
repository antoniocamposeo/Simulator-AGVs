#include "../include/Agv.h"
#include <iostream>

using namespace agv;
using namespace std;

Agv::Agv(int id, float speed):m_id{id},m_speed{speed},m_time_task{0},m_travel_time{0},m_actual_time{0}{
    this->m_machine = nullptr;
    this->m_task = "";
    this->m_position = std::make_tuple(0,0); 
    this->initialize_state();

}

void Agv::initialize_state(){
    this->m_state["Move"] = 0;
    this->m_state["Load"] = 0;
    this->m_state["Unload"] = 0;
    this->m_state["Wait"] = 0;
}

void Agv::inizialize_work_time(){

    this->m_work_time["Load"] = {0,0};
    this->m_work_time["Unload"] = {0,0};
    
}




int agv::Agv::main(){
    std::cout << "Init Variable:["<< this->m_state.size()<<"]" <<endl;
    return 0;
}


