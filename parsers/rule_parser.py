import copy
import json
from constants.criterion_keys import CriterionKeys
from constants.rules_reserved_keys import RulesReservedKeys
from constants.target_keys import TargetKeys
from enums.criterion_enum import CriterionEnum
from enums.target_enum import TargetEnum
from exceptions.criterion_value_missing_exception import CriterionValueMissingException
from exceptions.invalid_criterion_exception import InvalidCriterionException
from exceptions.invalid_target_exception import InvalidTargetException
from exceptions.rule_missing_criterion_exception import RuleMissingCriterionException

from exceptions.rule_missing_target_exception import RuleMissingTargetException
from models.rule_model import RuleModel


class RuleParser():

    def __parse_criterion(self,in_criterion):
        
        found_criterion = None

        for crit in CriterionEnum:
            if crit.value[CriterionKeys.VALUE_IN_RULE] == in_criterion[RulesReservedKeys.CRITERION_TARGET]:
                found_criterion = crit.value
                if(crit.value[CriterionKeys.REQUIRE_VALUE] == True):

                    if(in_criterion[RulesReservedKeys.CRITERION_VALUE] is None):
                        #raise exception
                        raise CriterionValueMissingException()
                    
                    found_criterion[CriterionKeys.VALUE_TO_CHECK] = in_criterion[RulesReservedKeys.CRITERION_VALUE]
                break

        if(found_criterion is None):
            raise InvalidCriterionException()
        
        return found_criterion
            

    def parse_file(self,path:str):
        with open(path, 'r') as raw_data:
            j_rule = json.load(raw_data)

            target = None
            criterion = None

            if(j_rule[RulesReservedKeys.TARGET_NAME] is None):
                raise RuleMissingTargetException()
            
            if(j_rule[RulesReservedKeys.CRITERION_OBJ_KEY] is None):
                raise RuleMissingCriterionException()
            
            found_target = None

            for target in TargetEnum:
                if target.value[TargetKeys.VALUE_IN_RULE] == j_rule[RulesReservedKeys.TARGET_NAME]:
                    found_target = target.value
                    break

            if(found_target is None):
                raise InvalidTargetException()
            
            criterion = copy.deepcopy(self.__parse_criterion(j_rule[RulesReservedKeys.CRITERION_OBJ_KEY]))
        
            ret_rule = RuleModel(found_target,criterion)

            return ret_rule
            


