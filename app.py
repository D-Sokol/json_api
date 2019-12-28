#!/usr/bin/env python3

from adverts import app

@app.shell_context_processor
def make_shell_context():
    import adverts
    import adverts.models
    context = vars(adverts)
    context.update(vars(adverts.models))
    return context


if __name__ == '__main__':
    app.run(debug=True)
