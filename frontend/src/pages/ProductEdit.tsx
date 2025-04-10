import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import useFetch from "../hook/useFetch";
import { useLocation, useParams } from "react-router-dom";
import EditProduct from "../components/edit/editProduct/EditProduct";
import { IProductsTable } from "../interfaces/Itable";
import { products } from "../constants/tables";
import LoadingSpinner from "../components/UI/loadingSpinner/LoadingSpinner";
import { useAdminStore } from "../store/zustand/store";
import {
  getDataFromProductName,
  uploadProductData,
  downloadZip
} from "../services/apiService";
import ProblemList from "../components/problemList";
import { ITSList } from "../interfaces/generic";
import Button from "../components/UI/button/Button";
import Modal from "../components/UI/modal/Modal";
import NewProblem from "../components/newProblem";
import PDFHandler from "../components/pdfHandler";

function ProductEdit() {
  const { t } = useTranslation();
  const token = useAdminStore((state) => state.token);
  const location = useLocation();
  const [productData, setProductData] = useState<ITSList[] | []>([]);
  const [loadingProductData, setLoadingProductData] = useState<boolean>(false);
  const [productName, sestProductName] = useState<string>("");
  const [editable, setEditable] = useState<boolean>(false);
  const [newProblem, setNewProblem] = useState<boolean>(false);
  const [selectedProblem, setSelectedProblem] = useState<ITSList>();
  const [uploadEnabled, setUploadEnabled] = useState<boolean>(false);
  const [pdfProblems, setPdfProblems] = useState<ITSList[] | []>([]);
  const [isAppendMode, setIsAppendMode] = useState<boolean>(true);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [zipEnabled, setZipEnabled] = useState<boolean>(false);

  // const { data, error, status } = useFetch<IProductsTable>(
  //   `${url}/${productId}.json`
  // );

  // if (status === "loading") {
  //   productEdit = <LoadingSpinner />;
  // }

  // if (error) {
  //   productEdit = <EditProduct product={productInfo} />;
  // }

  // if (status === "fetched" && data) {
  //   productEdit = <EditProduct product={data} />;
  // }

  async function downloadZipImg(token: string) {
    setZipEnabled(false);
    const data = await downloadZip(token);

  }

  async function loadDataFromProductName(token: string, product_name: string) {
    setLoadingProductData(true);
    const data = await getDataFromProductName(token, product_name);
    if (data?.status === 200) {
      setProductData(data?.productData || []);
    }
    setLoadingProductData(false);
  }

  const deleteProblem = async (problem: string) => {
    const newProductData: ITSList[] = productData?.filter(
      (item) => item.problem !== problem
    );
    uploadProductData(token, productName, newProductData);
    setProductData(newProductData);
  };
  const uploadToAzure = async (productData: ITSList[]) => {
    const res = await uploadProductData(token, productName, productData);
    if (res?.status === 200) {
      console.log("success");
    } else {
      console.log("error");
    }
    loadDataFromProductName(token, productName || "");
  };
  const addTSStep = (tsStep: ITSList) => {
    setIsLoading(true);
    const newData: ITSList[] = [...productData];
    if (selectedProblem) {
      const index = newData?.findIndex(
        (item) => item.problem === selectedProblem.problem
      );
      newData[index] = tsStep;
    } else {
      newData.push(tsStep);
    }
    uploadToAzure(newData);
    setProductData(newData);
    setIsLoading(false);
  };

  const openEditProblem = (data: ITSList) => {
    setSelectedProblem(data);
    setNewProblem(true);
  };

  useEffect(() => {
    const locationArray = location?.pathname.split("/");
    const productName = decodeURIComponent(locationArray[locationArray.length - 1]);

    sestProductName(productName);
    loadDataFromProductName(token, productName);
  }, [location, token]);
  return (
    <section style={{ maxHeight: "80vh", overflowY: "auto" }}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          width: "100%",
          marginBottom: "10px",
          gap: "10px",
        }}
      >
        <h3>{productName}</h3>
        <div style={{ width: "70%" }}>
          <h5>
            You can find a list of problems and their trouble shooting steps
            here.Click the expand icon to view the steps. To add a new problem
            or edit an existing problem, click the edit button.
          </h5>
        </div>
      </div>

      {newProblem && (
        <Modal
          title={productName}
          onConfirm={() => {
            setNewProblem((prev) => !prev);
          }}
        >
          <NewProblem
            isLoading={isLoading}
            productName={productName}
            data={selectedProblem}
            addTSStep={addTSStep}
            setNewProblem={setNewProblem}
          ></NewProblem>
        </Modal>
      )}
      <div
        style={{
          paddingTop: "5px",
          paddingBottom: "10px",
          display: "flex",
          marginBottom: "10px",
          justifyContent: "flex-end",
          alignItems: "center",
          width: "100%",
        }}
      >
        {editable && (
          <div>
            <Button onClick={() => setNewProblem(true)}>New Problem</Button>
            <Button onClick={() => setUploadEnabled(true)}>
              Import From PDF
            </Button>
            {zipEnabled && (
              <Button onClick={() => downloadZipImg(token)}>Download PDF Images</Button>
            )}
          </div>
        )}

        {/* {editable && (
          <Button outline onClick={() => uploadToAzure(productData)}>
            Save Changes
          </Button>
        )} */}

        <Button onClick={() => setEditable((prev) => !prev)}>
          {`${editable ? "Cancel Edit" : "Edit"}`}
        </Button>
      </div>

      {uploadEnabled && (
        <Modal
          title="Import From PDF"
          onConfirm={() => {
            setUploadEnabled(false);
          }}
        >
          <PDFHandler
            productName={productName}
            productData={productData}
            setProductData={setProductData}
            isAppendMode={isAppendMode}
            setIsAppendMode={setIsAppendMode}
            pdfProblems={pdfProblems}
            setPdfProblems={setPdfProblems}
            setUploadEnabled={setUploadEnabled}
            setZipEnabled={setZipEnabled}
          ></PDFHandler>
        </Modal>
      )}
      {loadingProductData && <LoadingSpinner></LoadingSpinner>}
      {productData.length > 0 && productName && (
        <ProblemList
          editable={editable}
          problemList={productData}
          productName={productName}
          deleteProblem={deleteProblem}
          openEditProblem={openEditProblem}
        ></ProblemList>
      )}
    </section>
  );
}

export default ProductEdit;
