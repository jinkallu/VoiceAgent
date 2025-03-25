const getResourceGroups = async (token) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/resourcegroups/", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const data = await response.json();
    if (data?.resource_groups) return data.resource_groups;
    return;
  } catch (e) {
    console.log(e);
    return;
  }
};

const getProductsOfResourceGroup = async (token, resourceGroupName) => {
  const requestData = {
    rg_name: resourceGroupName, // Example data to send
  };
  try {
    const response = await fetch("http://127.0.0.1:8000/products/", {
      method: "POST", // Use POST method to send data
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json", // Ensure you're sending JSON
      },
      body: JSON.stringify(requestData), // Convert the JavaScript object to JSON string
    });
    const data = await response.json();
    return data?.products || [];
  } catch (e) {
    console.log(e);
    return;
  }
};

export { getResourceGroups, getProductsOfResourceGroup };
