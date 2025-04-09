import pymupdf
from PIL import Image
import io
import tiktoken
from llm_utility import LLMUtility
import json
from io import BytesIO
import zipfile
import os
import threading
import time


class ProcessPDF:
    def __init__(self):
        self.lLMUtility = LLMUtility()

    def clean_json_markdown_block(self, s):
        return s.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()


    def process(self, pdf_path=None, file_data=None, img_flag=True):
        text, images, image_names = self.extract_pdf(pdf_path, file_data, img_flag=img_flag, max_img_size=5)
        token_count = self.count_tokens(text)
        print("Token count:", token_count)
        ts_step_1 = self.lLMUtility.troubelshooting_step1(text)
        clean_json_string = self.clean_json_markdown_block(ts_step_1)
        ts_python_dict = json.loads(clean_json_string)

        how_to_step_1 = self.lLMUtility.howto_step1(text)
        clean_json_string = self.clean_json_markdown_block(how_to_step_1)
        how_to_python_dict = json.loads(clean_json_string)

        full_problem_list = ts_python_dict + how_to_python_dict

        step_2 = self.lLMUtility.troubelshooting_step2(text, full_problem_list)

        step_3 = self.lLMUtility.troubelshooting_step3(text, step_2)

        clean_json_string = self.clean_json_markdown_block(step_3)
        full_problem_list_python_dict = json.loads(clean_json_string)
        # TODO: Check if it is sufficent, if not ask again to verify the list
        return {"data": full_problem_list_python_dict, "image_names": image_names}, images



    def count_tokens(self, text):
        encoding = tiktoken.encoding_for_model("gpt-4o")

        tokens = encoding.encode(text)
        return len(tokens)
    
    def compress_to_target_size(self, img, target_size_mb):

        quality = 95
        while quality > 10:
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=quality)
            size_mb = len(buffer.getvalue()) / 1024 / 1024
            if size_mb <= target_size_mb:
                print(f"Reached {size_mb:.2f} MB at quality {quality}")
                buffer.seek(0)
                return buffer
            quality -= 5
        print("Could not compress image")
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=10)
        buffer.seek(0)
        return buffer
    
    def delete_file_later(self, file_path: str, delay_seconds: int = 1800):
        def delete_file():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"[{time.ctime()}] Deleted file: {file_path}")
            except Exception as e:
                print(f"Error deleting file: {e}")

        threading.Timer(delay_seconds, delete_file).start()
    
    def create_images_zip(self, image_buffers, username):
         # Create a zip in memory
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for filename, buffer in image_buffers.items():
                buffer.seek(0)
                zip_file.writestr(filename, buffer.read())

        zip_buffer.seek(0)

        # Save to disk inside container (e.g., /app folder)
        zip_path = os.path.join("app", "zip", f"{username}.zip")  # or use "." for current dir
        os.makedirs(os.path.dirname(zip_path), exist_ok=True)
        with open(zip_path, "wb") as f:
            f.write(zip_buffer.read())

        self.delete_file_later(zip_path, delay_seconds=1800)  # 1800 seconds = 30 minutes
        
        return zip_path
        
        
    
    def extract_pdf_data(self, doc, img_flag=False, max_img_size=5): # max_img_size mb
        text = ""
        images = {}
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
                    if image.format == 'PNG':
                        image = image.convert("RGB")
                        image_ext = "jpeg"

                    #image = self.compress_to_target_size(image, max_img_size) # compress image to 5mb
                    buffer = BytesIO()
                    image.save(buffer, format="JPEG", quality=100)
                    buffer.seek(0)

                    img_name = f"image_page_{page_num+1}_{img_index}.{image_ext}"
                    images[img_name] = buffer
                    image_names.append(img_name)
        
        return text, images, image_names


    def extract_pdf(self, pdf_path=None, file_data=None, img_flag=False, max_img_size=5):
        
        if pdf_path:
            with pymupdf.open(pdf_path) as doc:
                return self.extract_pdf_data(doc, img_flag, max_img_size)
        else:
            with pymupdf.open(stream=file_data, filetype="pdf") as doc:
                return self.extract_pdf_data(doc, img_flag, max_img_size)            
    
if __name__ == "__main__":
    processPDF = ProcessPDF()
    processPDF.process(pdf_path=f"C:\\Users\\JineshKallunkathariy\\Downloads\\User_Manual_ActiPower-4-PDU_ENG_screen.pdf")
