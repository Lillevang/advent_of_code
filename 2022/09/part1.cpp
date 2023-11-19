#include <iostream>
#include <fstream>
#include <map>
#include <cmath>

const int knots = 2;

struct Coordinate
{
    int x = 0;
    int y = 0;
};

int main()
{
    std::ifstream input("./input");
    Coordinate rope[knots];

    std::map<std::string, bool> visited;

    visited.insert({"0,0", true});

    while (!input.eof())
    {
        std::string direction, steps;

        input >> direction;
        input >> steps;

        int stepCount = atoi(steps.c_str());

        for (int i = 0; i < stepCount; i++)
        {

            if (direction == "U")
                rope[0].y++;
            else if (direction == "D")
                rope[0].y--;
            else if (direction == "L")
                rope[0].x--;
            else if (direction == "R")
                rope[0].x++;

            for (int knot = 1; knot < knots; knot++)
            {
                int dx = (rope[knot - 1].x - rope[knot].x);
                int dy = (rope[knot - 1].y - rope[knot].y);

                if (sqrt(dx * dx + dy * dy) > 1.5)
                {
                    if (dx > 0)
                        rope[knot].x++;
                    else if (dx < 0)
                        rope[knot].x--;

                    if (dy > 0)
                        rope[knot].y++;
                    else if (dy < 0)
                        rope[knot].y--;

                    if (knot == knots - 1)
                    {
                        char keyChar[10];
                        sprintf(keyChar, "%d:%d", rope[knot].x, rope[knot].y);
                        visited.insert({std::string(keyChar), true});
                    }
                }
            }
        }
    }

    printf("%d\n", visited.size());
    return 0;
}
