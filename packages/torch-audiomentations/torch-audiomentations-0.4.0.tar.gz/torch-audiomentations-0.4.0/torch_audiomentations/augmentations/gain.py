import torch
import typing

from ..core.transforms_interface import BaseWaveformTransform
from ..utils.dsp import convert_decibels_to_amplitude_ratio


class Gain(BaseWaveformTransform):
    """
    Multiply the audio by a random amplitude factor to reduce or increase the volume. This
    technique can help a model become somewhat invariant to the overall gain of the input audio.

    Warning: This transform can return samples outside the [-1, 1] range, which may lead to
    clipping or wrap distortion, depending on what you do with the audio in a later stage.
    See also https://en.wikipedia.org/wiki/Clipping_(audio)#Digital_clipping
    """

    supports_multichannel = True

    def __init__(
        self,
        min_gain_in_db: float = -18.0,
        max_gain_in_db: float = 6.0,
        mode: str = "per_example",
        p: float = 0.5,
        p_mode: typing.Optional[str] = None,
    ):
        super().__init__(mode, p, p_mode)
        self.min_gain_in_db = min_gain_in_db
        self.max_gain_in_db = max_gain_in_db
        if self.min_gain_in_db >= self.max_gain_in_db:
            raise ValueError("min_gain_in_db must be higher than max_gain_in_db")

    def randomize_parameters(self, selected_samples, sample_rate: int):
        distribution = torch.distributions.Uniform(
            low=torch.tensor(
                self.min_gain_in_db, dtype=torch.float32, device=selected_samples.device
            ),
            high=torch.tensor(
                self.max_gain_in_db, dtype=torch.float32, device=selected_samples.device
            ),
            validate_args=True,
        )
        selected_batch_size = selected_samples.size(0)
        self.parameters["gain_factors"] = convert_decibels_to_amplitude_ratio(
            distribution.sample(sample_shape=(selected_batch_size,))
        )

    def apply_transform(self, selected_samples, sample_rate: int):
        num_dimensions = len(selected_samples.shape)
        if num_dimensions == 1:
            # TODO: We shouldn't support this
            gain_factors = self.parameters["gain_factors"]
        elif num_dimensions == 2:
            gain_factors = self.parameters["gain_factors"].unsqueeze(1)
        elif num_dimensions == 3:
            gain_factors = self.parameters["gain_factors"].unsqueeze(1).unsqueeze(1)
        else:
            raise Exception(
                "Invalid number of dimensions ({}) in input tensor".format(num_dimensions)
            )
        return selected_samples * gain_factors
