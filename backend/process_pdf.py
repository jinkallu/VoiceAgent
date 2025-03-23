import pymupdf
from PIL import Image
import io
import tiktoken
from llm_utility import LLMUtility

class ProcessPDF:
    def __init__(self):
        self.lLMUtility = LLMUtility()

    def process(self, pdf_path):
        text, images = self.extract_pdf(pdf_path, img_flag=True)
        token_count = self.count_tokens(text)
        print("Token count:", token_count)
        step_1 = self.lLMUtility.troubelshooting_step1(text)
        step_2 = self.lLMUtility.troubelshooting_step2(text, step_1)
        step_3 = self.lLMUtility.troubelshooting_step3(text, step_2)
        print(step_3)



    def count_tokens(self, text):
        encoding = tiktoken.encoding_for_model("gpt-4o")

        tokens = encoding.encode(text)
        return len(tokens)

    def extract_pdf(self, pdf_path, img_flag=False):
        text = ""
        images = []
        with pymupdf.open(pdf_path) as doc:
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


        return text, images
            
    
if __name__ == "__main__":
    processPDF = ProcessPDF()
    processPDF.process(f"C:\\Users\\Jinesh\\Downloads\\User_Manual_ActiPower-4-PDU_ENG_screen.pdf")
