import { useState } from "react";
import Button from "./UI/button/Button";
import { uploadPDF } from "../services/apiService";
import { useAdminStore } from "../store/zustand/store";
import LoadingSpinner from "./UI/loadingSpinner/LoadingSpinner";
interface props {
  uploadSelectedImage: (val: FormData, fileName: string, step: string) => void;
  step: string;
}

function ImageHandler({ uploadSelectedImage, step }: props) {
  const [selectedFile, setSelectedFile] = useState<File | null>();
  const [isLoading, setIsLoading] = useState(false);

  const onFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    // Update the state
    if (!event.target.files) {
      setSelectedFile(null);
      return;
    }
    setSelectedFile(event.target.files[0]);
  };

  // On file upload (click the upload button)
  const onFileUpload = async () => {
    // Create an object of formData
    const formData = new FormData();

    // Update the formData object
    if (selectedFile) {
      formData.append("file", selectedFile);
      formData.append("fileb", selectedFile);
      console.log(selectedFile);
      setIsLoading(true);
      const res = await uploadSelectedImage(formData, selectedFile.name, step);
      setSelectedFile(null);
      setIsLoading(false);

      console.log(res);

      // setPdfProblems(newData);
    }
  };

  // Details of the uploaded file

  // Request made to the backend api
  // Send formData object

  return (
    <div>
      <input
        type="file"
        name="fileIn"
        onChange={onFileChange}
        accept="image/png, image/jpeg"
      ></input>
      <Button onClick={onFileUpload}>Upload</Button>
      <div style={{ display: "flex", alignItems: "center" }}>
        {isLoading && <LoadingSpinner></LoadingSpinner>}

        {isLoading && (
          <h4>Please wait .. Proessing can take a couple of minutes..!</h4>
        )}
      </div>
    </div>
  );
}

export default ImageHandler;
