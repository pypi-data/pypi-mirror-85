from datetime import datetime, timezone


# constructors messy due to marshmallow. Maybe use classtype or something like that for overloading?
class JanimlWithCategories:

    @property
    def Categories(self):
        return self._Categories

    @Categories.setter
    def Categories(self, categories):
        if(type(categories) is list):
            if(all(isinstance(x, Category) for x in categories)):
                self._Categories = categories
        elif(isinstance(categories, Category)):
            self._Categories = [categories]
        else:
            raise Exception("Not a list of categories or a category")

    def get(self, key):
        splitted = key.split(".")
        categoryName = splitted[0]
        parameterName = splitted[1]
        try:
            categoryIdx = next(i for i, e in enumerate(self.Categories) if e.name == categoryName)
            parameterIdx = next(i for i, e in enumerate(self.Categories[categoryIdx].Parameters) if e.name == parameterName)
            return(self.Categories[categoryIdx].Parameters[parameterIdx].value[0])
        except StopIteration:
            return(None)

    def set(self, key, value):
        splitted = key.split(".")
        categoryName = splitted[0]
        parameterName = splitted[1]
        if(type(value) is not list):
            value = [value]
        if(len(value)):
            try:
                categoryIdx = next(i for i, e in enumerate(self.Categories) if e.name == categoryName)
                parameterIdx = next(i for i, e in enumerate(self.Categories[categoryIdx].Parameters) if e.name == parameterName)
                self.Categories[categoryIdx].Parameters[parameterIdx].value = value
            except StopIteration:
                parameter = Parameter(parameterName, value=value)
                category = Category(categoryName, [parameter])
                self.Categories.append(category)


class Device:
    def __init__(self, name: str, manufacturer: str = None, serialNumber: str = None, deviceIdentifier: str = None):
        if manufacturer is not None:
            self.manufacturer = manufacturer
        if serialNumber is not None:
            self.serialNumber = serialNumber
        if deviceIdentifier is not None:
            self.deviceIdentifier = deviceIdentifier
        self.name = name


class SIUnit():
    def __init__(self, exponent, factor, offset, value):
        self.exponent = exponent
        self.factor = factor
        self.offset = offset
        self.value = value


class Unit():
    def __init__(self, label, quantity, SIUnit=None):
        if SIUnit is not None:
            self.SIUnit = SIUnit
        self.label = label
        self.quantity = quantity


class Author:
    def __init__(self, name, affiliation=None, role=None, email=None, location=None, phone=None):
        if affiliation is not None:
            self.affiliation = affiliation
        if role is not None:
            self.role = role
        if email is not None:
            self.email = email
        if location is not None:
            self.location = location
        if phone is not None:
            self.phone = phone
        self.name = name


class Parameter:
    def __init__(self, name, value, parameterType=None):
        self.name = name
        self.parameterType = parameterType
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if(type(value) is list):
            self._value = value
        else:
            self._value = [value]
        self.parameterType = None
        if(type(self._value[0]) is int):
            self.parameterType = "Int64"
        elif(type(self._value[0]) is float):
            self.parameterType = "Float64"
        elif(type(self._value[0]) is str):
            self.parameterType = "String"
        elif(type(self._value[0]) is bool):
            self.parameterType = "Boolean"
        elif(type(self._value[0]) is datetime):
            self.parameterType = "DateTime"
        elif(self._value[0] is None):
            self.parameterType = self.parameterType
        else:
            raise Exception("Not a allowed parameter type: " + type(self._value[0]).__name__)


class Category:
    def __init__(self, name, Parameters=None, SeriesSets=None, Categories=None):
        if SeriesSets:
            self.SeriesSets = SeriesSets
        if Categories:
            self.Categories = Categories
        self.name = name
        self.Parameters = Parameters

    def to_simple_dict(self):
        parameter_dict = {}
        for param in self.Parameters:
            full_name = self.name + "_" + param.name
            full_name = full_name.replace(".", "_")
            if len(param.value) == 1:
                parameter_dict[full_name] = param.value[0]
            else:
                parameter_dict[full_name] = param.value
        return(parameter_dict)


