import random as rand

'''
Jonathan Elsner
2020

Python module that facilitates asking common types of questions to the user.
Accounts for invalid user responses and reprompts the question. Provides a high
amount of customization for handling edge cases and input sanitization with
straightforward default parameters.
'''


def yes_no_cast(response: str):
    '''
    Function to determine whether a given string represents the affirmative or
    the negative.

    Valid affirmative responses incude: 'yes' 'YES' 'y' 'Y' 'yup'

    Valid negative responses include: 'no' 'N' 'nein' 'foo'

    Arguments

        response    str containing an affirmative, negative, or something else

    Returns

        True if the response is the affirmative, otherwise False
    '''

    # You might think this is a little lax for what is considered affirmative,
    # or negative for that matter. The stakes aren't high, this works.
    return response.lower()[0] == 'y'


def ask_question(prompt: str, in_bounds=lambda _: True, cast=lambda x: x, error: str = 'Invalid response'):
    '''
    Generalized function for asking the user questions, validating their
    response, and responding accordingly.

    Arguments

        prompt      The question to ask the user

        in_bounds   A function verifying that the user's response is within the
                    domain of correct answers. For example, if the question asks
                    for an answer between 1 and 100, in_bounds makes sure that
                    1 < response < 100

        cast        The cast that should be applied to the string returned by
                    input() to correctly format the user's input

        error       The message to print when the user inputs an invalid
                    response

    Returns

        A valid response from the user
    '''

    answer = None
    while True:
        try:
            # Prompt the user, and if they put in an invalid answer, ask again
            answer = cast(input(prompt))
            while not in_bounds(answer):
                print(error)  # Let the user know they put in an invalid answer
                answer = cast(input(prompt))

            break  # Break out of error-handling loop
        except ValueError:  # Deal with bad casts
            print(error)

    return answer


def range_question(prompt: str, lower_bound: float = 0, upper_bound: float = 5, error='Invalid response') -> float:
    '''
    Ask the user to give a rating on a numerical scale.

    Arguments

        prompt      What is being rated, not including the scale on which it is
                    rated, completing the phrase 'On a scale of one to ten...'

        lower_bound The lowest numerical rating the user can give the prompt

        upper_bound The highest numerical rating the user can give the prompt

        error       The message read to the user when they input an invalid
                    response

        Returns

            the numerical value with which the user responded
    '''

    # Ask the user the question and return their response
    return ask_question(
        'On a scale of {0} to {1}, '.format(
            lower_bound, upper_bound) + prompt + ' ',
        in_bounds=lambda x: lower_bound <= x <= upper_bound,
        cast=float,
        error=error
    )


def option_question(prompt: str, options: list, return_values=None, error: str = 'Invalid response'):
    '''
    Ask the user to pick from a list of options in response to a prompt. The
    user responds by inputting the numerical index of the option.

    Arguments

        prompt      The prompt for the question

        options     The list of options the user can pick in response to the prompt

        return_values       The list of values to return, with each index
                            corresponding to the value that will be returned
                            when the option with the same index is chosen by the
                            user

        error       The message to be printed to the user when they input an
                    invalid response

    Returns

        the integer index of the option chosen or the value of return_values at
        the chosen index
    '''

    # Generate the prompt string
    txt = prompt + '\n' + '\n'.join(['\t{i} - {c}'.format(i=i, c=c)
                                     for i, c in enumerate(options)]) + '\n> '

    # Ask the question and get the user's response
    choice = ask_question(txt,
                          in_bounds=lambda c: 0 <= c < len(options),
                          cast=int,
                          error=error
                          )

    # Return the user's choice in the proper format
    if return_values is None:
        return choice
    else:
        return return_values[choice]


def ask_some(questions: dict, n: int) -> dict:
    '''
    Ask the user a limited number of yes or no questions specified

    Arguments

        questions       The yes or no questions that could be asked

        n               The number of questions to ask, less than or equal to
                        the length of the questions list

    Returns

        A dictionary relating the str keyword for each question to the user's
        True/False response to the question
    '''

    chosen = {}

    # Ask only n questions
    for i in range(n):
        q = None

        # Loop through questions until one not previously asked is selected
        while q == None or q in chosen.keys():
            q = rand.choice(list(questions.keys()))

            # Notify the user if all the possible questions have been asked
            if len(chosen) == len(questions):
                print('All questions in set asked!')
                return chosen

        # Ask the user the question and record their response
        chosen.update({q: yes_no_question(questions[q] + ' ')})

    return chosen


def yes_no_question(prompt: str, error: str = 'Invalid response') -> bool:
    '''
    Asks the user a yes or no question

    Arguments

        prompt      The yes or no question to ask the user

        error       The message to print to the user when they input an invalid
                    response

    Returns

        True if the user answers yes, False otherwise
    '''
    return ask_question(prompt,
                        in_bounds=lambda c: c is not None,
                        cast=yes_no_cast,
                        error=error
                        )
