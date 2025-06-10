from . import processor, validator
from package.modalities.registry import register_modality

register_modality(
    name="test-dsc",
    processor_cls=processor.DSCProcessor,
    validator_cls=validator.DSCValidator
)
