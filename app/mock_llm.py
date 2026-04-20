from __future__ import annotations

import random
import time
from dataclasses import dataclass

from .incidents import STATE


@dataclass
class FakeUsage:
    input_tokens: int
    output_tokens: int


@dataclass
class FakeResponse:
    text: str
    usage: FakeUsage
    model: str


class FakeLLM:
    def __init__(self, model: str = "vinfast-assistant-v1") -> None:
        self.model = model

    def generate(self, prompt: str) -> FakeResponse:
        time.sleep(0.15)

        input_tokens = max(20, len(prompt) // 4)
        output_tokens = random.randint(80, 150)

        if STATE["cost_spike"]:
            output_tokens *= 4

        prompt_lower = prompt.lower()

        # ===== RULE-BASED RESPONSES =====
        if "dưới 300" in prompt_lower or "giá rẻ" in prompt_lower:
            answer = "Bạn có thể tham khảo VinFast VF 3, đây là dòng xe mini với giá khoảng 302 triệu, phù hợp nhu cầu giá rẻ."

        elif "vf 5" in prompt_lower:
            answer = "VinFast VF 5 có giá khoảng 529 triệu và thường có ưu đãi giảm 6% tùy chương trình."

        elif "vf e34" in prompt_lower:
            answer = "VinFast VF e34 là xe phù hợp đi trong đô thị, thiết kế nhỏ gọn và tiện lợi."

        elif "vf 6" in prompt_lower and "vf 7" in prompt_lower:
            answer = "VF 6 có giá khoảng 689 triệu, VF 7 khoảng 789 triệu, cả hai có kích thước SUV nhưng VF 7 lớn hơn."

        elif "300 km" in prompt_lower:
            answer = "VinFast Herio có thể chạy khoảng 326 km mỗi lần sạc, phù hợp nhu cầu di chuyển xa."

        elif "vf 8" in prompt_lower:
            answer = "VinFast VF 8 thuộc phân khúc SUV và có giá từ khoảng 1.019 tỷ đồng."

        elif "vf 9" in prompt_lower:
            answer = "VinFast VF 9 có 3 hàng ghế và 6 chỗ ngồi, phù hợp gia đình lớn."

        elif "dịch vụ" in prompt_lower:
            answer = "VinFast EC Van là lựa chọn phù hợp cho dịch vụ vận tải với khả năng tải hàng tốt."

        elif "nhỏ gọn" in prompt_lower:
            answer = "Bạn nên chọn VinFast VF 3, đây là xe điện nhỏ gọn rất phù hợp đi trong thành phố."

        elif "vf 3" in prompt_lower:
            answer = "VinFast VF 3 có giá khoảng 302 triệu và đi được khoảng 210 km mỗi lần sạc."

        else:
            answer = "VinFast có nhiều dòng xe điện phù hợp nhu cầu khác nhau, bạn có thể cân nhắc VF 3, VF 5 hoặc VF 6."

        return FakeResponse(
            text=answer,
            usage=FakeUsage(input_tokens, output_tokens),
            model=self.model,
        )