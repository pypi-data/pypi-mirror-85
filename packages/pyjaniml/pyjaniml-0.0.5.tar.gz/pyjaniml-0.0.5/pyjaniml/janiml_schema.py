from marshmallow import fields, post_load, post_dump, Schema

from .janiml import JaniML, Category, SeriesSet, Series, ExperimentStep, Sample, Parameter, Device, Author, SIUnit, Result, ExperimentStepReference, SampleReference, Method, Infrastructure


class DeviceSchema(Schema):
    deviceIdentifier = fields.String()
    serialNumber = fields.String()
    name = fields.String()
    manufacturer = fields.String()

    @post_load
    def make_device(self, data, **kwargs):
        return Device(**data)


class AuthorSchema(Schema):
    name = fields.String()
    affiliation = fields.String()
    location = fields.String()
    role = fields.String()
    email = fields.String()
    phone = fields.String()

    @post_load
    def make_autor(self, data, **kwargs):
        return Author(**data)


class ParameterSchema(Schema):
    name = fields.String()
    parameterType = fields.String()
    value = fields.Method("serializeValue", deserialize="deserializeValue")

    def serializeValue(self, obj):
        return(obj.value)

    def deserializeValue(self, values):
        return(values)

    @post_load
    def make_parameter(self, data, **kwargs):
        return Parameter(**data)


class SIUnitSchema(Schema):
    exponent = fields.Float()
    factor = fields.Float()
    offset = fields.Float()
    value = fields.String()

    @post_load
    def make_si_unit(self, data, **kwargs):
        return SIUnit(**data)


class UnitSchema(Schema):
    label = fields.String()
    quantity = fields.String()
    SIUnit = fields.Nested(SIUnitSchema)


class AutoIncrementedValueSetSchema(Schema):
    startValue = fields.Method(
        "serializeValue", deserialize="deserializeValue")
    increment = fields.Method("serializeValue", deserialize="deserializeValue")

    def serializeValue(self, obj):
        return(obj)

    def deserializeValue(self, values):
        return(values)

    @post_load
    def make_tuple(self, data, **kwargs):
        return (data["startValue"], data["increment"])


class SeriesSchema(Schema):
    name = fields.String()
    seriesType = fields.String()
    dependency = fields.String()
    seriesID = fields.String()
    plotScale = fields.String()
    visible = fields.Bool()
    IndividualValueSets = fields.Method(
        "serializeValue", deserialize="deserializeValue")
    EncodedValueSets = fields.List(fields.List(fields.String()))
    AutoIncrementedValueSets = fields.List(fields.Dict(
        increment=fields.Float(), startValue=fields.Float()))
    Unit = fields.Nested(UnitSchema)

    def serializeValue(self, obj):
        try:
            return obj.IndividualValueSets
        except AttributeError:
            pass

    def deserializeValue(self, value):
        return value

    @post_load
    def make_series(self, data, **kwargs):
        return Series(**data)

    @post_dump
    def remove_none_set(self, data, **kwargs):
        if data["IndividualValueSets"] is None:
            data.pop("IndividualValueSets", None)
        return data


class SeriesSetSchema(Schema):
    length = fields.Int()
    name = fields.String()
    Series = fields.Nested(SeriesSchema, many=True)

    @post_load
    def make_seriesset(self, data, **kwargs):
        return SeriesSet(**data)


class CategorySchema(Schema):
    name = fields.String()
    Parameters = fields.Nested(ParameterSchema, many=True)
    SeriesSets = fields.Nested(SeriesSetSchema, many=True)
    Categories = fields.Nested('self', many=True)

    @post_load
    def make_category(self, data, **kwargs):
        return Category(**data)


class MethodSchema(Schema):
    name = fields.String()
    Author = fields.Nested(AuthorSchema)
    Device = fields.Nested(DeviceSchema)
    Categories = fields.Nested(CategorySchema, many=True)

    @post_load
    def make_method(self, data, **kwargs):
        return Method(**data)


class SampleReferenceSchema(Schema):
    sampleID = fields.String()
    samplePurpose = fields.String()
    role = fields.String()

    @post_load
    def make_sample_reference(self, data, **kwargs):
        return SampleReference(**data)


class ExperimentStepReferenceSchema(Schema):
    experimentStepID = fields.String()
    dataPurpose = fields.String()
    role = fields.String()

    @post_load
    def make_experimentstep_reference(self, data, **kwargs):
        return ExperimentStepReference(**data)


class InfrastructureSchema(Schema):
    Timestamp = fields.DateTime()
    SampleReferenceSet = fields.Nested(SampleReferenceSchema, many=True)
    ExperimentStepReferenceSet = fields.Nested(
        ExperimentStepReferenceSchema, many=True)

    @post_load
    def make_infrastructure(self, data, **kwargs):
        return Infrastructure(**data)


class ResultsSchema(Schema):
    name = fields.String()
    SeriesSet = fields.Nested(SeriesSetSchema)
    Categories = fields.Nested(CategorySchema, many=True)

    @post_load
    def make_result(self, data, **kwargs):
        return Result(**data)


class SampleSchema(Schema):
    name = fields.String()
    sampleID = fields.String()
    barcode = fields.String()
    comment = fields.String()
    TagSet = fields.Dict(keys=fields.Str(), values=fields.Str())
    sourceDataLocation = fields.String()
    derived = fields.Bool()
    containerType = fields.String()
    containerID = fields.String()
    locationInContainer = fields.String()
    Categories = fields.Nested(CategorySchema, many=True)

    @post_load
    def make_sample(self, data, **kwargs):
        return Sample(**data)


class ExperimentStepSchema(Schema):
    name = fields.String()
    experimentStepID = fields.String()
    TagSet = fields.Dict(keys=fields.Str(), values=fields.Str())
    sourceDataLocation = fields.String()
    comment = fields.String()
    templateUsed = fields.String()
    Infrastructure = fields.Nested(InfrastructureSchema)
    Method = fields.Nested(MethodSchema)
    Results = fields.Nested(ResultsSchema, many=True)

    @post_load
    def make_experiment_step(self, data, **kwargs):
        return ExperimentStep(**data)


class JaniMLSchema(Schema):
    SampleSet = fields.Nested(SampleSchema, many=True)
    ExperimentStepSet = fields.Nested(ExperimentStepSchema, many=True)
    SignatureSet = fields.List(fields.String())

    @post_load
    def make_janiml(self, data, **kwargs):
        return JaniML(**data)
