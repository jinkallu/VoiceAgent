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

const createResourceGroup = async (token, name) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/createresourcegroup/", {
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

const getProductsOfResourceGroup = async ({ token }) => {
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
      return { status: 200, productData: data?.product_data || [] };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

const getProductResource = async (token, product_name, resource) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/product_resource/", {
      method: "POST",
      body: JSON.stringify({
        product_name,
        type: resource?.type || "",
        file_name: resource?.fileName || "",
      }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json", // Ensure you're sending JSON
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      const imageBlog = await response.blob();
      const imageURL = URL.createObjectURL(imageBlog);
      return { status: 200, imageURL };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};
const uploadProductData = async (token, product_name, data) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/upload_productdata/", {
      method: "POST",
      body: JSON.stringify({
        product_name,
        data,
      }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json", // Ensure you're sending JSON
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      return { status: 200 };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

const addProduct = async (token, product_name) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/add_product/", {
      method: "POST",
      body: JSON.stringify({
        product_name,
      }),
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json", // Ensure you're sending JSON
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      const data = await response.json();
      return { status: 200, data };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

const uploadPDF = async (token, formData) => {
  try {
    const response = await fetch("http://127.0.0.1:8000/upload_pdf/", {
      method: "POST",
      body: formData,

      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      const data = await response.json();
      console.log(data);
      return { ...data, status: 200 };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

export {
  getResourceGroups,
  createResourceGroup,
  getProductsOfResourceGroup,
  getResouceGroupFromUsername,
  getDataFromProductName,
  getProductResource,
  uploadProductData,
  addProduct,
  uploadPDF,
};
