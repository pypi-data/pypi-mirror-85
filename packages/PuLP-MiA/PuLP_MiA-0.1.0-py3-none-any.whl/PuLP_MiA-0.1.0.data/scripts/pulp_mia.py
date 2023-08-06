from copy import copy
from typing import TypeVar, Iterable, Tuple, Callable, Any, Mapping

from pulp import LpProblem, LpVariable, LpMinimize, LpMaximize, LpInteger, LpContinuous, lpDot, LpStatus, value

__author__ = 'Dmitriy Pavlov'
__email__ = 'dpavlov239@mail.ru'
__version__ = '0.1.0'
__license__ = 'MIT'

def get_key(__d: Any, __value: Any) -> Any:
    """Получение ключа по значению value из произвольного словаря d
    Если такого ключа нет - возвращает None"""
    for k, v in __d.items():
        if v == __value:
            return k
    return None


Constraint = TypeVar('T', bound='Constraint')
class Constraint(object):
    """Класс ОГРАНИЧЕНИЕ"""
    def __init__(self: Constraint, Sign: str='==') -> None:
        """конструктор класса ОГРАНИЧЕНИЕ"""
        super(Constraint, self).__init__()
        self._ACoeffDict = {}
        self._Sign = Sign
        self._BValue = 0

    def _convert_coeff_key(self: Constraint, ACoeffKey: Iterable) -> tuple:
        """Преобразует все "ключи" ПЕРЕМЕННЫХ в int, кроме типа ПЕРЕМЕННОЙ (0-позиция)"""
        if isinstance(ACoeffKey,str):
            return ACoeffKey
        ACoeffKey_ = list(ACoeffKey)
        for i in range(1, len(ACoeffKey_)):
            ACoeffKey_[i] = int(ACoeffKey_[i])
        return tuple(ACoeffKey_)

    def setACoeffDict(self: Constraint, AcoeffDict: dict) -> None:
        """установка словаря коэффициентов при переменных в ОГРАНИЧЕНИИ"""
        self._ACoeffDict = AcoeffDict

    def getACoeffDict(self: Constraint) -> dict:
        """получение словаря коэффициентов при переменных из ОГРАНИЧЕНИЯ"""
        return self._ACoeffDict

    def setCoeff(self: Constraint, ACoeffKey: Iterable, ACoeffValue: float) -> None:
        """установка коэффициента при переменной с именем ACoeffKey в ОГРАНИЧЕНИЕ"""
        self._ACoeffDict[self._convert_coeff_key(ACoeffKey)] = ACoeffValue

    def getCoeff(self: Constraint, ACoeffKey: Iterable) -> float:
        """получение коэффициента при переменной с именем ACoeffKey из ОГРАНИЧЕНИЯ"""
        if self._convert_coeff_key(ACoeffKey) in self._ACoeffDict:
            return self._ACoeffDict[self._convert_coeff_key(ACoeffKey)]
        else:
            return None

    def setSign(self: Constraint, Sign: str) -> None:
        """установка знака Sign в ОГРАНИЧЕНИЕ"""
        self._Sign = Sign

    def getSign(self: Constraint) -> str:
        """получение знака Sign из ОГРАНИЧЕНИЯ"""
        return self._Sign

    def setBValue(self: Constraint, BValue: float) -> None:
        """установка значения BValue в ОГРАНИЧЕНИЕ"""
        self._BValue = BValue

    def getBValue(self: Constraint) -> float:
        """получение значения BValue из ОГРАНИЧЕНИЯ"""
        return self._BValue

    def getAVector(self: Constraint, VariablesDict: Mapping[Iterable,int]) -> Iterable[float]:
        """получение вектора А ОГРАНИЧЕНИЯ"""
        AVector = [0 for i in range(len(VariablesDict))]
        for i in iter(self._ACoeffDict):
            AVector[VariablesDict[i]] = self._ACoeffDict[i]
        return AVector


