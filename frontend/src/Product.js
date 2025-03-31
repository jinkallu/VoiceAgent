import React, { useState, useEffect } from "react";
import Problem from "./Problem";

const Product = ({ token, index, product }) => {
    const [message, setMessage] = useState("");
    const [product_data, setProductData] = useState("")
    const [images, setImages] = useState([]);


    const addImage = (name, imgdata) => {
        setImages(prev => [...prev, { name, imgdata }]);
    };

    const updateImage = (name, newImgData) => {
        setImages(prevImages =>
            prevImages.map(img =>
                img.name === name ? { ...img, imgdata: newImgData } : img
            )
        );
    };

    useEffect(() => {
        if (!product_data) {
            return;
        }

        if (!product_data.image_names) {
            return;
        }

        for (let i = 0; i < product_data.image_names.length; i++) {
            addImage(product_data.image_names[i], Node);

            // Define your request payload
            const requestData = {
                img_url: product_data.image_names[i] || null,  // Example data to send
            };

            fetch("http://127.0.0.1:8000/product_image/", {
                method: "POST",  // Use POST method to send data
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json'  // Ensure you're sending JSON 
                },
                body: JSON.stringify(requestData),  // Convert the JavaScript object to JSON string
            })
                .then((res) => res.json())
                .then((data) => {
                    console.log(data)
                    updateImage(product_data.image_names[i], data.image_data || []);
                })
                .catch(() => setMessage("Unauthorized"));
        }

    }, [product_data])

    useEffect(() => {

        if (!product) {
            return
        }
        console.log(product)

        // Define your request payload
        const requestData = {
            product_name: product.json || null,  // Example data to send
        };


        fetch("http://127.0.0.1:8000/product_data/", {
            method: "POST",  // Use POST method to send data
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'  // Ensure you're sending JSON 
            },
            body: JSON.stringify(requestData),  // Convert the JavaScript object to JSON string
        })
            .then((res) => res.json())
            .then((data) => {
                console.log(data)
                setProductData(data.product_data || []);
            })
            .catch(() => setMessage("Unauthorized"));

    }, [product])

    const getImageDataByName = (name) => {
        const image = images.find(img => img.name === name);
        return image ? image.imgdata : null;
    };

    const getImageExtension = (name) => {
        return name.substring(name.lastIndexOf(".") + 1);
    }

    return (
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <li key={index}>
                <strong>{product.name}</strong>
            </li>
            {/* Left section for Product Data */}
            <div style={{ flex: 1, marginRight: '20px' }}>
                <ul>
                    {Array.isArray(product_data.data) && product_data.data.length > 0 ? (
                        product_data.data.map((p, pindex) => (
                            <Problem token={token} index={pindex} problem={p} />
                        )
                        )
                    ) : (
                        <p>No Problems found</p>
                    )}

                </ul>
            </div>
            {/* Right section for Images */}
            <div style={{ flex: 1 }}>
                <div>
                    {/* Assuming you have an array of images */}
                    {product_data.image_names && product_data.image_names.length > 0 ? (
                        product_data.image_names.map((image, index) => (
                            <img
                                key={index}
                                src={`data:image/${getImageExtension(image)};base64,${getImageDataByName(image)}`}
                                alt={image}
                                style={{ width: '100px', height: '100px', marginBottom: '10px' }}
                                draggable
                                onDragStart={(e) => {
                                    const imageData = getImageDataByName(image);
                                    e.dataTransfer.setData("imageName", image);
                                    e.dataTransfer.setData("imageData", imageData);
                                }}
                            />
                        ))
                    ) : (
                        <p>No images available</p>
                    )}
                </div>
            </div>

        </div>
    );
};

export default Product;
