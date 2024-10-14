struct Position
{
    /* data */
    int x{0};
    int y{0};
};
struct State
{
    int load{0};
    int unload{0};
    int work{0};
    int complete{0};
};
struct WorkTime
{
    int start_load{0};
    int end_load{0};
    int start_unload{0};
    int end_unload{0};
};