Plan = TypeVar('T', bound='Plan')
class Plan(object):
    """Класс ПЛАН"""
    def __init__(self, PlanDict: dict={}, ResultVariables=None, VariablesDict: dict=None, PlanValue=None, Status=None):
        """Конструктор класса ПЛАН"""
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
        """выдача статуса решения"""
        return LpStatus[self._Status]

    def getPValue(self):
        """выдача значения целевой функции"""
        return self._PPlanValue

    def getPVector(self, VariablesDict: Mapping[Iterable,int]) -> Iterable[float]:
        """возвращает вектор-ПЛАН"""
        PVector = [0 for i in range(len(VariablesDict))]
        for i in self._PPlanDict:
            PVector[VariablesDict[i]] = self._PPlanDict[i]
        return PVector

    def getPDict(self, with_zeroe_values=False) -> dict:
        """возвращает ПЛАН в виде словаря"""
        if not with_zeroe_values:
            return {k:v for k, v in self._PPlanDict.items() if v != 0}
        return copy(self._PPlanDict)



Task = TypeVar('T', bound='Task')
class Task(object):
    """Класс ЗАДАЧА
    Основной класс библиотеки
    """

    def __repr__(self) -> str:
        """строковое представление ЗАДАЧИ (краткая информация)"""
        self.collectVariables()
        res = 'TASK info:' + '\n'
        res += '\tNAME: ' + str(self._name) + '\n'
        res += '\tSIZE: ' + str(self.variablesCount) + ' x ' + str(self.constraintsCount)
        return res

    def __init__(self, Name: str=None, VariablesType: str='Continuous', debug=False) -> None:
        """конструктор класса ЗАДАЧА"""
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
        """установка целевой функции в ЗАДАЧУ"""
        self._Objective = Objective
        if self._debug:
            self.collectVariables()     # слишком часто обновляемся!

    def addConstraint(self, Constraint: Constraint) -> None:
        """добавление ОГРАНИЧЕНИЯ в ЗАДАЧУ и сбор переменных"""
        self._Constraints.append(Constraint)
        if self._debug:
            self.collectVariables()     # слишком часто обновляемся!

    def collectVariables(self) -> None:
        """формирование ассоциативных переменных из ЗАДАЧИ (из self._Objective + self.Constarints)"""
        self._Plan = None
        self._Variables = copy(self._Objective.getACoeffDict())
        for constr in self._Constraints:
            self._Variables.update(constr.getACoeffDict())

        #присвоение номеров ПЕРЕМЕННЫМ
        num = 0
        for i in iter(self._Variables):
            self._Variables[i] = num
            num += 1

    @property
    def AMatrix(self) -> Iterable[Iterable[float]]:
        """формирование и выдача матрицы А"""
        return [constr.getAVector(self._Variables) for constr in self._Constraints]

    @property
    def BVector(self) -> Iterable[float]:
        """выдача вектора B (вектор ресурсов)"""
        return [b.getBValue() for b in self._Constraints]

    @property
    def CVector(self) -> Iterable[float]:
        """выдача вектора C (целевая функция)"""
        return self._Objective.getAVector(self._Variables)

    @property
    def PVector(self) -> Iterable[float]:
        """выдача вектора P (план)"""
        if not self._Plan:
            self.solve()
        return self._Plan.getPVector(self._Variables)

    @property
    def PDict(self) -> dict:
        """выдача словаря-плана"""
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
        """выдача ПЛАНА (решение задачи и выдача плана - если не решалась)"""
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

        #формирование целевой функции
        prob += lpDot(x, self.CVector)

        #формирование ограничений
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
        """выдача True, если целевая функция стремится в максимум"""
        return (self._Objective.getSign() == 'MAX')

    @property
    def isMinimize(self) -> bool:
        """выдача True, если целевая функция стремится в минимум"""
        return (self._Objective.getSign() == 'MIN')

    @property
    def variablesCount(self) -> int:
        """число ПЕРЕМЕННЫХ ЗАДАЧИ"""
        return len(self._Variables)

    @property
    def constraintsCount(self) -> int:
        """число ОГРАНИЧЕНИЙ ЗАДАЧИ"""
        return len(self._Constraints)

    def solve(self: Task) -> None:
        """Стандартное решение задачи линейного программирования"""
        prob = self.Prob
        prob.solve()
        self._Plan = Plan(
            ResultVariables=prob.variables(),
            VariablesDict=self._Variables,
            PlanValue=prob.objective.value(),
            Status=prob.status
        )
