import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Itable as Props, complex } from "../../../interfaces/Itable";
import Card from "../../UI/card/Card";
import Badge from "../../UI/badge/Badge";
import Modal from "../../UI/modal/Modal";
import { useTranslation } from "react-i18next";
import { Icon } from "@iconify/react";
import classes from "./CustomTable.module.scss";
import { useAdminStore } from "../../../store/zustand/store";

const CustomTable: React.FC<Props> = (props) => {
  console.log(props);
  const [showModal, setShowModal] = useState(false);
  const setCurrentProduct = useAdminStore((state) => state.setCurrentProduct);
  function showModalHandler() {
    setShowModal((prev) => !prev);
  }
  function tableBody(item: complex, index: number) {
    /* type guard (in typescript) */
    return (
      <tr key={index}>
        <td>{item.ID}</td>
        <td className={classes.product_name}>{item.product}</td>
        <td className={classes.actions}>
          <Icon icon="charm:menu-kebab" />
          <div className={classes.actions__box}>
            <div className={classes.actions__delete} onClick={showModalHandler}>
              <Icon icon="fluent:delete-24-regular" width="24" />
            </div>
            <div className={classes.actions__edit}>
              <Link to={`/products/${item.product}`}>
                <Icon
                  onClick={() =>
                    setCurrentProduct({ ID: item.ID, product: item.product })
                  }
                  icon="fluent:edit-16-regular"
                  width="24"
                />
              </Link>
            </div>
          </div>
        </td>
      </tr>
    );
  }

  const initDataShow = () => {
    return props.limit && props.bodyData
      ? props.bodyData.slice(0, Number(props.limit))
      : props.bodyData;
  };

  const [dataShow, setDataShow] = useState(initDataShow);
  // const [selectedCategory, setSelectedCategory] = useState(
  //   props.selectedCategory
  // );

  // if (props.selectedCategory) {
  //   if (selectedCategory !== props.selectedCategory)
  //     setDataShow(props.bodyData);
  // }
  // setSelectedCategory(props.selectedCategory);

  let pages = 1;

  let range: number[] = [];

  if (props.limit !== undefined) {
    let page = Math.floor(props.bodyData.length / Number(props.limit));
    pages = props.bodyData.length % Number(props.limit) === 0 ? page : page + 1;
    range = [...Array(pages).keys()];
  }

  const [currPage, setCurrPage] = useState(0);

  const selectPage = (page: number) => {
    const start = Number(props.limit) * page;
    const end = start + Number(props.limit);

    setDataShow(props.bodyData?.slice(start, end));

    setCurrPage(page);
  };

  const { t } = useTranslation();

  useEffect(() => {
    setDataShow(initDataShow);
  }, [props.bodyData]);
  return (
    <>
      {/* modal for delete customer and product case*/}
      {showModal ? (
        <Modal
          title={t("deleteCustomer")}
          message={`${t("modalMessage")}`}
          onConfirm={showModalHandler}
        />
      ) : null}

      <div className={classes.container}>
        <Card>
          <div className={classes.wrapper}>
            <div className={classes.table__wrapper}>
              <table
                className={props.limit ? classes.largeTable : classes.table}
              >
                {props.headData ? (
                  <thead>
                    <tr>
                      {props.headData.map((item, index) => (
                        <th key={index}>{t(item)}</th>
                      ))}
                    </tr>
                  </thead>
                ) : null}
                <tbody>
                  {dataShow.map((item, index) => tableBody(item, index))}
                </tbody>
              </table>
            </div>

            {pages > 1 ? (
              <div className={classes.table__pagination}>
                {range.map((item, index) => (
                  <div
                    key={index}
                    className={`${classes.table__pagination_item} ${
                      currPage === index ? classes.active : ""
                    }`}
                    onClick={() => selectPage(index)}
                  >
                    {item + 1}
                  </div>
                ))}
              </div>
            ) : null}
          </div>
        </Card>
      </div>
    </>
  );
};

export default CustomTable;
