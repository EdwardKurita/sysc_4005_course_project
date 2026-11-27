from sysc_4005_course_project.model.random_generation import *

import inquirer as iq

def main() -> None:
    choices = ['Simulate', 'draw_bags', 'draw_occupancy', 'Run All Tests']

    questions = [
        iq.List(
            'choice',
            message="Please select an option:",
            choices=choices,
        ),
    ]

    answers = iq.prompt(questions)

    if answers:
        if answers['choice'] == choices[0]:
            print("RUNNING SIMULATION")

        elif answers['choice'] == choices[1]:
            print("route to draw_bags")

        elif answers['choice'] == choices[2]:
            print("route to draw_occupancy")

        elif answers['choice'] == choices[3]:
            print("Run test circuit")

        else:
            print("INVALID ANSWER")

    else:
        print("NO ANSWER GIVEN. ENDING PROGRAM.")


    
