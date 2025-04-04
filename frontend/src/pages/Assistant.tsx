import React, { useEffect, useState } from "react";
import { useAdminStore } from "../store/zustand/store";
import { createResourceGroup } from "../services/apiService";
import Button from "../components/UI/button/Button";

function Assistant() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [resourceName, setResourceName] = useState("");
  const resourceGroup = useAdminStore((state) => state.resourceGroup);
  const token = useAdminStore((state) => state.token);

  useEffect(() => {
    console.log(resourceGroup);
  }, [resourceGroup]);

  async function createAssistant(res_name: string) {
    if (!res_name) {
      return;
    }
    const res = await createResourceGroup(token, res_name);
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
          </div>
        )}
        {resourceGroup.length === 0 && !isModalOpen && (
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
                placeholder="Enter resource name"
                value={resourceName}
                onChange={(e) => setResourceName(e.target.value)}
                className="w-full p-2 border rounded"
              />
              <div className="mt-4 flex justify-end">
                <Button outline onClick={() => setIsModalOpen(false)}>
                  Cancel
                </Button>
                <Button
                  onClick={() => {
                    createAssistant(resourceName);
                    setIsModalOpen(false);
                  }}
                >
                  Create
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}

export default Assistant;
