const API_BASE_URL = process.env.REACT_APP_API_URL;

const registerUser = async (username, password, email) => {
  try {
    const response = await fetch(`${API_BASE_URL}/register/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        password,
        email
      }),
    });

    const data = await response.json();
    return data

  } catch (e) {
    console.log(e);
    return;
  }

}

const authenticate = async (username, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: "POST",
      body: JSON.stringify({ username, password }),
      headers: {
        "Content-Type": "application/json", // <-- Add this!
      },
    });

    const data = await response.json();
    console.log(data);
    return data;
  } catch (e) {
    console.log(e);
    return;
  }
};

const getResourceGroups = async (token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/resourcegroups/`, {
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

const restartApp = async (token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/restart_app/`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
    });

    // const data = await response.json();
    // if (data?.resource_groups) return data.resource_groups;
    return;
  } catch (e) {
    console.log(e);
    return;
  }
};

const createResourceGroup = async (token, res_name) => {
  try {
    const response = await fetch(`${API_BASE_URL}/createresourcegroup/`, {
      method: "POST",
      body: JSON.stringify({
        res_name,
      }),
      headers: {
        "Content-Type": "application/json", // <-- Add this!
        Authorization: `Bearer ${token}`,
      },
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
    const response = await fetch(`${API_BASE_URL}/products/`, {
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
    const response = await fetch(`${API_BASE_URL}/loadresourcegroups/`, {
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
    const response = await fetch(`${API_BASE_URL}/product_data/`, {
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
    const response = await fetch(`${API_BASE_URL}/product_resource/`, {
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
    const response = await fetch(`${API_BASE_URL}/upload_productdata/`, {
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
    const response = await fetch(`${API_BASE_URL}/add_product/`, {
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
    const response = await fetch(`${API_BASE_URL}/upload_pdf/`, {
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

const downloadZip = async (token) => {
  try {
    const response = await fetch(`${API_BASE_URL}/download_zip/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status !== 200) {
      return { status: response.status, message: "Unauthorized" };
    } else {
      const blob = await response.blob();

      // Create a download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "images.zip"; // You can dynamically set the name here if needed
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url); // Clean up
      return { status: 200 };
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

const uploadImage = async (token, formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/upload_image/`, {
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
      return data;
    }
  } catch (e) {
    console.log(e);
    return;
  }
};

const removeResource = async (token, product_name, resource) => {
  try {
    const response = await fetch(`${API_BASE_URL}/remove_resource/`, {
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
      const data = await response.json();
      console.log(data);
      return { status: 200, data };
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
  removeResource,
  uploadImage,
  authenticate,
  registerUser,
  restartApp,
  downloadZip
};
