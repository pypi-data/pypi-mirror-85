from ..types import *


class SchemaValidator:
    @staticmethod
    def validateSchema(data, config):
        requiredColsNotInData = SchemaValidator.getRequiredColumnsThatArentInData(data, config)
        if len(requiredColsNotInData) > 0:
            message = "Data does not contain the following required columns {}.\nFailing because the remainder of " \
                      "the checks won't be able to complete without these".format(requiredColsNotInData)
            return ValidatorResponse(ValidatorStatus.FAIL, message)
        return ValidatorResponse(ValidatorStatus.SUCCESS)

    @staticmethod
    def getRequiredColumnsThatArentInData(data, config):
        return config.getArgs()["requiredColumns"].difference(data.columns)
