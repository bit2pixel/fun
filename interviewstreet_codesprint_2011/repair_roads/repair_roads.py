#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

pretty_output = True

def get_input():
    keyboard = sys.stdin
    return keyboard.readline()

def say(message, prefix = '  ', suffix = ' -> '):
    if pretty_output:
        sys.stdout.write("%s%s%s" % (prefix, message, suffix))

def get_number_of_test_cases():
    say('How many test cases will you enter?', prefix = '\n')
    return int(get_input())

class Byteland:
    def __init__(self):
        self.no_of_cities = self.get_no_of_cities()
        self.no_of_connections = self.no_of_cities - 1 # n-1

        self.no_of_required_robots = None

        self.connections = {}

        for con in range(self.no_of_connections):
            self.make_connection(self.get_connection())

        #Calculating the number of required robots"
        self.calculate_required_no_of_robots()

    def get_no_of_cities(self):
        say('Enter the number of cities', suffix=' -> ')
        return int(get_input())

    def get_connection(self):
        while True:
            say('Add Connection (Ex: from_city to_city)')
            con_data = get_input()
            connections = con_data.split()

            # Get exactly two parameters
            if len(connections) == 2:

                from_city = int(connections[0])
                to_city = int(connections[1])

                # Inputs cannot exceed the number of cities
                if from_city in range(self.no_of_cities) and to_city in range(self.no_of_cities):

                    return [from_city, to_city]

            print '\n  Error: Inputs cannot exceed the number of cities. City numbers start from zero. Try again.\n'

    def make_connection(self, data):
        from_city = data[0]
        to_city = data[1]

        if not self.connections.has_key(from_city):
            self.connections[from_city] = []

        self.connections[from_city].append(to_city)
        say("Connection created from city %s to city %s." % (from_city, to_city), prefix='  ', suffix='  \n\n')

    def calculate_required_no_of_robots(self):
        return self.no_of_required_robots


if __name__ == '__main__':
    no_of_tests = get_number_of_test_cases()

    test_cases = []

    for t in range(no_of_tests):
        say("Test Case %s" % str(t + 1), prefix='\n=== ', suffix=' ===\n')
        test_cases.append(Byteland())

    say('Required number of robots for test cases', prefix='\n== ', suffix=' ==\n\n')
    for tc_list_item in list(enumerate(test_cases)):
        test_case_number = tc_list_item[0]
        test_case = tc_list_item[1]
        say("Test Case %s:" % test_case_number)
        print test_case.no_of_required_robots

    print
