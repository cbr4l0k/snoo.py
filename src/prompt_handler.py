import os
import json
import tiktoken
from hashlib import sha256
from dotenv import load_dotenv

load_dotenv()
OUTPUTS_PATH = os.getenv("OUTPUTS_PATH")


class PromptHandler:

    def __init__(self, model_name: str):
        self.initial_files_report = None
        self.load_initial_filesreport()

        self.prompts = {0: {"template": """Identify which dependencies the file uses and do a brief explanation of what the file contains.
                                           Context we have this tree files:
                                            {}
                                """.format(self.initial_files_report) +
                                """                          
                                You must return a json with this fields:
                                    "dependencies": [list of dependencies names, external libraries as 'ext/library' and internal
                                    libraries as 'int/library' are accepted, for example: 'ext/numpy', 'int/my_library/plotter'],
                                    "explanation": 'short code explanation highlighting ONLY: main features, key classes, functions 
                                    and methods, if makes sense infer behavior from method names'""

                                For identifying the dependencies you must:
                                    1. Look at the context of the file tree.
                                    2. Idenfitify the dependencies of the file.
                                    3. Check if any identified dependency in the code is or not in the file tree. 
                                       A dependency is internal if for example the code says: 'from my_library.sub_lib import module' 
                                       and there is a folder named 'my_library' in the file tree and a folder or file named 'sub_lib'.
                                    4. If the dependency is not in the file tree, it's external and shuld be written as 'ext/library'
                                       or 'ext/library/sublibrary' and so on. 
                                    5. If the dependency is in the file tree, it's internal and should be written as 'int/library'
                                       or 'int/library/sublibrary' and so on.

                                 give me the json only, give me a well formated json, be short and concise, don't forget,
                                 the (int or ext)/lib structure, use the file tree as context. Maximum of 60 words as explaination.
                                 Code received: 
                                 
                                 {code}

                                 Think on your response, if for example you have 'from yada.yada.yodo import yuda' don't write
                                 'yada.yada.yodo' as dependency, write 'yada/yada/yodo', 'yada.yada.yodo' is wrong. 
                                 YOUR JSON RESPONSE GOES HERE:""",
                            "input_variables": ["code", ],
                            "prompt_token_lenght": -1
                            },
                        1: {"template": """Given this new fragment of code of a bigger file, identify which dependencies the file uses and do
                                           a brief explanation of what the file contains. 
                                           Context we have this tree files:
                                           {}
                                """.format(self.initial_files_report) +
                                """
                                    You must return a json with this fields:
                                        "dependencies": [list of dependencies names, external libraries as 'ext/library' and internal
                                        libraries as 'int/library' are accepted, for example: 'ext/numpy', 'int/my_library/plotter'],
                                        "explanation": 'short code explanation highlighting ONLY: main features, key classes, functions 
                                        and methods, if makes sense infer behavior from method names'""

                                    For identifying the dependencies you must:
                                        1. Look at the context of the file tree.
                                        2. Idenfitify the dependencies of the file.
                                        3. Check if any identified dependency in the code is or not in the file tree. 
                                        A dependency is internal if for example the code says: 'from my_library.sub_lib import module' 
                                        and there is a folder named 'my_library' in the file tree and a folder or file named 'sub_lib'.
                                        4. If the dependency is not in the file tree, it's external and shuld be written as 'ext/library'
                                        or 'ext/library/sublibrary' and so on. 
                                        5. If the dependency is in the file tree, it's internal and should be written as 'int/library'
                                        or 'int/library/sublibrary' and so on.

                                    give me the json only, give me a well formated json, be short and concise, don't forget,
                                    the (int or ext)/lib structure, use the file tree as context. Maximum of 60 words as explaination.
                                    Code received: 

                                    {code}
                                            
                                    YOUR JSON RESPONSE GOES HERE:""",
                            "input_variables": ["code", ],
                            "prompt_token_lenght": -1
                            },
                        2: {"template": """Now that you have identified the dependencies and the explanation of the file in different
                                           json chunks, you must unify the dependencies and explanations in a single json file.
                                           You are a pro bot developer and can take into account that the dependencies and explanations
                                           don't have repeated values. 
                                           
                                           You must return a json with this fields:

                                           "dependencies": [list of dependencies names, external libraries as 'ext/library' and internal
                                           libraries as 'int/library' are accepted, for example: 'ext/numpy', 'int/my_library/plotter', 
                                           include imports like 'from lib import something',
                                           if 'from lib import something' write it as '(int or ext)/lib', 
                                           if 'from lib.sublib import something' write it as '(int or ext)/lib.sublib' and so on],
                                           "explanation": 'short code explanation highlighting ONLY: main features, key classes, functions 
                                           and methods, if makes sense infer behavior from method names. This explaination condenses the
                                           other explainations and takes the knowledge of all of them.'""

                                           Make sure to give the dependencies in the desired form '(int or ext)/dependency'.
                                           Check for errors and fix them. Maximum of 60 words as explaination.
                                           Jsons reports received: 
                                           
                                           {json_reports}
                                            
                                           YOUR JSON RESPONSE GOES HERE: """,
                            "input_variables": ["json_reports", ],
                            "prompt_token_lenght": -1
                            },
                        3: {"template": """Given this python analysis file of a project, identify the level of coupling in the project and
                                           the level of cohesion in the project. You must explain your answer, the reason why you think
                                           the project has that level of coupling and cohesion. You must return a json with this fields: 
                            
                                           "coupling": 'low, medium or high, and the reason why you think the project has that level of coupling',
                                           "cohesion": 'low, medium or high, and the reason why you think the project has that level of cohesion'
                                           "explanation":'short explanation of why you think the project has that level of coupling and cohesion, 
                                                          also explain if this is a good thing or a bad thing, and why. '""

                                            give me the json ONLY and dont forget to explain your desicion and it's implications, 
                                            terminate the json, give me a well formated json, be short and concise, File received: {json_reports}.

                                            JSON GOES HERE: """,
                            "input_variables": ["json_reports", ],
                            "prompt_token_lenght": -1
                            }, 
                         4: {"template": """You've been given a json with the fields 'dependencies' and 'explaination', your
                                            work is to correct the json response if needed and return it, you only have to change
                                            the 'dependencies' field, the 'explaination' field is correct.
                             
                                            You must return a json with this fields:

                                            For checking the dependencies you must:
                                                1. Look at the context of the file tree.
                                                2. Idenfitify the dependencies of the file.
                                                3. Check if any identified dependency in the code is or not in the file tree. 
                                                A dependency is internal if for example the code says: 'from my_library.sub_lib import module' 
                                                and there is a folder named 'my_library' in the file tree and a folder or file named 'sub_lib'.
                                                4. If the dependency is not in the file tree, it's external and shuld be written as 'ext/library'
                                                or 'ext/library/sublibrary' and so on. 
                                                5. If the dependency is in the file tree, it's internal and should be written as 'int/library'
                                                or 'int/library/sublibrary' and so on.

                                            The file tree is:
                                            {}""".format(self.initial_files_report) + """

                                            Think on your response, if for example you have 'from yada.yada.yodo import yuda' don't write
                                            'yada.yada.yodo' as dependency, write 'yada/yada/yodo', 'yada.yada.yodo' is wrong. 
                                            Adding the file extension is wrong, for example 'yada/yada/yodo.py' is wrong,
                                            'yada/yada/yodo' is correct. 

                                            Give me the json only, give me a well formated json, be short and concise, don't forget to leave
                                            the 'explaination' field as it is. Change the dependencies which end with '.file_extension' 
                                            to the correct form, delete the '.file_extension' part. 

                                            JSON GOES HERE: \n {json_reports}""",
                                            "input_variables": ["json_reports", ],
                                            "prompt_token_lenght": -1
                         },
                         5: {"template": """You've been given a json file with fields 'dependencies' and 'explaination' for a folder in a project,
                                            your task is to add an explaination field for the folders inside the json file. If a folder already has an
                                            explaination field, you must not change it. This is what the 'explaination' field should look like:
                             
                                            "explanation": 'short folder explaination condensing the logic, purpose and explainations of the 
                                            files inside the folder, if the folder already has an explaination, don't change it.'""

                                            You can identify a folder by the 'type' field, if the type is 'directory' then it's a folder, 
                                            and also if the folder has the 'contents' or 'children' field, it's a folder.
                                            This is the Json file you've been given:

                                            {json_reports} 
                             
                                            Remember to add only the 'explaination' field to the folders, without changing the 'dependencies' field, 
                                            and the other existing fields. End the json properly, with good formatting.
                                            YOUR JSON RESPONSE GOES HERE:
                                            """,    
                             "input_variables": ["json_reports", ],
                             "prompt_token_lenght": -1
                         }
                        }

        self.longest_prompt_lenght = -1
        self.set_model(model_name=model_name)
        self.set_largest_prompt_token_lenght()


    def load_initial_filesreport(self) -> None:
        """
            Loads the initial files report
        """
        with open(f"{OUTPUTS_PATH}filesreport.txt", "r") as f:
            self.initial_files_report = f.read()

    def set_largest_prompt_token_lenght(self) -> None:
        """
            Sets the largest prompt token lenght for all the templates
        """
        for template in self.prompts:
            if self.prompts[template]["prompt_token_lenght"] > self.longest_prompt_lenght:
                self.longest_prompt_lenght = self.prompts[template]["prompt_token_lenght"]

    def set_model(self, model_name: str) -> None:
        """
            Sets the model name and encoding for the prompt handler.
            And with that it gets the prompt token lenght for each template.
        """
        self.model_name = model_name
        self.encoding = tiktoken.encoding_for_model(self.model_name)
        self.set_token_lenght()

    def get_raw_template(self, template: int = 0) -> dict:
        """
            Returns the raw prompt for the given template
        """
        return self.prompts[template]

    def get_prompt(self, template: int = 0, **kwargs) -> str:
        """
            Returns the prompt for the given template,
            if the template has input variables, they must be passed as kwargs
        """
        return self.prompts[template]["template"].format(**kwargs)

    def get_prompt_token_lenght(self, prompt: str) -> int:
        """
            Returns the prompt token lenght for the given prompt
        """
        return len(self.encoding.encode(prompt))

    def set_token_lenght(self) -> None:
        """
            Sets the token lenght for all the templates using the current model encoding
        """

        for template in self.prompts:
            white_spaced_template = self.white_spaced_template(template=template)
            self.prompts[template]["prompt_token_lenght"] = len(self.encoding.encode(white_spaced_template))

    def white_spaced_template(self, template: int = 0) -> str:
        """
            Returns the template with all the input variables replaced by an empty string
        """
        dict_vars = {var: "" for var in self.prompts[template]["input_variables"]}
        return self.prompts[template]["template"].format(**dict_vars)