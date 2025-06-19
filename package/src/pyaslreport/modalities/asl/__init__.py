from . import processor, validator
from pyaslreport.modalities.registry import register_modality

register_modality(
    name="asl",
    processor_cls=processor.ASLProcessor,
    validator_cls=validator.ASLValidator
)