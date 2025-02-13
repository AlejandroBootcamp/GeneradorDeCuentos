from openai import OpenAI


class Modelo:
    def __init__(self,api_key, model, base_url):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.api = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate_tale(self,prompt):
        cleaned_prompt = self.clean_prompt(prompt)
        completion = self.api.chat.completions.create(  ##funcion openAI Petición POST
            model= self.model,
            messages=[
                {"role": "system",
                 "content": "Eres un generador de cuentos cortos.Vas a crear cuentos infantiles breves con un género y protagonista determinados. El máximo que debe ocupar el cuento son dos párrafos."},

                {"role": "user", "content": cleaned_prompt},
            ],
            temperature=0.7,  ## aleatoriedad creatividad/respuesta
            max_tokens=4096,  ## limite
        )

        response = completion.choices[0].message.content
        return response
    
    def clean_prompt(self,prompt):
        prompt = prompt.strip()
        prompt = prompt.capitalize()
        return prompt
