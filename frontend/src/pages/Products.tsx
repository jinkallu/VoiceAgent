import React, { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";
import useFetch from "../hook/useFetch";
import CustomTable from "../components/tables/customTable/CustomTable";
import { IProductsTable } from "../interfaces/Itable";
import { productsHeader } from "../constants/tables";
import LoadingSpinner from "../components/UI/loadingSpinner/LoadingSpinner";
import Dropdown from "../components/UI/dropdown/Dropdown";
import { useAdminStore } from "../store/zustand/store";
import Button from "../components/UI/button/Button";
import { useNavigate } from "react-router-dom";
import Modal from "../components/UI/modal/Modal";
import CreateProduct from "../components/createProduct";

function Products() {
  const { t } = useTranslation();
  const products = useAdminStore((state) => state.products);
  const [createProduct, setCreateProduct] = useState<boolean>(false);

  // if (status === "loading") {
  //   productsTable = <LoadingSpinner />;
  // }

  //   //if fetch has error:
  //   //select data from local file ("../constants/tables.ts")
  //   switch (selected) {
  //     case "digital":
  //       tableData = products?.filter((item) => item.category === selected);
  //       break;
  //     case "clothing":
  //       tableData = products?.filter((item) => item.category === selected);
  //       break;
  //     case "beauty":
  //       tableData = products?.filter((item) => item.category === selected);
  //       break;
  //     default:
  //       tableData = products;
  //   }

  // productsTable = (
  //   <CustomTable
  //     selectedCategory={selected}
  //     headData={productsHeader}
  //     bodyData={tableData}
  //     limit={10}
  //   />
  // );
  // }

  return (
    <section>
      {createProduct && (
        <Modal
          title="Create New Product"
          onConfirm={() => {
            setCreateProduct(false);
          }}
        >
          <CreateProduct></CreateProduct>
        </Modal>
      )}
      <h2 className="title">{t("products")}</h2>
      <div
        style={{
          display: "flex",
          justifyContent: "flex-end",
          alignItems: "center",
          width: "100%",
        }}
      >
        <Button onClick={() => setCreateProduct(true)}>New Product</Button>
      </div>
      {/* <Dropdown
        dropdownData={dropdownOptions}
        onChange={selectedChangeHandler}
      /> */}
      {products?.length > 0 ? (
        <CustomTable
          headData={productsHeader}
          bodyData={products?.map((item: string, index: number) => ({
            product: item,
            ID: index + 1,
          }))}
          limit={10}
        />
      ) : (
        <div>
          <h3>No products to display. Add products to continue</h3>
        </div>
      )}
    </section>
  );
}

export default Products;
