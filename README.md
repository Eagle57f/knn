Use `pip install -r requirements.txt` in the cmd before launching the program for the first time.

All .csv files must be in /tables.



    The .svg file must be is this form:
    
    
        The first column must be the names of the possibilities
            ▼
    +=================+==============+==============+==============+
    ‖ Name            ‖   Caracter 1 |   Caracter 2 |   Caracter n ‖   <- The first row must be the titles of the columns
    +=================+==============+==============+==============+
    ‖ aaaaaaaaaaa     ‖       50     |    2.8124    |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ bbbbbbbbbbbbbb  ‖       22     |    2.84454   |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ aaaaaaaaaaa     ‖       2*0    |    3.69878   |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ bbbbbbbbbbbbbb  ‖       31     |    3.69878   |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ bbbbbbbbbbbbbb  ‖       24     |    3.69878   |      ...     ‖
    +-----------------+--------------+--------------+--------------+
    ‖ x               ‖       50     |    3.69878   |      ...     ‖   <- The last row must be the searched item, 
    +=================+==============+==============+==============+      which name must be x or X or / or ?