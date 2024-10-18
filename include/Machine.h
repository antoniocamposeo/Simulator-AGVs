#ifndef MACHINE_H
#define MACHINE_H

#include "Agv.h"
#include <unordered_map>
#include <tuple>
#include <string>

using namespace std;

typedef std::tuple<int,int> position;
typedef std::unordered_map<std::string,int> state;

namespace machine{

   //using namespace agv;

    class Machine
    {
        private:
            /* data */
            int m_id;
            int m_number_works;
            int m_execution_time;
            int m_load_time;
            int m_unload_time;
            int m_actual_time;
            int m_start_load_time;
            int m_finish_load_time;
            int m_start_unload_time;
            int m_finish_unload_time;
            int m_index_work;
            state m_state;
            position m_position;
            //agv::Agv m_agv_load;
            //agv::Agv m_agv_unlod;

        public:
            Machine(int id,int number_works, int execution_time,int load_time, int unload_time, position position);
           
            int get_id();
            //agv::Agv get_unload(); 
            //agv::Agv get_load();
            state get_state();
            position get_position();
           
            void set_load();
            void set_unload();
           
            void update_time();
            void check_overlap();
            void check_load();
            void check_unload();
            void calculate_work_time();
            
            void main();
    };
}
#endif