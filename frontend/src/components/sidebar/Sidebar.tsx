import React, { useState, useEffect, useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import { useWindowSize } from "usehooks-ts";
import { useTranslation } from "react-i18next";
import { images } from "../../constants";
import sidebarNav from "../../config/sidebarNav";
import SidebarContext from "../../store/sidebarContext";
import LoginContext from "../../store/loginContext";
import { Icon } from "@iconify/react";
import classes from "./Sidebar.module.scss";
import { useAdminStore } from "../../store/zustand/store";
import { getProductsOfResourceGroup } from "../../services/apiService";
import LoadingSpinner from "../UI/loadingSpinner/LoadingSpinner";

function Sidebar() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [loadingProducts, setLoadingProducts] = useState<boolean>(false);
  const { width } = useWindowSize();
  const location = useLocation();
  const sidebarCtx = useContext(SidebarContext);
  const loginCtx = useContext(LoginContext);
  const { t } = useTranslation();

  const setProducts = useAdminStore((state) => state.setProducts);
  const token = useAdminStore((state) => state.token);
  const setToken = useAdminStore((state) => state.setToken);
  const resourceGroup = useAdminStore((state) => state.resourceGroup);

  function openSidebarHandler() {
    setProducts([]);
    if (token) getProducts(token);

    //for width>768(tablet size) if sidebar was open in width<768 was opened too.
    //just in case of tablet size and smaller then, sidebar__open can added.
    if (width <= 768) document.body.classList.toggle("sidebar__open");
  }

  function logoutHandler() {
    openSidebarHandler();
    loginCtx.toggleLogin();
  }
  async function getProducts(token: string) {
    setLoadingProducts(true);
    const data = await getProductsOfResourceGroup({ token });
    if (data?.status === 401) {
      setToken(null);
    }

    if (data?.status === 200) {
      setProducts(data?.products || []);
    }
    setLoadingProducts(false);
  }

  useEffect(() => {
    const curPath = window.location.pathname.split("/")[1];
    const activeItem = sidebarNav.findIndex((item) => item.section === curPath);

    setActiveIndex(curPath.length === 0 ? 0 : activeItem);
  }, [location]);

  return (
    <div
      className={`${classes.sidebar} ${
        !sidebarCtx.isOpen && classes.sidebar_close
      }`}
    >
      <div className={classes.sidebar__logo}>
        <img src={images.logo} alt="Tralpine" />
      </div>
      <div className={classes.sidebar__menu}>
        <Link className={classes.sidebar__menu__item} to={`assistant`}>
          <div className={classes.sidebar__menu__item__icon}>
            <Icon icon={""} />
          </div>
          <div className={classes.sidebar__menu__item__txt}>Assistant</div>
        </Link>
        {resourceGroup?.length > 0 &&
          <Link
            to={`products`}
            className={classes.sidebar__menu__item}
            onClick={openSidebarHandler}
          >
            <div className={classes.sidebar__menu__item__icon}>
              <Icon icon={""} />
            </div>
            <div className={classes.sidebar__menu__item__txt}>Products</div>
          </Link>
        }
        {/* {products.length > 0 ? (
          products?.map((item: string, index: number) => (
            <Link
              to={`products/${item}`}
              key={`nav-${index}`}
              className={`${classes.sidebar__menu__item} ${
                activeIndex === index && classes.active
              }`}
              onClick={openSidebarHandler}
            >
              <div className={classes.sidebar__menu__item__icon}>
                <Icon icon={item} />
              </div>
              <div className={classes.sidebar__menu__item__txt}>{item}</div>
            </Link>
          ))
        ) : (
          <h1>No Products to display</h1>
        )} */}
        {loadingProducts && <LoadingSpinner></LoadingSpinner>}
      </div>

      <div className={[classes.sidebar__menu, classes.logout].join("")}>
        <Link
          to="/landing"
          className={classes.sidebar__menu__item}
          onClick={logoutHandler}
        >
          <div className={classes.sidebar__menu__item__icon}>
            <Icon icon="tabler:logout" />
          </div>
          <div className={classes.sidebar__menu__item__txt}>{t("logout")}</div>
        </Link>
      </div>
    </div>
  );
}

export default Sidebar;
