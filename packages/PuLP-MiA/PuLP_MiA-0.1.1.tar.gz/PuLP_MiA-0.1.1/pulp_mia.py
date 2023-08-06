from copy import copy
from typing import TypeVar, Iterable, Tuple, Callable, Any, Mapping

from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, LpInteger, LpContinuous, lpDot, LpStatus, value

__author__ = 'Dmitriy Pavlov'
__email__ = 'dpavlov239@mail.ru'
__version__ = '0.1.1'
__license__ = 'MIT'

def get_key(__d: Any, __value: Any) -> Any:
    """Getting a key by value from an arbitrary dictionary d
If there is no such key, it returns None"""
    for k, v in __d.items():
        if v == __value:
            return k
    return None


Constraint = TypeVar('T', bound='Constraint')
class Constraint(object):
    """The class CONSTRAINT"""
    def __init__(self: Constraint, Sign: str='==') -> None:
        """конструктор класса ОГРАНИЧЕНИЕ"""
        super(Constraint, self).__init__()
        self._ACoeffDict = {}
        self._Sign = Sign
        self._BValue = 0

    def _convert_coeff_key(self: Constraint, ACoeffKey: Iterable) -> tuple:
        """Converts all" keys " of VARIABLES to int, except for the VARIABLE type (0-position)"""
        if isinstance(ACoeffKey,str):
            return ACoeffKey
        ACoeffKey_ = list(ACoeffKey)
        for i in range(1, len(ACoeffKey_)):
            ACoeffKey_[i] = int(ACoeffKey_[i])
        return tuple(ACoeffKey_)

    def setACoeffDict(self: Constraint, AcoeffDict: dict) -> None:
        """setting a dictionary of coefficients for variables in a CONSTRAINT"""
        self._ACoeffDict = AcoeffDict

    def getACoeffDict(self: Constraint) -> dict:
        """getting a dictionary of coefficients for variables from a CONSTRAINT"""
        return self._ACoeffDict

    def setCoeff(self: Constraint, ACoeffKey: Iterable, ACoeffValue: float) -> None:
        """setting the coefficient for a variable named ACoeffKey in the CONSTRAINT"""
        self._ACoeffDict[self._convert_coeff_key(ACoeffKey)] = ACoeffValue

    def getCoeff(self: Constraint, ACoeffKey: Iterable) -> float:
        """getting the coefficient for a variable named ACoeffKey from a CONSTRAINT"""
        if self._convert_coeff_key(ACoeffKey) in self._ACoeffDict:
            return self._ACoeffDict[self._convert_coeff_key(ACoeffKey)]
        else:
            return None

    def setSign(self: Constraint, Sign: str) -> None:
        """setting the Sign sign to a CONSTRAINT"""
        self._Sign = Sign

    def getSign(self: Constraint) -> str:
        """getting the Sign from a RESTRICTION"""
        return self._Sign

    def setBValue(self: Constraint, BValue: float) -> None:
        """setting B value to a CONSTRAINT"""
        self._BValue = BValue

    def getBValue(self: Constraint) -> float:
        """getting B Value from a CONSTRAINT"""
        return self._BValue

    def getAVector(self: Constraint, VariablesDict: Mapping[Iterable,int]) -> Iterable[float]:
        """getting A CONSTRAINT vector"""
        AVector = [0 for i in range(len(VariablesDict))]
        for i in iter(self._ACoeffDict):
            AVector[VariablesDict[i]] = self._ACoeffDict[i]
        return AVector


Plan = TypeVar('T', bound='Plan')
class Plan(object):
    """The class PLAN"""
    def __init__(self, PlanDict: dict={}, ResultVariables=None, VariablesDict: dict=None, PlanValue=None, Status=None):
        """Constructor of the PLAN class"""
        super(Plan, self).__init__()
        self._Status = Status
        self._PPlanValue = PlanValue
        self._PPlanDict = PlanDict
        if (ResultVariables) and (VariablesDict):
            for v in ResultVariables:
                vkey = get_key(VariablesDict, int(str(v.name).split('x_')[1]))
                vvalue = v.varValue
                self._PPlanDict[vkey] = vvalue

    def __repr__(self) -> str:
        return 'PLAN info:\n' + '\tStatus: ' + str(self.getStatus()) + '\n\tObjective: ' + str(self.getPValue())

    def getStatus(self):
        """returns the solution status"""
        return LpStatus[self._Status]

    def getPValue(self):
        """returns the value of the target function"""
        return self._PPlanValue

    def getPVector(self, VariablesDict: Mapping[Iterable,int]) -> Iterable[float]:
        """returns a vector PLAN"""
        PVector = [0 for i in range(len(VariablesDict))]
        for i in self._PPlanDict:
            PVector[VariablesDict[i]] = self._PPlanDict[i]
        return PVector

    def getPDict(self, with_zeroe_values=False) -> dict:
        """returns the PLAN in the form of a dictionary"""
        if not with_zeroe_values:
            return {k:v for k, v in self._PPlanDict.items() if v != 0}
        return copy(self._PPlanDict)



