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

const getProductsOfResourceGroup = async (token) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/products/", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json", // Ensure you're sending JSON
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      const data = await response.json();
      return { status: 200, products: data?.products || [] };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};
const getResouceGroupFromUsername = async (token) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/loadresourcegroups/", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json", // Ensure you're sending JSON
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      const data = await response.json();
      return { status: 200, rgs: data?.resource_groups || [] };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

const getDataFromProductName = async (token, product_name) => {
  console.log("product name", product_name);
  try {
    const response = await fetch("http://127.0.0.1:8000/product_data/", {
      method: "POST",
      body: JSON.stringify({ product_name }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json", // Ensure you're sending JSON
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      const data = await response.json();
      console.log(data);
      return { status: 200, productData: data?.product_data || [] };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

export {
  getResourceGroups,
  getProductsOfResourceGroup,
  getResouceGroupFromUsername,
  getDataFromProductName,
};
