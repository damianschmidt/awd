def step(progress, number_of_steps):
    print(f'\n-------------------- PROGRESS: {loading_bar(progress, number_of_steps)} '
          f'{(progress / number_of_steps) * 100: .1f}% --------------------\n')
    progress += 1
    return progress


def loading_bar(progress, step_number):
    bar = ''
    for i in range(step_number):
        bar += '##' if i < progress else '  '
    return f'[{bar}]'
