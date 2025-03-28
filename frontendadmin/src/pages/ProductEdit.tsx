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
  console.log(location);

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
    if (data?.status === 200) {
      sestProductData(data?.productData?.data || []);
    }
  }

  useEffect(() => {
    const locationArray = location?.pathname.split("/");
    const productName = locationArray[locationArray.length - 1];
    loadDataFromProductName(token, productName);
  }, [location, token]);
  return (
    <section>
      <h2 className="title">{`${t("editProduct")}-${
        currentProduct?.product
      }`}</h2>
      {productData.length > 0 && (
        <ProblemList problemList={productData}></ProblemList>
      )}
    </section>
  );
}

export default ProductEdit;
