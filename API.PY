# old
import openai

openai.api_key = os.environ['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']

# new
from openai import OpenAI

client = OpenAI(
  api_key=os.environ['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'],  # this is also the default, it can be omitted
)