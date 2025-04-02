import { useState } from "react";
import Button from "./UI/button/Button";
import { uploadPDF } from "../services/apiService";
import { useAdminStore } from "../store/zustand/store";
import LoadingSpinner from "./UI/loadingSpinner/LoadingSpinner";
import { ITSList } from "../interfaces/generic";
interface props {
  pdfProblems: ITSList[] | [];
  setPdfProblems: (val: ITSList[] | []) => void;
  isAppendMode: boolean;
  setIsAppendMode: (val: boolean) => void;
  setProductData: (val: ITSList[]) => void;
  productData: ITSList[];
}

function PDFHandler({
  pdfProblems,
  setPdfProblems,
  productData,
  isAppendMode,
  setIsAppendMode,
  setProductData,
}: props) {
  const [selectedFile, setSelectedFile] = useState<File | null>();
  const token = useAdminStore((state) => state.token);
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
      setIsLoading(true);
      const res = await uploadPDF(token, formData);
      setIsLoading(false);
      console.log(res);

      if (
        res &&
        res?.status === 200 &&
        res?.data?.data &&
        res?.data?.data.length > 0
      ) {
        const newData = res?.data?.data?.map((item: any) => {
          const newSteps =
            item?.steps?.map((stepItem: string) => ({ step: stepItem })) || [];
          return { problem: item.problem, steps: newSteps };
        });
        if (isAppendMode) {
          setProductData([...productData, ...newData]);
        } else {
          setProductData(newData);
        }
        // setPdfProblems(newData);
      }
    }

    // Details of the uploaded file

    // Request made to the backend api
    // Send formData object
  };

  return (
    <div>
      <input
        type="file"
        name="fileIn"
        onChange={onFileChange}
        accept="application/pdf"
      ></input>
      <Button onClick={onFileUpload}>Upload</Button>
      <div style={{ display: "flex", alignItems: "center" }}>
        <Button outline onClick={() => setIsAppendMode(!isAppendMode)}>
          Choose Mode
        </Button>
        <h3>{isAppendMode ? "Append" : "Overwrite"}</h3>
      </div>
      {isLoading && <LoadingSpinner></LoadingSpinner>}

      {isLoading && (
        <h4>Please wait .. Proessing can take a couple of minutes..!</h4>
      )}
    </div>
  );
}

export default PDFHandler;
