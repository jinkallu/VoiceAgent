import React, { useEffect, useState } from "react";
import { useAdminStore } from "../store/zustand/store";
import { createResourceGroup } from "../services/apiService"


function Assistant() {
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [resourceName, setResourceName] = useState("");
    const resourceGroup = useAdminStore((state) => state.resourceGroup);
    const token = useAdminStore((state) => state.token);

    useEffect(() => {
        console.log(resourceGroup)

    }, [resourceGroup])

    async function createAssistant(res_name:string){
        if (!res_name){
            return
        }
        const res = await createResourceGroup(token, res_name);
    }

    return (
        
            <div>
                Assistant
           

            {resourceGroup.length > 0 && resourceGroup[0]["app-url"] &&
                <section>
                <a href={resourceGroup[0]["app-url"]} target="_blank" rel="noopener noreferrer">
                    {resourceGroup[0]["app-url"]}
                </a>
                </section>
            }
            {
                resourceGroup.length === 0 && !isModalOpen &&(
                <div>
                    <button
                        onClick={() => setIsModalOpen(true)}
                        className="p-2 bg-blue-500 text-white rounded"
                    >
                        Create Assistant
                    </button>
                </div>
                )
            }
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
                            <button
                                onClick={() => setIsModalOpen(false)}
                                className="mr-2 px-4 py-2 bg-gray-400 rounded"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={() => {
                                    //console.log("Resource Created:", resourceName);
                                    createAssistant(resourceName)
                                    setIsModalOpen(false);
                                }}
                                className="px-4 py-2 bg-blue-500 text-white rounded"
                            >
                                Create
                            </button>
                        </div>
                    </div>
                </div>
            )}
        
        </div>
  );
}

export default Assistant;
