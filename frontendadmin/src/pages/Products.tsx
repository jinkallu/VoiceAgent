import React, { useState, useRef, useEffect } from "react";
import { useTranslation } from "react-i18next";
import useFetch from "../hook/useFetch";
import CustomTable from "../components/tables/customTable/CustomTable";
import { IProductsTable } from "../interfaces/Itable";
import { productsHeader } from "../constants/tables";
import LoadingSpinner from "../components/UI/loadingSpinner/LoadingSpinner";
import Dropdown from "../components/UI/dropdown/Dropdown";
import { useAdminStore } from "../store/zustand/store";

function Products() {
  const { t } = useTranslation();
  const products = useAdminStore((state) => state.products);

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
      <h2 className="title">{t("products")}</h2>
      {/* <Dropdown
        dropdownData={dropdownOptions}
        onChange={selectedChangeHandler}
      /> */}
      <CustomTable
        headData={productsHeader}
        bodyData={products?.map((item: string, index: number) => ({
          product: item,
          ID: index + 1,
        }))}
        limit={10}
      />
    </section>
  );
}

export default Products;
