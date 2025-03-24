import React, { useState, useEffect } from "react";

const ImageResource = ({ token, index, step }) => {
    const [imageUrl, setImageUrl] = useState(null); // Store the image URL

    // Handle the image drop
    const handleDrop = (e) => {
        e.preventDefault(); // Prevent default behavior (prevent file opening)
        const imageName = e.dataTransfer.getData("imageName");
        const imageData = e.dataTransfer.getData("imageData");
    };

    // Allow the drop by preventing the default behavior
    const handleDragOver = (e) => {
        e.preventDefault(); // Necessary for dropping to work
    };

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
                backgroundColor: imageUrl ? "transparent" : "#f9f9f9",
            }}
        >
            {imageUrl ? (
                <img
                    src={imageUrl}
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
