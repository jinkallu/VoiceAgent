import React, { useContext, useEffect, useRef } from "react";

import LoginContext from "../../store/loginContext";
import langContextObj from "../../store/langContext";
import { images } from "../../constants";
import Input from "../UI/input/Input";
import Button from "../UI/button/Button";
import { useTranslation } from "react-i18next";
import classes from "./Login.module.scss";
import { Link, useNavigate } from "react-router-dom";
import { useAdminStore } from "../../store/zustand/store";
import { registerUser } from "../../services/apiService";

function RegisterBox() {
  const loginCtx = useContext(LoginContext);
  const langCtx = useContext(langContextObj);
  const userNameRef = useRef<HTMLInputElement>(null);
  const emailRef = useRef<HTMLInputElement>(null);
  const passwordRef = useRef<HTMLInputElement>(null);
  const verifyPasswordRef = useRef<HTMLInputElement>(null);
  const errorMessageRef = useRef<HTMLSpanElement>(null);
  const registerSuccessMessage = useRef<HTMLSpanElement>(null);
  const userNameErrorMessage = useRef<HTMLSpanElement>(null);
  const navigate = useNavigate();
  const { t } = useTranslation();
  const setToken = useAdminStore((state) => state.setToken);
  const setResourceGroup = useAdminStore((state) => state.setResourceGroup);

  function checkPWDComplexity(pwd:string){
    // TODO: add more complexities
    if (!pwd){
        return false;
    }
    else if(pwd.length < 4){
        return false
    }
    return true
  }

  async function registerHandler(e: React.FormEvent) {
    e.preventDefault();

    if(passwordRef === null || verifyPasswordRef === null){
        return;
    }
    if(passwordRef.current === null || verifyPasswordRef.current === null){
        return;
    }
    

    const password = passwordRef.current.value;
    const verifyPassword = verifyPasswordRef.current.value;

    if (password !== verifyPassword) {
        passwordRef?.current?.focus();
        errorMessageRef.current?.setAttribute(
            "style",
            "display: inline-block;opacity: 1"
          );
        return
    } 

    if(!checkPWDComplexity(password)){
        errorMessageRef.current?.setAttribute(
            "style",
            "display: inline-block;opacity: 1"
          );
        return
    }

    const data = await registerUser(
      userNameRef.current?.value,
      passwordRef.current?.value,
      emailRef.current?.value,
    )
    
    console.log(data);
    if (data) {
      // console.log(data);
      // setToken(data.access_token);
      // setResourceGroup(data?.resourceGroups || []);
      // localStorage.setItem("token", data.access_token);
      // loginCtx.toggleLogin();
      registerSuccessMessage.current?.setAttribute(
        "style",
        "display: inline-block;opacity: 1",
      );
      setTimeout(() => {
        navigate("/");
      }, 3000); // Wait 100ms before navigating
    } else {
      userNameRef?.current?.focus();
      userNameErrorMessage.current?.setAttribute(
        "style",
        "display: inline-block;opacity: 1",
      );
    }
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
        <h2 className={classes.title}>{t("registrationPage")}</h2>
        <form onSubmit={registerHandler}>
          <Input
            ref={userNameRef}
            type={"text"}
            id={"userName"}
            placeholder={"admin"}
            value="test"
          />
          <span ref={registerSuccessMessage} className={classes.successMessage}>
            {t("registerSuccessMessage")}
          </span>
          <span ref={userNameErrorMessage} className={classes.errorMessage}>
            {t("userNameErrorMessage")}
          </span>
          <Input type="email" id="email" placeholder="Work Email" ref={emailRef} />
          <Input type={"password"} id={"pass"} ref={passwordRef} />
          <span ref={errorMessageRef} className={classes.errorMessage}>
            {t("pwdErrorMessage")}
          </span>
          <Input type={"password"} id={"veripass"} ref={verifyPasswordRef}/>
          <Button type="submit">{t("register")}</Button>
        </form>       
        <Link className={classes.forgat_pass} to="/login">
          Login
          </Link> 
      </div>

      <div className={classes.keyPic}>
        <img
          src={require("../../assets/images/Revenue-cuate.svg").default}
          alt="illustrator key"
        />
      </div>
    </div>
  );
}

export default RegisterBox;
