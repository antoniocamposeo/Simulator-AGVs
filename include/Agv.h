#include <utils.h>
#include <string>
#include <Machine.h>
class Agv
{
private:
    /* data */
    int m_id{0};
    int m_speed{0};
    int m_time_task{0};
    int m_travel_time{0};
    int m_actual_time{0};

    Machine m_machine;
    State m_state;
    WorkTime m_work_time;
    Position m_position;

    std::string m_task{""};    

public:
    Agv(int id, int speed)m_id{id},m_speed{speed}{};
    State get_state();
    std::string get_task();
    void update_time();
    void s
};

