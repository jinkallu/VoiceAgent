import React, { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import useFetch from "../hook/useFetch";
import { useLocation, useParams } from "react-router-dom";
import EditProduct from "../components/edit/editProduct/EditProduct";
import { IProductsTable } from "../interfaces/Itable";
import { products } from "../constants/tables";
import LoadingSpinner from "../components/UI/loadingSpinner/LoadingSpinner";
import { useAdminStore } from "../store/zustand/store";
import { getDataFromProductName } from "../services/apiService";
import ProblemList from "../components/problemList";
import { ITSList } from "../interfaces/generic";
import { Icon } from "@iconify/react";
import Button from "../components/UI/button/Button";
import Modal from "../components/UI/modal/Modal";
import NewProblem from "../components/newProblem";

const url =
  "https://admin-panel-79c71-default-rtdb.europe-west1.firebasedatabase.app/products";
function ProductEdit() {
  const { t } = useTranslation();
  const params = useParams();
  let { productId } = params;
  const currentProduct = useAdminStore((state) => state.currentProduct);
  const token = useAdminStore((state) => state.token);
  const location = useLocation();
  const [productData, sestProductData] = useState<ITSList[] | []>([]);
  const [productName, sestProductName] = useState<string>();
  const [editable, setEditable] = useState<boolean>(false);
  const [newProblem, setNewProblem] = useState<boolean>(false);

  let productInfo: IProductsTable = products.filter(
    (item) => item.ID.toString() === productId
  )[0];

  let productEdit;

  const { data, error, status } = useFetch<IProductsTable>(
    `${url}/${productId}.json`
  );

  if (status === "loading") {
    productEdit = <LoadingSpinner />;
  }

  if (error) {
    productEdit = <EditProduct product={productInfo} />;
  }

  if (status === "fetched" && data) {
    productEdit = <EditProduct product={data} />;
  }

  async function loadDataFromProductName(token: string, product_name: string) {
    const data = await getDataFromProductName(token, product_name);
    console.log("....", data);
    if (data?.status === 200) {
      sestProductData(data?.productData || []);
    }
  }

  useEffect(() => {
    const locationArray = location?.pathname.split("/");
    const productName = locationArray[locationArray.length - 1];

    sestProductName(productName);
    loadDataFromProductName(token, productName);
  }, [location, token]);
  return (
    <section style={{ maxHeight: "100%", overflowY: "auto" }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          alignItems: "center",
        }}
      >
        <h2 className="title">{`${editable ? t("editProduct-") : ""}${
          currentProduct?.product
        }`}</h2>

        <Button onClick={() => setEditable((prev) => !prev)}>
          {`${editable ? "Cancel Edit" : "Edit"}`}
        </Button>
      </div>
      {newProblem && (
        <Modal
          title="New Proble"
          onConfirm={() => {
            setNewProblem((prev) => !prev);
          }}
        >
          <NewProblem></NewProblem>
        </Modal>
      )}
      {editable && (
        <div>
          <Button onClick={() => setNewProblem(true)}>New Problem</Button>
        </div>
      )}
      {productData.length > 0 && productName && (
        <ProblemList
          editable={editable}
          problemList={productData}
          productName={productName}
        ></ProblemList>
      )}
    </section>
  );
}

export default ProductEdit;
