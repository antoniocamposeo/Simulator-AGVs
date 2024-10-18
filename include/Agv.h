#ifndef AGV_H
#define AGV_H

#include "Machine.h"
#include <unordered_map>
#include <string>
#include <tuple>


using namespace std;

typedef struct TaskTime{
    int start;
    int end;
};
typedef std::tuple<int,int> position;
typedef std::unordered_map<std::string,TaskTime> worktime;
typedef std::unordered_map<std::string,int> state;

namespace agv{
   
    using namespace machine;

    class Agv
    {
    private:
        /* data */
        int m_id;
        float m_speed;
        int m_time_task;
        int m_travel_time;
        int m_actual_time;

        machine::Machine* m_machine;
        state m_state;
        worktime m_work_time;
        position m_position;
        std::string m_task;    

    public:
        Agv(int id, float speed);
        
        void initialize_state();
        void inizialize_work_time();
        void update_time(int time );
        
        void set_time_task(int task_time);
        void set_machine(Machine machine );
        void set_task(std::string task);
        void set_move_duration(std::string task);
        void set_position(position point);
        
        void update_machine_state();
        void check_state();
        void check_task();
        
        position get_position();
        machine::Machine* get_machine()const {return m_machine;};
        state get_state() const {return m_state;};
        std::string get_task() const {return m_task;};
        
        
        int main();
    
    };
}
#endif