Task = TypeVar('T', bound='Task')
class Task(object):
    """The class TASK
The main class of the library
    """

    def __repr__(self) -> str:
        """string representation of the TASK (summary)"""
        self.collectVariables()
        res = 'TASK info:' + '\n'
        res += '\tNAME: ' + str(self._name) + '\n'
        res += '\tSIZE: ' + str(self.variablesCount) + ' x ' + str(self.constraintsCount)
        return res

    def __init__(self, Name: str=None, VariablesType: str='Continuous', debug=False) -> None:
        """constructor of the TASK class"""
        super(Task, self).__init__()
        #
        self._name = Name or 'test-task'
        self._VariablesType = VariablesType
        self._debug = debug
        #
        self._Objective = Constraint() # Constraint
        self._Constraints = [] # List[Constraint]
        #
        self._Variables = {} # dict
        #
        self._Plan = None # Plan

    def setObjective(self, Objective: Constraint) -> None:
        """setting the Objective function in the TASK"""
        self._Objective = Objective
        if self._debug:
            self.collectVariables()

    def addConstraint(self, Constraint: Constraint) -> None:
        """adding a CONSTRAINT to a TASK and collecting variables"""
        self._Constraints.append(Constraint)
        if self._debug:
            self.collectVariables()

    def collectVariables(self) -> None:
        """forming associative variables from the PROBLEM"""
        self._Plan = None
        self._Variables = copy(self._Objective.getACoeffDict())
        for constr in self._Constraints:
            self._Variables.update(constr.getACoeffDict())

        #assigning numbers to VARIABLES
        num = 0
        for i in iter(self._Variables):
            self._Variables[i] = num
            num += 1

    @property
    def AMatrix(self) -> Iterable[Iterable[float]]:
        """the formation and results matrix A"""
        return [constr.getAVector(self._Variables) for constr in self._Constraints]

    @property
    def BVector(self) -> Iterable[float]:
        """the formation and results vector B (resource vector)"""
        return [b.getBValue() for b in self._Constraints]

    @property
    def CVector(self) -> Iterable[float]:
        """the formation and results vector C (Objective function)"""
        return self._Objective.getAVector(self._Variables)

    @property
    def PVector(self) -> Iterable[float]:
        """return the vector P (plan)"""
        if not self._Plan:
            self.solve()
        return self._Plan.getPVector(self._Variables)

    @property
    def PDict(self) -> dict:
        """return the dictionary-plan"""
        if not self._Plan:
            self.solve()
        return self._Plan.getPDict(with_zeroe_values=False)

    @property
    def Status(self):
        if not self._Plan:
            self.solve()
        return self._Plan.getStatus()

    @property
    def PValue(self):
        if not self._Plan:
            self.solve()
        return self._Plan.getPValue()


    @property
    def Plan(self) -> Plan:
        """return a PLAN (solving the problem and issuing a plan - if not solved)"""
        if not self._Plan:
            self.solve()
        return self._Plan


    @property
    def Prob(self) -> LpProblem:
        if not self._debug:
            self.collectVariables()

        if self.isMaximize:
            prob = LpProblem("ZDO TASK", LpMaximize)
        else:
            prob = LpProblem("ZDO TASK", LpMinimize)

        if self._VariablesType == 'Continuous':
            x = LpVariable.matrix("x",
            (list(range(len(self.CVector)))), 0, None, LpContinuous)  # LpContinuous
        elif self._VariablesType == 'Integer':
            x = LpVariable.matrix("x",
            (list(range(len(self.CVector)))), 0, None, LpInteger)  # LpInteger
        elif self._VariablesType == 'Boolean':
            x = LpVariable.matrix("x",
            (list(range(len(self.CVector)))), 0, 1, LpInteger)  # LpInteger (as Boolean)
        else:
            raise Exception('Unknown variables type' + str(self._VariablesType))

        #forming the Objective function
        prob += lpDot(x, self.CVector)

        #creating Constraints
        for constr in self._Constraints:
            if constr.getSign() == '==':
                prob += lpDot(x, constr.getAVector(self._Variables)) == constr.getBValue()
            elif constr.getSign() == '<=':
                prob += lpDot(x, constr.getAVector(self._Variables)) <= constr.getBValue()
            elif constr.getSign() == '>=':
                prob += lpDot(x, constr.getAVector(self._Variables)) >= constr.getBValue()

        return prob

    @property
    def isMaximize(self) -> bool:
        """returns True if the target function tends to the maximum"""
        return (self._Objective.getSign() == 'MAX')

    @property
    def isMinimize(self) -> bool:
        """returns True if the target function tends to the minimum"""
        return (self._Objective.getSign() == 'MIN')

    @property
    def variablesCount(self) -> int:
        """number of TASK VARIABLES"""
        return len(self._Variables)

    @property
    def constraintsCount(self) -> int:
        """the number of CONSTRAINTS in the PROBLEM"""
        return len(self._Constraints)

    def solve(self: Task) -> None:
        """Standard solution to a linear programming problem"""
        prob = self.Prob
        prob.solve()
        self._Plan = Plan(
            ResultVariables=prob.variables(),
            VariablesDict=self._Variables,
            PlanValue=prob.objective.value(),
            Status=prob.status
        )
