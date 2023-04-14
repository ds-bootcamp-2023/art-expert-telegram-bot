from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import httpx
from httpx import AsyncClient
from pydantic import BaseModel

InputFileType = bytes | BytesIO


@dataclass
class HuggingFaceModelsClient:
    hugging_face_api_url: str
    hugging_face_token: str
    httpx_client: AsyncClient
    timeout: int

    async def generate_caption_for_image(self, image_bytes: InputFileType) -> str:
        resp = await self.httpx_client.post(
            f"{self.hugging_face_api_url}/models/nlpconnect/vit-gpt2-image-captioning",
            content=image_bytes,
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.json()[0]["generated_text"]

    async def generate_image_by_caption(self, caption: str) -> bytes:
        resp = await self.httpx_client.post(
            f"{self.hugging_face_api_url}/models/runwayml/stable-diffusion-v1-5",
            json={"inputs": caption},
            timeout=self.timeout,
        )
        resp.raise_for_status()
        return resp.content
