# tests/test_summary.py

from app.reasoning.llm import llm


text = """
Satellite-on-a-Chip (SAToC) is a technology
that integrates multiple satellite subsystems
into a single FPGA-based architecture.

The architecture includes:

- OBDH
- TT&C
- ADCS
- EPS

SpaceLab at UFSC has been developing
SAToC for future Brazilian space missions.
"""


prompt = f"""
Create a concise executive summary.

TEXT:

{text}
"""


response = llm.invoke(prompt)

print("\nSUMMARY\n")

print(response.content)