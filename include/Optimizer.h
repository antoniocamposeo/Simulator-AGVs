#ifndef OPTIMIZER_H
#define OPTIMIZER_h

#include <Machine.h>
#include <Agv.h>
#include <tuple>
#include <unordered_map>
#include <string>

using namespace machine;
using namespace agv;

namespace optimizer{

typedef std::tuple<int,int> position;
typedef std::unordered_map<std::string,std::tuple<int, int>> position_stock;


typedef struct AGV {
    std::unordered_map<std::string, int> State;
    std::string Task;
    machine::Machine Machine;
    position Position;
};

typedef struct Machine {
    std::unordered_map<std::string, int> State;
    agv::Agv Agv_Load;
    agv::Agv Agv_Unload;
};

typedef std::unordered_map<std::string, AGV> AGVs;
typedef std::unordered_map<std::string, Machine> Machines;
typedef std::unordered_map<int, int> sequence;
typedef std::unordered_map<AGVs, Machines> state;

class Optimizer{

private:
    int m_N;
    int m_M;
    int m_sim_time;
    float m_speed;
    int m_t;
    position_stock m_stock_position;
    sequence m_sequence;
    machine::Machine* m_machineArray;
    agv::Agv* m_agvArray;

    agv::Agv* m_agv_available;
    machine::Machine* m_machine_load_available;
    machine::Machine* m_machine_unload_available;    
    state m_state;

public:
    Optimizer(int N, int M, int sim_time, float speed);
    ~Optimizer();

    void update_state();
    void agv_availables();
    void machines_availables();
    void assign_machine_agv(); 
    void check_sequence();
    void find_best_machine_to_assign();
    void distance_to_time();
    void update_task();
    void update_all();
    void print_position_agv();
    void check_status_simulation();
    void set_states();
    void get_states();
    void main();

};
}


#endif