import os
import numpy as np
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

class ASR:
    def __init__(self):
        self.model_path = os.path.join(os.getcwd(), "checkpoints/SenseVoiceSmall")
        # self.model_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
        self.sense_model = AutoModel(
            model=self.model_path,
            device="cpu",
            disable_update=True,
            disable_pbar=True,
            # vad_model="fsmn-vad",
            # vad_model_version="v2.0.4",
            # vad_kwargs={"max_single_segment_time": 3000},
            # punc_model="ct-punc-c",
            # punc_model_revision="v2.0.4",
        )
        self.cache = {}

    async def on_audio_frame(self, frame) -> str | None:
        adjusted_length = len(frame) - (len(frame) % 2)
        frame_fp32 = (
            np.frombuffer(frame[:adjusted_length], dtype=np.int16).astype(np.float32)
            / 32768
        )
        return self.__generate_text(frame_fp32)
    
    def audio_frame(self, frame):
        adjusted_length = len(frame) - (len(frame) % 2)
        frame_fp32 = (
            np.frombuffer(frame[:adjusted_length], dtype=np.int16).astype(np.float32)
            / 32768
        )
        return self.__generate_text(frame_fp32)

    def __generate_text(self, audio_buffer):
        """
        将音频缓冲区的语音转换为文本

        使用sense_model模型将音频数据转换成文本。
        参数说明:
        - input: 输入的音频数据(self.audio_buffer)
        - cache: 模型缓存，这里使用空字典
        - language: 设置语言为中文
        - use_itn: 启用智能文本规范化

        返回值:
        str: 经过后处理的识别文本结果
        """
        result = self.sense_model.generate(
            input=audio_buffer,
            cache=self.cache,
            language="auto",
            use_itn=True,
            # batch_size_s=60,
            # merge_vad=True,  #
            # merge_length_s=15,
        )
        return rich_transcription_postprocess(result[0]["text"])
