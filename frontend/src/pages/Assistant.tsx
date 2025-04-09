import React, { useEffect, useState, useRef, useContext } from "react";
import { useAdminStore } from "../store/zustand/store";
import { createResourceGroup, restartApp } from "../services/apiService";
import Button from "../components/UI/button/Button";
import LoadingSpinner from "../components/UI/loadingSpinner/LoadingSpinner";
import classes from "../components/login/Login.module.scss";
import { useTranslation } from "react-i18next";
import langContextObj from "../store/langContext"
import { useNavigate } from "react-router-dom";


function Assistant() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [resourceName, setResourceName] = useState("");
  const resourceGroup = useAdminStore((state) => state.resourceGroup);
  const token = useAdminStore((state) => state.token);
  const [isLoading, setIsLoading] = useState(false);
  const errorMessageRef = useRef<HTMLSpanElement>(null);
  const { t } = useTranslation();
  const langCtx = useContext(langContextObj);
  const setToken = useAdminStore((state) => state.setToken);
  const setUserName = useAdminStore((state) => state.setUserName);
  const setResourceGroup = useAdminStore((state) => state.setResourceGroup);
  const navigate = useNavigate();


  useEffect(() => {
    console.log(resourceGroup);
  }, [resourceGroup]);

  async function createAssistant(res_name: string) {
    if (!res_name) {
      return;
    }
    const isOnlyLowercaseLetters = /^[a-z]+$/.test(res_name);
    if (!isOnlyLowercaseLetters) {
      console.error("Resource name must contain only lowercase letters (a–z).");
      return;
    }
    setIsLoading(true);
    const data = await createResourceGroup(token, res_name);
    if (data?.access_token) {
      setToken(data.access_token);
      setResourceGroup(data?.resourceGroups || []);
      localStorage.setItem("token", data.access_token);
      //loginCtx.toggleLogin();
      setTimeout(() => {
        navigate("/");
      }, 500); // Wait 100ms before navigating
    }
    setIsLoading(false);
    setIsModalOpen(false);
  }

  async function restart() {
    const res = await restartApp(token);
  }

  return (
    <section>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "start",
          gap: "15px",
        }}
      >
        <h3>Assistant</h3>
        {resourceGroup.length > 0 && resourceGroup[0]["app-url"] && (
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "start",
              gap: "25px",
            }}
          >
            <p>
              Visit the assistant using following URL. Add products and trouble
              shooting steps.
            </p>
            <a
              style={{
                backgroundColor: "red",
                color: "white",
                padding: "1em 1.5em",
                textDecoration: "none",
                textTransform: "uppercase",
                borderRadius: "5px",
              }}
              href={resourceGroup[0]["app-url"]}
              target="_blank"
              rel="noopener noreferrer"
            >
              Open Assistant
            </a>
            <iframe
              src={resourceGroup[0]["app-url"]}
              allow="microphone"
              style={{ width: "100%", height: "500px", border: "none" }}
            />
            <Button onClick={() => restart()}>
              Restart App
            </Button>
          </div>
        )}
        {resourceGroup?.length === 0 && !isModalOpen && (
          <div>
            <Button onClick={() => setIsModalOpen(true)}>
              Create Assistant
            </Button>
          </div>
        )}
        {/* Modal */}
        {isModalOpen && (
          <div className="fixed inset-0 flex items-center justify-center bg-gray-900 bg-opacity-50">
            <div className="bg-white p-4 rounded shadow-lg w-1/3">
              <h2 className="text-lg font-bold mb-4">Create Assistant</h2>
              <input
                type="text"
                placeholder="Enter assistant name"
                value={resourceName}
                onChange={(e) => setResourceName(e.target.value)}
                className="w-full p-2 border rounded"
              />
              <div >
                <span ref={errorMessageRef} className={classes.errorMessage}>
                  {t("assistanterrorMessage")}
                </span>
              </div>
              <div className="mt-4 flex justify-end">
                <Button outline onClick={() => setIsModalOpen(false)}>
                  Cancel
                </Button>
                <Button
                  onClick={() => {
                    createAssistant(resourceName);
                    //setIsModalOpen(false);
                  }}
                >
                  Create
                </Button>
              </div>
              {isLoading && <LoadingSpinner></LoadingSpinner>}
              {isLoading && (
                <h4>Please wait .. Proessing can take a couple of minutes..!</h4>
              )}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

export default Assistant;
