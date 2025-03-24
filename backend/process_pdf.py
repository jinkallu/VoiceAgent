import pymupdf
from PIL import Image
import io
import tiktoken
from llm_utility import LLMUtility
import json

class ProcessPDF:
    def __init__(self):
        self.lLMUtility = LLMUtility()

    def clean_json_markdown_block(self, s):
        return s.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()


    def process(self, pdf_path=None, file_data=None):
        text, images, image_names = self.extract_pdf(pdf_path, file_data, img_flag=True)
        token_count = self.count_tokens(text)
        print("Token count:", token_count)
        ts_step_1 = self.lLMUtility.troubelshooting_step1(text)
        clean_json_string = self.clean_json_markdown_block(ts_step_1)
        ts_python_dict = json.loads(clean_json_string)

        how_to_step_1 = self.lLMUtility.howto_step1(text)
        clean_json_string = self.clean_json_markdown_block(how_to_step_1)
        how_to_python_dict = json.loads(clean_json_string)

        full_problem_list = ts_python_dict + how_to_python_dict
        print(len(full_problem_list))
        print(full_problem_list)

        step_2 = self.lLMUtility.troubelshooting_step2(text, full_problem_list)
        print(len(step_2))
        print(step_2)

        step_3 = self.lLMUtility.troubelshooting_step3(text, step_2)
        print(len(step_3))
        print(step_3)

        clean_json_string = self.clean_json_markdown_block(step_3)
        full_problem_list_python_dict = json.loads(clean_json_string)
        # TODO: Check if it is sufficent, if not ask again to verify the list
        return {"data": full_problem_list_python_dict, "image_names": image_names}, images



    def count_tokens(self, text):
        encoding = tiktoken.encoding_for_model("gpt-4o")

        tokens = encoding.encode(text)
        return len(tokens)
    
    def extract_pdf_data(self, doc, img_flag=False):
        text = ""
        images = []
        image_names = []

        for page_num in range(len(doc)):
            text += doc[page_num].get_text()
            if img_flag:
                for img_index, img in enumerate(doc[page_num].get_images(full=True)):
                    xref = img[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]

                    # Convert to high-quality PIL image
                    image = Image.open(io.BytesIO(image_bytes))
                    img_name = f"image_page{page_num+1}_{img_index}.{image_ext}"
                    images.append({img_name: image})
                    image_names.append(img_name)
        
        return text, images, image_names


    def extract_pdf(self, pdf_path=None, file_data=None, img_flag=False):
        
        if pdf_path:
            with pymupdf.open(pdf_path) as doc:
                return self.extract_pdf_data(doc, img_flag)
        else:
            with pymupdf.open(stream=file_data, filetype="pdf") as doc:
                return self.extract_pdf_data(doc, img_flag)            
    
if __name__ == "__main__":
    processPDF = ProcessPDF()
    processPDF.process(pdf_path=f"C:\\Users\\JineshKallunkathariy\\Downloads\\User_Manual_ActiPower-4-PDU_ENG_screen.pdf")
