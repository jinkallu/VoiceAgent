import React, {  useEffect } from "react";
import { useAdminStore } from "../store/zustand/store";


function Assistant() {
    const resourceGroup = useAdminStore((state) => state.resourceGroup);

    useEffect(() => {
        console.log(resourceGroup)

    }, [resourceGroup])
  
  return (
    <section>
        <div>
        Assistant
        </div>
        
        {resourceGroup.length > 0 && resourceGroup[0]["app-url"] && 
            <a href={resourceGroup[0]["app-url"]} target="_blank" rel="noopener noreferrer">
                {resourceGroup[0]["app-url"]}
            </a>
        }
        
    </section>
  );
}

export default Assistant;
