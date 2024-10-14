
#include <utils.h>
#include <Agv.h>

class Machine
{
private:
    /* data */
    int m_id{0};
    int m_number_works{0};
    int m_execution_time{0};
    int m_load_time{0};
    int m_unload_time{0};
    int m_actual_time{0};
    int m_start_load_time{-1};
    int m_finish_load_time{-1};
    int m_start_unload_time{-1};
    int m_finish_unload_time{-1};
    int m_index_work{0};
    Position m_position;
    Agv m_agv_load;
    Agv m_agv_unlod;

public:
    Machine(int id,int number_works, int execution_time,int load_time, int unload_time, Position position): 
    m_id{ id }, m_number_works{number_works}, m_execution_time{execution_time},m_load_time{load_time},m_unload_time{unload_time},m_position{position}
    {};
    int get_id();
    Agv get_unload(); // capire se inserire pointer
    Agv get_load();
    State get_state();
    Position get_position();
    void set_load(Machi);
    void set_unload();
    void update_time();
    void check_overlap();
    void check_load();
    void check_unload();
    void calculate_work_time();
    void main();
};
