pulp_mia
**************************

PuLP-MiA is an Multi-index Addon for PuLP.
It was created to simplify working with multi-index variables
when forming constraints and an objective function.

Installation
================

The easiest way to install pulp-mia is via `PyPi <https://pypi.python.org/pypi/PuLP-MiA>`_

If pip is available on your system::

     pip install pulp-mia

Otherwise follow the download instructions on the PyPi page.

PuLP-MiA requires:
     + Python >= 3.4
     + PuLP >= 1.6.10 (see PuLP README file for more details)

Examples
================

Use Task() to create new LP-task. To create with name MyTask and in debug mode use

.. code-block::

    task = Task(Name='MyTask', debug=True)

Debug mode updates the list of variables for any changes.
Release mode updates ones only before solving a Lp-problem.

Use VariablesType flag to set type of variables

.. code-block::

    task = Task(VariablesType='Integer')     # Continuous, Integer, Boolean

Continuous is a default type.

To form the task use Constraint() class.

To create the Objective function (criterion) use

.. code-block::

    c = Constraint('MAX')     # 'MAX, 'MIN'

To set some coeffients on old or new variables use

.. code-block::

    c.setCoeff(('v'), 0.3)     # v-indicator with weight 0.3
    c.setCoeff(('p'), 0.7)     # p-indicator with weight 0.7

To set an Objective function on the task use

.. code-block::

    task.setObjective(c)

To create some Constraints use

.. code-block::

    a = Constraint('<=')      # '<=', '==', '>='

To set some coeffients on old or new variables use

.. code-block::

    # 50x11 + 100x12 + 50x21 + 100x22 <= 200
    a.setCoeff(('x', 1, 1), 50)
    a.setCoeff(('x', 1, 2), 100)
    a.setCoeff(('x', 2, 1), 50)
    a.setCoeff(('x', 2, 2), 100)

To set a sum of line combine of all variables in a-constraint use

.. code-block::

    a.setBValue(200)

To set a Constraint on the task use

.. code-block::

    task.addConstraint(a)

Let's create a Constraint with v-indicator and p-indicator use

.. code-block::

    a = Constraint('==')
    a.setCoeff(('x', 1, 1), 1)
    a.setCoeff(('x', 1, 2), 1)
    a.setCoeff(('v'), -1)     # v = x11 + x12
    task.addConstraint(a)

    a = Constraint('==')
    a.setCoeff(('x', 2, 1), 1)
    a.setCoeff(('x', 2, 2), 1)
    a.setCoeff(('p'), -1)     # p = x21 + x22
    task.addConstraint(a)

To run auto-solver by PuLP and watch result use

.. code-block::

    from pprint import pprint

    print(task)               # name & size of task
    print(task.Plan)          # solve and show status & objective value
    print('PLAN')
    pprint(task.PDict)        # show the plan as a dict

Once solved Plan is here.
By default here is no zero variables. To get full Plan use

.. code-block::

    pprint(task.Plan.getPDict(with_zeroe_values=True))

If you'll make some modifications (new Objective or Constraints) - Plan will be lost.

Before solving you can get elements of task in matrix-like style

.. code-block::

    print('\nAMatrix')
    pprint(task.AMatrix)
    print('\nBVector')
    pprint(task.BVector)
    print('\nCVector')
    pprint(task.CVector)

To see generated variables in task, status and value of Objective use

.. code-block::

    pprint(task._Variables)
    print('\nStatus', task.Status)
    print('\nObjective', task.PValue)

Finally, to get the generated pulp problem, use

.. code-block::

    prob = task.Prob

Now see how some Assignment problem can be solved by PuLP-MiA

.. code-block::

    from itertools import product
    from pprint import pprint

    from pulp_mia import Task, Constraint

    # SETS
    i_set = list(range(5))
    j_set = list(range(2))

    m_set = list(range(2))
    g_set = list(range(4))
    s_set = list(range(5))
    k_set = list(range(5))

    t_zad = 0.3
    t_s_set = [0.05*(s + 1) for s in s_set]

    G = [1, 0.5, 0.36, 0.5]
    k_set_var = [0.5*(k + 1) for k in k_set]

    def get_p(k, g):
        return 1/(G[g]/(1.7*k_set_var[k]) + 1)

    alfa_p = 0.5
    alfa_v = 0.5

    # task
    task = Task(debug=True)

    # Objective
    c_new = Constraint('MAX')
    c_new.setCoeff(('v'), alfa_v/len(i_set))
    for i, j, m, g, s, k in product(i_set, j_set, m_set, g_set, s_set, k_set):
        c_new.setCoeff(('x', i, j, m, g, s, k), alfa_p*get_p(k, g)/(1/(min(G)/(1.7*max(k_set_var)) + 1)*len(i_set)))
    task.setObjective(c_new)

    # Constraints
    # Constraint 1
    for i, m, g, s, k in product(i_set, m_set, g_set, s_set, k_set):
        a_new = Constraint('<=')
        for j in j_set:
            a_new.setCoeff(('x', i, j, m, g, s, k), 1)
        a_new.setBValue(1)
        task.addConstraint(a_new)

    # Constraint 1.5
    for i in i_set:
        a_new = Constraint('<=')
        for j, m, g, s, k in product(j_set, m_set, g_set, s_set, k_set):
            a_new.setCoeff(('x', i, j, m, g, s, k), 1)
        a_new.setBValue(1)
        task.addConstraint(a_new)

    # Constraint 2
    for i, j in product(i_set, j_set):
        a_new = Constraint('<=')
        for m, g, s, k in product(m_set, g_set, s_set, k_set):
            a_new.setCoeff(('x', i, j, m, g, s, k), 1)
        a_new.setBValue(1)
        task.addConstraint(a_new)

    # Constraint 3
    for j in j_set:
        a_new = Constraint('<=')
        for i, m, g, s, k in product(i_set, m_set, g_set, s_set, k_set):
            a_new.setCoeff(('x', i, j, m, g, s, k), t_s_set[s])
        a_new.setBValue(t_zad)
        task.addConstraint(a_new)

    # Constraint 4
    a_new = Constraint('==')
    for i, j, m, g, s, k in product(i_set, j_set, m_set, g_set, s_set, k_set):
        a_new.setCoeff(('x', i, j, m, g, s, k), 1)
    a_new.setCoeff(('v'), -1)
    a_new.setBValue(0)
    task.addConstraint(a_new)


    print(task)
    print(task.Plan)
    print('PLAN')
    pprint(task.PDict)


Copyright Dmitriy A. Pavlov (dpavlov239@mail.ru) under MIT license

See the LICENSE file for copyright information.