import React, { useContext, useEffect } from "react";
import { Outlet, useNavigate } from "react-router-dom";

import Sidebar from "../components/sidebar/Sidebar";
import TopNav from "../components/topnav/TopNav";
import sidebarNav from "../config/sidebarNav";
import { useAdminStore } from "../store/zustand/store";

import SidebarContext from "../store/sidebarContext";
import classes from "./MainLayout.module.scss";
import { getResouceGroupFromUsername } from "../services/apiService";

function MainLayout() {
  const sidebarCtx = useContext(SidebarContext);
  const token = useAdminStore((state) => state.token);
  const setResourceGroups = useAdminStore((state) => state.setResourceGroups);
  const setToken = useAdminStore((state) => state.setToken);
  const navigate = useNavigate();

  useEffect(() => {
    if (document.body.classList.contains("sidebar__open"))
      document.body.classList.remove("sidebar__open");
  }, []);

  // async function loadResourceGroups(token: string) {
  //   const rgs = await getResouceGroupFromUsername(token);
  //   if (rgs?.status === 200) {
  //     setResourceGroups(rgs?.rgs);
  //   } else if (rgs?.status === 401) {
  //     setToken(null);
  //     navigate("/login");
  //   }
  // }

  // useEffect(() => {
  //   if (token) loadResourceGroups(token);
  //   else navigate("/login");
  // }, [token]);

  return (
    <div className={classes.container}>
      <Sidebar />
      <div className={classes.main}>
        <div
          className={`${classes.main__content} ${
            !sidebarCtx.isOpen ? classes.close_sidebar : ""
          } main_wrapper`}
        >
          <TopNav />
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default MainLayout;
