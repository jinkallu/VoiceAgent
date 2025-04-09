import React, { useContext, useEffect, useRef, useState } from "react";

import LoginContext from "../../store/loginContext";
import langContextObj from "../../store/langContext";
import { images } from "../../constants";
import Input from "../UI/input/Input";
import Button from "../UI/button/Button";
import { useTranslation } from "react-i18next";
import classes from "./Login.module.scss";
import { Link, useNavigate } from "react-router-dom";
import { useAdminStore } from "../../store/zustand/store";
import { authenticate } from "../../services/apiService";
import LoadingSpinner from "../UI/loadingSpinner/LoadingSpinner";
import { tokenToString } from "typescript";

function LoginBox() {
  const loginCtx = useContext(LoginContext);
  const langCtx = useContext(langContextObj);
  const userNameRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const errorMessageRef = useRef<HTMLSpanElement>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const navigate = useNavigate();
  const { t } = useTranslation();
  const setToken = useAdminStore((state) => state.setToken);
  const setUserName = useAdminStore((state) => state.setUserName);
  const setResourceGroup = useAdminStore((state) => state.setResourceGroup);

  async function loginHandler(e: React.FormEvent) {
    e.preventDefault();
    if (!userNameRef.current?.value || !passwordRef.current?.value) {
      return;
    }
    setIsLoading(true);
    const data = await authenticate(
      userNameRef.current?.value,
      passwordRef.current?.value
    );

    if (data?.access_token) {
      setToken(data.access_token);
      setResourceGroup(data?.resourceGroups || []);
      localStorage.setItem("token", data.access_token);
      setUserName(userNameRef?.current?.value);
      loginCtx.toggleLogin();
      setTimeout(() => {
        navigate("/");
      }, 500); // Wait 100ms before navigating
    } else {
      userNameRef?.current?.focus();
      errorMessageRef.current?.setAttribute(
        "style",
        "display: inline-block;opacity: 1"
      );
    }
    setIsLoading(false);
  }

  return (
    <div
      className={`${classes.container} ${
        langCtx.lang === "fa" ? classes.rtl : ""
      }`}
    >
      <div className={classes.loginBox}>
        <div className={classes.logo}>
          <img src={images.logo} alt="digikala" />
        </div>
        <h2 className={classes.title}>{t("loginPage")}</h2>
        <form onSubmit={loginHandler}>
          <Input
            ref={userNameRef}
            type={"text"}
            id={"userName"}
            //placeholder={"admin"}
          />
          <span ref={errorMessageRef} className={classes.errorMessage}>
            {t("errorMessage")}
          </span>
          <Input type={"password"} id={"pass"}  ref={passwordRef} />
          <Button type="submit">{t("login")}</Button>
          {isLoading && <LoadingSpinner></LoadingSpinner>}
          <Link className={classes.forgat_pass} to="/">
            {t("forgetPass")}
          </Link>
          <div className={classes.checkbox}>
            <input type="checkbox" id="rememberMe" />
            <label htmlFor="rememberMe">{t("rememberMe")}</label>
          </div>
        </form>
        <Link className={classes.forgat_pass} to="/register">
          Register
        </Link>
      </div>

      <div className={classes.keyPic}>
        <img
          src={require("../../assets/images/tralpinechat_small.png")}
          alt="Tralpine chat"
        />
      </div>
    </div>
  );
}

export default LoginBox;