class Method(JanimlWithCategories):
    def __init__(self, name, Author=None, Device=None, Categories=None):
        self.name = name
        if Author is not None:
            self.Author = Author
        if Device is not None:
            self.Device = Device
        if Categories is not None:
            self.Categories = Categories

    @property
    def Author(self):
        return self._Author

    @Author.setter
    def Author(self, author):
        if(isinstance(author, Author)):
            self._Author = author
        else:
            raise Exception("Not a Author")

    @property
    def Device(self):
        return self._Device

    @Device.setter
    def Device(self, device):
        if(isinstance(device, Device)):
            self._Device = device
        else:
            raise Exception("Not a Device")


class ExperimentStepReference:
    def __init__(self, experimentStepID, role, dataPurpose="consumed"):
        self.experimentStepID = experimentStepID
        self.role = role
        self.dataPurpose = dataPurpose


class SampleReference:
    def __init__(self, sampleID, role, samplePurpose="consumed"):
        self.sampleID = sampleID
        self.role = role
        self.samplePurpose = samplePurpose


class Infrastructure:
    def __init__(self, Timestamp=datetime.now(timezone.utc), ExperimentStepReferenceSet=None, SampleReferenceSet=None):
        if ExperimentStepReferenceSet is not None:
            self.ExperimentStepReferenceSet = ExperimentStepReferenceSet
        if SampleReferenceSet is not None:
            self.SampleReferenceSet = SampleReferenceSet
        self.Timestamp = Timestamp


class Sample(JanimlWithCategories):
    def __init__(self, name, sampleID, Categories=None):
        if Categories is not None:
            self.Categories = Categories
        self.sampleID = sampleID
        self.name = name


class Series:
    def __init__(self, name: str, seriesType: str, seriesID: str, dependency: str = "dependend", plotScale: str = "linear", visible: bool = True, IndividualValueSets: list = None, AutoIncrementedValueSets: dict = None, EncodedValueSets: [str] = None):
        self.name = name
        self.seriesType = seriesType
        self.seriesID = seriesID
        self.dependency = dependency
        self.plotScale = plotScale
        self.visible = visible
        if IndividualValueSets is not None:
            self.IndividualValueSets = IndividualValueSets
        if AutoIncrementedValueSets is not None:
            self.AutoIncrementedValueSets = AutoIncrementedValueSets
        if EncodedValueSets is not None:
            self.EncodedValueSets = EncodedValueSets


class SeriesSet:
    def __init__(self, name, length, Series):
        self.length = length
        self.name = name
        self.Series = Series

    def getSeries(self, series_name):
        series = next((series for series in self.Series if series.name == series_name), None)
        return(series)


class Result(JanimlWithCategories):
    def __init__(self, name, SeriesSet=None, Categories=None):
        if SeriesSet is not None:
            self.SeriesSet = SeriesSet
        if Categories is not None:
            self.Categories = Categories
        self.name = name


class ExperimentStep(JanimlWithCategories):
    def __init__(self, name, experimentStepID, Infrastructure=None, Method=None, Results=None, Categories=None, sourceDataLocation=None, TagSet=None):
        if TagSet is not None:
            self.TagSet = TagSet
        if Infrastructure is not None:
            self.Infrastructure = Infrastructure
        if Method is not None:
            self.Method = Method
        if Results is not None:
            self.Results = Results
        if sourceDataLocation is not None:
            self.sourceDataLocation = sourceDataLocation
        if Categories is not None:
            self.Categories = Categories
        self.experimentStepID = experimentStepID
        self.name = name

    def getResult(self, result_name):
        result = next((result for result in self.Results if result.name == result_name), None)
        return(result)


class JaniML:
    def __init__(self, SampleSet=None, ExperimentStepSet=None, SignatureSet=None):
        if SampleSet is not None:
            self.SampleSet = SampleSet
        if ExperimentStepSet is not None:
            self.ExperimentStepSet = ExperimentStepSet
        if SignatureSet is not None:
            self.SignatureSet = SignatureSet
