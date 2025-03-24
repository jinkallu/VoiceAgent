import React, { useState, useEffect } from "react";

const ImageResource = ({ token, index, step }) => {
    const [imageName, setImageName] = useState(null); // Store the image URL
    const [imageData, setImageData] = useState(null); // Store the image URL

    // Handle the image drop
    const handleDrop = (e) => {
        e.preventDefault(); // Prevent default behavior (prevent file opening)
        const imgName = e.dataTransfer.getData("imageName");
        setImageName(imgName)
        const imgData = e.dataTransfer.getData("imageData");
        setImageData(imgData)
    };

    // Allow the drop by preventing the default behavior
    const handleDragOver = (e) => {
        e.preventDefault(); // Necessary for dropping to work
    };

    const getImageExtension = (name) => {
        return name.substring(name.lastIndexOf(".") + 1);
    }

    return (
        <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            style={{
                border: "2px dashed #ccc",
                padding: "20px",
                width: "300px",
                height: "50px",
                textAlign: "center",
                position: "relative",
                backgroundColor: imageData ? "transparent" : "#f9f9f9",
            }}
        >
            {imageData ? (
                <img
                    src={`data:image/${getImageExtension(imageName)};base64,${imageData}`}
                    alt="Dropped"
                    style={{
                        maxWidth: "100%",
                        maxHeight: "100%",
                        objectFit: "contain",
                    }}
                />
            ) : (
                <p>Drag and drop an image here</p>
            )}
        </div>
    );
};

export default ImageResource;
